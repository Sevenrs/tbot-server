#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character, Shop
from GameServer.Controllers.data.client import CLIENT_VERSION, PING_TIMEOUT
import MySQL.Interface as MySQL
from dotenv import dotenv_values
import requests
import re, time, _thread, datetime

"""
This method will send the new client its unique ID
"""
def id_request(**_args):

    # If our client is already registered, drop the packet
    if _args['client'] in _args['server'].clients:
        return

    # Read account name from packet
    client_version  = _args['packet'].ReadString()
    account         = _args['packet'].ReadString()

    # Create error packet, in the event we require it
    error = PacketWrite()
    error.AddHeader(bytearray([0xE2, 0x2E]))
    error.AppendBytes([0x00])

    # Read environment variables
    env = dotenv_values('.env')

    # Check if we are authorized to use this account
    response = requests.post("{0}/verify".format(env['INTERNAL_ROOT_URL']),
                             json={
                                 "username": account,
                                 "ip": _args['socket'].getpeername()[0]
                             },

                             headers={
                                 "Content-Type": "application/json",
                                 "Authorization": env['INTERNAL_ACCESS_TOKEN']
                             })


    # Get user and check if we have a result. Just disconnect the client if we do not.
    if response.status_code != 200:
        raise Exception('Verification failed')

    # Fetch the response into a readable list
    verification_response = response.json()

    # Get internal user from the database
    _args['mysql'].execute('SELECT `id` FROM `users` WHERE `external_id` = %s', [
        verification_response['web_id']
    ])
    internal_user = _args['mysql'].fetchone()

    # Check if the internal user was found
    if internal_user is None:
        raise Exception('Internal user could not be found')

    ''' If the client version is incorrect, we must send an error message and disconnect the client. '''
    if client_version != CLIENT_VERSION:
        error.AppendInteger(14, 1, 'little') # Client version error
        _args['socket'].send(error.packet)
        raise Exception('Invalid client version')

    # Get available ID
    id = 0
    for i in range(65535):

        # If the ID is in use, skip the iteration
        if i in _args['server'].client_ids:
            continue

        # If the ID is not in the client id container of the server, use the id and add it to the container
        id = i
        _args['server'].client_ids.append(id)
        break
    
    # Update our socket to use this ID and assign the account to it as well
    _args['client']['id']           = id                                        # Client identification number
    _args['client']['account']      = verification_response['username']         # The username from the website
    _args['client']['account_id']   = internal_user['id']                       # User ID in our local database, not the web id
    _args['client']['warnet_bonus'] = verification_response['warnet_bonus']     # Whether this user is eligible for the warnet bonus icon
    _args['client']['character']    = None                                      # Character object
    _args['client']['new']          = True                                      # Whether we need to send the initial lobby message
    _args['client']['needs_sync']   = False                                     # Whether we need to send a character sync packet
    _args['client']['lobby_data']   = {'mode': 0, 'page': 0}                    # Lobby information
    _args['client']['last_ping']    = datetime.datetime.now()                   # Last ping timestamp

    # Disconnect all connected sessions with this account name (to stop two or more clients with the same account)
    for session in _args['connection_handler'].GetClients():
        if session['account'] == account and session['socket'] is not _args['socket']:
            _args['connection_handler'].UpdatePlayerStatus(session, 2)

    # Find our relay client and connect it with this client
    for client in _args['server'].relay_server.clients:
        if client['account'] == _args['client']['account']:
            client['game_client'] = _args['client']
            client['game_server'] = _args['server']
            _args['client']['relay_client'] = client
            break
    
    # Add new connection to server client container
    _args['server'].clients.append(_args['client'])

    ''' If we have no relay client, then something is wrong. We must have a relay client.
            In this case, close our own connection. '''
    if 'relay_client' not in _args['client']:
        error.AppendInteger(4, 1, 'little') # Protocol error
        _args['socket'].send(error.packet)
        return _args['connection_handler'].CloseConnection(_args['client'])

    # Construct ID request response and send it to the client
    reply = PacketWrite()
    reply.AddHeader(bytearray([0xE0, 0x2E]))
    reply.AppendInteger(id, 2, 'little')
    reply.AppendBytes([0x01, 0x00])
    _args['socket'].send(reply.packet)

    # Start ping thread
    _thread.start_new_thread(ping, (_args,))
    
"""
This method will obtain the character and return it to the client
"""
def get_character(**_args):
    print('Character request for', _args['client']['account'])
    
    # Check if we have a character for this account
    _args['mysql'].execute("""SELECT `character`.* FROM `characters` `character` WHERE character.user_id = %s
            ORDER BY `character`.`id` ASC LIMIT 1""", [
        _args['client']['account_id']
    ])
    
    # Fetch character row
    character = _args['mysql'].fetchone()
    
    # If we do not have a character, simply send the character not found packet
    if character is None:
        _args['socket'].send(bytearray([0xE1, 0x2E, 0x02, 0x00, 0x00, 0x35]))
    else:

        # Append the character to the client instance and also pass the client instance to the
        # global server client container
        _args['client']['character'] = character
        _args['connection_handler'].UpdatePlayerStatus(_args['client'])
        
        # Construct character information packet and send it over
        character_information = PacketWrite()
        character_information.AddHeader(bytearray([0xE1, 0x2E]))
        character_information.AppendBytes([0x01, 0x00])
        character_information.AppendBytes(Character.construct_bot_data(_args, character))
        _args['socket'].send(character_information.packet)

"""
This method will handle new character creation requests
"""
def create_character(**_args):
    
    # Character creation results
    character_create_success      = bytearray([0x01, 0x00])
    character_create_name_taken   = bytearray([0x00, 0x36])
    character_create_name_error   = bytearray([0x00, 0x33])
    
    character_type  = int(_args['packet'].GetByte(2))
    username        = _args['packet'].ReadString(6)[1:]
    character_name  = _args['packet'].ReadString()

    # Read environment variables
    env = dotenv_values('.env')

    # Verify if we have authorization to create a character for this user
    response = requests.post("{0}/verify".format(env['INTERNAL_ROOT_URL']),
                             json={
                                 "username": username,
                                 "ip": _args['socket'].getpeername()[0]
                             },

                             headers={
                                 "Content-Type": "application/json",
                                 "Authorization": env['INTERNAL_ACCESS_TOKEN']
                             })

    if response.status_code != 200:
        raise Exception('Validation failed while trying to create a character')
    
    # Find the internal user
    _args['mysql'].execute('SELECT `id` FROM `users` WHERE `external_id` = %s', [ response.json()['web_id'] ])
    internal_user = _args['mysql'].fetchone()
    
    # Check if there's already a character connected to this account
    _args['mysql'].execute('SELECT `id` FROM `characters` WHERE `user_id` = %s', [ internal_user['id'] ])
    if _args['mysql'].rowcount > 0:
        raise Exception('User attempted to create a character while already having a character')
    
    # Check the character type is between 1 and 3
    elif character_type < 1 or character_type > 3:
        raise Exception('User sent an invalid character type')
    
    # Create a new packet with the character creation result command
    packet = PacketWrite()
    packet.AddHeader(bytearray([0xE2, 0x2E]))
    
    # Check if the name has been taken. If so, send error and close connection.
    _args['mysql'].execute('SELECT `id` FROM `characters` WHERE `name` = %s', [character_name])
    if _args['mysql'].rowcount > 0:
        packet.AppendBytes(character_create_name_taken)
        _args['socket'].send(packet.packet)
        return _args['connection_handler'].CloseConnection(_args['client'])

    # Check if the name is valid. If not, send error and close connection.
    elif not re.match('^[a-zA-Z0-9]+$', character_name) or len(character_name) < 4 or len(character_name) > 13:
        packet.AppendBytes(character_create_name_error)
        _args['socket'].send(packet.packet)
        return _args['connection_handler'].CloseConnection(_args['client'])
    else:
        packet.AppendBytes(character_create_success)
        
        # Insert the new character in the database
        _args['mysql'].execute("""INSERT INTO `characters` (`user_id`, `name`, `type`) VALUES (%s, %s, %s)""",
                       [ internal_user['id'], character_name, character_type ])

        # Retrieve character id of the character we just built and create a new wearing and inventory table for our character
        character_id = _args['mysql'].lastrowid
        _args['mysql'].execute('INSERT INTO `character_wearing` (`character_id`) VALUES (%s)', [character_id])
        _args['mysql'].execute('INSERT INTO `inventory` (`character_id`) VALUES (%s)', [character_id])

        # Send success status to the client
        _args['socket'].send(packet.packet)

"""
This method will handle exit server requests
"""
def exit_server(**_args):
    
    # Send acknowledgement to the client
    exit = PacketWrite()
    exit.AddHeader(bytearray([0x0A, 0x2F]))
    exit.AppendBytes(bytearray([0x01, 0x00]))
    _args['socket'].send(exit.packet)
    
    # Disconnect the client, in case the connection is still alive
    _args['connection_handler'].UpdatePlayerStatus(_args['client'], 2)

'''
This method will ask the client to send back a pong packet to the server so we know
it is still alive
'''
def ping(_args):

    while _args['client'] in _args['server'].clients:

        # If the amount of seconds between now and the last ping exceeds 90, disconnect the client
        if (datetime.datetime.now() - _args['client']['last_ping']).total_seconds() >= PING_TIMEOUT:
            return _args['connection_handler'].UpdatePlayerStatus(_args['client'], 2)

        # Send ping packet and wait 1 second
        ping_rpc = PacketWrite()
        ping_rpc.AddHeader([0x01, 0x00])
        ping_rpc.AppendBytes([0xCC])
        try:
            _args['client']['socket'].send(ping_rpc.packet)
        except Exception:
            pass
        time.sleep(1)

'''
This method is invoked when the client sends us a pong packet indicating it is still alive.
We should update the last ping time
'''
def pong(**_args):
    _args['client']['last_ping'] = datetime.datetime.now()

    # Additionally, if the relay tcp client is still alive then we can update its last ping timestamp as well
    if 'relay_client' in _args['client']:
        _args['client']['relay_client']['last_ping'] = datetime.datetime.now()