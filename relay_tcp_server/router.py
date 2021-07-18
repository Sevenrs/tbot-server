from Packet.Write import Write as PacketWrite
from GameServer.Controllers.Room import get_slot
import _thread, time, socket
import MySQL.Interface as MySQL

def route(client, packet):

    packets = {
        '32a0': id_request,
        '36a0': check_connection,
        '37a0': remove_connection
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
def id_request(**_args):

    # Read account name from the packet
    account = _args['packet'].ReadString()[1:]

    # Create MySQL connection to see if we are authorized to use this account
    connection = MySQL.GetConnection()
    cursor = connection.cursor(dictionary=True)
    cursor.execute(
        'SELECT `id` FROM `users` WHERE `username` = %s AND `banned` = 0 AND `last_ip` = %s',[
            account, _args['client']['socket'].getpeername()[0]
        ]
    )

    # Fetch user
    user = cursor.fetchone()

    # Before checking, close the SQL connection
    connection.close()

    # Check if the user exists. If it does not, throw an exception which closes the connection
    if user is None:
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
    _args['client']['account']  = account
    _args['client']['id']       = id

    # Add the client to our client container
    _args['client']['server'].clients.append(_args['client'])

    # Send response to client
    result = PacketWrite()
    result.AddHeader(bytes=[0x1A, 0xA4])
    result.AppendBytes([0x01, 0x00])
    result.AppendBytes([id & 0xFF, id >> 8 & 0xFF])
    _args['client']['socket'].send(result.packet)

    # After 10 seconds, we should check if we have a game client assigned
    _thread.start_new_thread(check_state, (_args['client'],))

'''
This method determines who is relayed and who is not
If a client is relay, their relay ID is pushed to the relay ID container
'''
def check_connection(**_args):
    for i in range(0, 8):
        start = (17 * i) + 8

        connected       = int(_args['packet'].ReadInteger(start + 2, 1, 'little'))
        character_name  = _args['packet'].ReadStringByRange(start + 2, (start + 17))

        if connected == 0 and len(character_name) > 0:
            room = _args['client']['game_server'].rooms[str(_args['client']['game_client']['room'])]

            # Find our slot
            slot_nr = get_slot({'client': _args['client']['game_client']}, room)
            room_slot = room['slots'][str(slot_nr)]

            # Add relay ID of the player that is not connected
            for client in _args['client']['server'].clients:
                if client['game_client']['character']['name'] == character_name:
                    if client['id'] not in room_slot['relay_ids']:
                        room_slot['relay_ids'].append(client['id'])

'''
This method removes a relay ID from the requesting client's relay ID container
'''
def remove_connection(**_args):
    character_name  = _args['packet'].ReadStringByRange(2, 17)

    # Find our own room
    room = _args['client']['game_server'].rooms[str(_args['client']['game_client']['room'])]

    # Remove relay ID from the room
    for client in _args['client']['server'].clients:
        if client['game_client']['character']['name'] == character_name:
            slot_nr = get_slot({'client': _args['client']['game_client']}, room)
            room_slot = room['slots'][str(slot_nr)]

            # It is possible this is invoked before the client sent the check_connection packet so we must check
            # if the id is actually in relay_ids
            if client['id'] in room_slot['relay_ids']:
                room_slot['relay_ids'].remove(client['id'])

    # It is possible that the connection was closed by the remote client causing the ID to be removed from
    # the state and not from the room, making the above snippet not work. This will loop through all IDs in the
    # entire room and check if we should remove them
    for i in range(0, 8):
        if str(i + 1) in room['slots']:
            ids = room['slots'][str(i + 1)]['relay_ids']
            for id in ids:
                if id not in _args['client']['server'].ids:
                    ids.remove(id)

''' Check if we have a client assigned after 10 seconds. If not, disconnect (time out)'''
def check_state(client):
    time.sleep(10)

    # Check if we have a game_client assigned to our client
    if 'game_client' not in client:
        print('timed out!')
        client['socket'].shutdown(socket.SHUT_RDWR)
        client['socket'].close()