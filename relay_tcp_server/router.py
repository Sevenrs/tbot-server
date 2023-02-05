import _thread
import datetime
import requests
import socket
import time
from dotenv import dotenv_values

from GameServer.Controllers.Room import get_slot
from Packet.Write import Write as PacketWrite
from ratelimit import LOGIN_VERIFY_RATE_LIMIT
from relay_tcp_server import connection as connection_handler
import MySQL.Interface as MySQL


def route(client, packet):
    print("[{0}] [client_id={1}] Got packet by ID: 0x{2} <{3}>".format(
        client['server'].name,
        client['id'] if 'id' in client else None,
        packet.id,
        packet.data
    ))

    packets = {
        '32a0': request_relay_login,
        '36a0': request_relay_user_info,
        '37a0': request_relay_user_exit
    }.get(packet.id, unknown)(**locals())


'''
Handle unknown packets by redirecting its contents to stdout
'''


def unknown(**_args):
    print("[{0}]: Unknown packet: <0x{1}[len={3}]::{2}>".format(_args['client']['server'].name, _args['packet'].id,
                                                                _args['packet'].data, len(_args['packet'].data)))


'''
Retrieve first available ID and register the client for later access
'''


def request_relay_login(**_args):

    # Read account name from the packet
    account = _args['packet'].read_string()[1:]

    # Consume login rate limit point
    LOGIN_VERIFY_RATE_LIMIT.try_acquire('LOGIN_RELAY_ID_REQUEST_{0}'.format(_args['client']['address'][0]))

    # Create MySQL connection, so we can see if this IP address is allowed to access the account
    connection = MySQL.get_connection()
    cursor = connection.cursor(dictionary=True)

    # Attempt to find a user by the username where our IP matches the last one
    cursor.execute('''SELECT `username` FROM `users` WHERE `username` = %s AND `last_ip` = %s''', [
        account,
        _args['client']['address'][0]
    ])

    # Fetch the user
    user = cursor.fetchone()

    # Close MySQL connection
    connection.close()

    # Create response packet
    result = PacketWrite()
    result.add_header(bytes=[0x1A, 0xA4])

    # Check if the user exists. If it does not, throw an exception which closes the connection
    if user is None:
        result.append_bytes([0x00])
        result.append_integer(50, 1, 'little')  # Incorrect authentication
        _args['client']['socket'].sendall(result.packet)
        raise Exception('IP address {0} is not authorized to sign in with account {1}'.format(
            _args['client']['socket'].getpeername()[0],
            account
        ))

    # Retrieve first available ID
    id = 0
    for i in range(65535):
        if i in _args['client']['server'].ids:
            continue

        id = i
        _args['client']['server'].ids.append(id)
        break

    # Fill our client object with relevant information
    _args['client']['account'] = user['username']
    _args['client']['id'] = id
    _args['client']['last_ping'] = datetime.datetime.now()

    # Add the client to our client container
    _args['client']['server'].clients.insert(id, _args['client'])

    # It is possible that the duplication check in the game server does not find all relay clients
    # This is because it is possible to have relay clients without a game client.
    # Disconnect any relay client that is connected with our account to stop the existence of multiple instances
    for client in _args['client']['server'].clients:
        if client['account'] == _args['client']['account'] and client is not _args['client']:
            connection_handler.close_connection(client)

    # Send response to client
    result.append_bytes([0x01, 0x00])
    result.append_bytes([id & 0xFF, id >> 8 & 0xFF])
    _args['client']['socket'].sendall(result.packet)

    # Start keep-alive thread
    _thread.start_new_thread(keep_alive, (_args,))


'''
This method determines who is relayed and who is not
If a client is relayed, their relay ID is pushed to the relay ID container
'''


def request_relay_user_info(**_args):
    # If our game client doesn't have a room, drop the packet
    if 'room' not in _args['client']['game_client']:
        return

    # Find our room, slot number and slot instance
    room = _args['client']['game_server'].rooms[str(_args['client']['game_client']['room'])]
    slot_nr = get_slot({'client': _args['client']['game_client']}, room)
    room_slot = room['slots'][str(slot_nr)]

    # Reset relay IDs to an empty array, we're starting off clean
    room_slot['relay_ids'] = []

    # Loop through all possible players
    for i in range(0, 8):

        # Dynamically calculate the index of data we need to read
        start = (17 * i) + 8

        # Read if the remote player is connected and their character name
        connected = int(_args['packet'].read_integer(start + 1, 1, 'little'))
        character_name = _args['packet'].read_string_by_range(start + 2, (start + 17))

        if len(character_name) > 0:
            print("[relay_tcp_server@request_relay_user_info()] <from: {2}> :: remote character: {0}, connected: {1}".format(
                character_name,
                connected,
                _args['client']['game_client']['character']['name']
            ))

        # If their character name exists and if they're not connected, we should add their ID to the relay ID array.
        if connected == 0 and len(character_name) > 0:

            # Attempt to find their client and add their relay ID to our container
            try:

                # Attempt to retrieve the remote client by looping through all clients.
                for client in _args['client']['server'].clients:

                    # Check if the game_client is not None to ensure it exists. We'll also be making sure this client
                    # has a character assigned to begin with.
                    if 'game_client' in client and client['game_client'] is not None \
                            and 'character' in client['game_client'] and client['game_client']['character'] is not None:

                        # Check if this is the client we are looking for by comparing the character name
                        if client['game_client']['character']['name'] == character_name:

                            # If the remote client ID is not already in the relay ID array, append the ID to the array.
                            if client['id'] not in room_slot['relay_ids']:
                                room_slot['relay_ids'].append(client['id'])
            except Exception as e:
                print(
                    'Failed to add a relay ID to the container because: {0}. It is likely the remote client no longer '
                    'exists'.format(
                        str(e)))


'''
This method removes a relay ID from the requesting client's relay ID container
'''


def request_relay_user_exit(**_args):
    # If our game client doesn't have a room, drop the packet
    if 'room' not in _args['client']['game_client']:
        return

    # Read character name
    character_name = _args['packet'].read_string_by_range(2, 17)

    # Find our own room, slot number and slot instance
    room = _args['client']['game_server'].rooms[str(_args['client']['game_client']['room'])]
    slot_nr = get_slot({'client': _args['client']['game_client']}, room)
    room_slot = room['slots'][str(slot_nr)]

    # Attempt to remove the relay ID from the room
    try:
        for client in _args['client']['server'].clients:

            # Check if the client is not None and if the game_client is also not None. We'll also check if the client
            # has a character assigned with it.
            if client is not None and 'game_client' in client and client['game_client'] is not None \
                    and 'character' in client['game_client'] and client['game_client']['character'] is not None:

                # Check if the character name is equal to the name we received
                if client['game_client']['character']['name'] == character_name:

                    # Check if the ID is in the array before attempting to remove it
                    if client['id'] in room_slot['relay_ids']:
                        room_slot['relay_ids'].remove(client['id'])
    except Exception as e:
        print(
            'Failed to remove a relay ID from the room because: {0}. It is likely that the remote client no longer '
            'exists.'.format(
                str(e)))

    # It is possible that the connection was closed by the remote client causing the ID to be removed from
    # the state and not from the room, making the above snippet not work. This will loop through all IDs in the
    # entire room and check if we should remove them based on their existence in the server ID container.
    for i in range(0, 8):
        if str(i + 1) in room['slots']:
            ids = room['slots'][str(i + 1)]['relay_ids']
            for id in ids:
                if id not in _args['client']['server'].ids:
                    ids.remove(id)


''' Check if our last ping timestamp is recent enough. If not, disconnect our client. '''


def keep_alive(_args):
    while _args['client'] in _args['client']['server'].clients:

        # Wait 10 seconds before checking
        time.sleep(10)

        # If the last ping was too long ago, disconnect the client
        if (datetime.datetime.now() - _args['client']['last_ping']).total_seconds() >= 90:
            return connection_handler.close_connection(_args['client'])
