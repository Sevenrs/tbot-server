#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character, Shop
import MySQL.Interface as MySQL
import re, time, _thread

"""
This method will send the new client its unique ID
"""
def id_request(**_args):

    # Read account name from packet
    account = _args['packet'].ReadString()

    # Get user from the database
    _args['mysql'].execute(
        'SELECT `id`, `username`, `active_bot_slot` FROM `users` WHERE `username` = %s AND `banned` = 0 AND `last_ip` = %s',
        [
            account,
            _args['socket'].getpeername()[0]
        ])

    # Get user and check if we have a result. Just disconnect the client if we do not
    user = _args['mysql'].fetchone()
    if user is None:
        raise Exception('Invalid user given in the ID request')
    
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

    print("Client id: {0}".format(id))
    
    # Update our socket to use this ID and assign the account to it as well
    _args['client']['id']           = id
    _args['client']['account']      = user['username']
    _args['client']['account_data'] = {'bot_slot': user['active_bot_slot'], 'id': user['id']}
    _args['client']['character']    = None
    _args['client']['new']          = True
    _args['client']['lobby_data']   = {'mode': 0, 'page': 0}

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
        return _args['connection_handler'].CloseConnection(_args['client'])

    # Construct packet and send it back to the client
    response = PacketWrite()
    response.AddHeader(bytearray([0xE0, 0x2E]))

    # Add connection ID and send the packet to the client
    response.AppendInteger(id, 2, 'little')
    response.AppendBytes([0x01, 0x00])

    _args['socket'].send(response.packet)

    # Start ping thread
    #_thread.start_new_thread(ping, (_args['server'], _args['client'],))
    
"""
This method will obtain the character and return it to the client
"""
def get_character(**_args):
    print('Character request for', _args['client']['account'])
    
    # Check if we have a bot in the active slot (or have a character, at all)
    _args['mysql'].execute("""SELECT `character`.* FROM `characters` `character` WHERE character.user_id = %s
                    ORDER BY `character`.`id` ASC LIMIT 1 OFFSET %s""", [
        _args['client']['account_data']['id'],
        _args['client']['account_data']['bot_slot']
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
    
    # Check if the username exists in the user table, close the connection if this fails
    _args['mysql'].execute('SELECT `id`, `banned`, `last_ip` FROM `users` WHERE `username` = %s', [username])
    user = _args['mysql'].fetchone()
    
    # Check if the row has been found and if it has been, check if the user has been banned
    if user is None:
        raise Exception('User was not found while trying to create a character')

    # Check if our ip address matches the last ip of the account.
    #   We should not be able to create a character that does not belong to us
    elif user['last_ip'] != _args['socket'].getpeername()[0]:
        raise Exception('The IP address the user connected from trying to create a character does not match the IP address in the database')
    
    # Check if the user has been banned
    elif user['banned'] == 1:
        raise Exception('User has been banned and attempted to create a character')
    
    # Check if there's already a character connected to this account
    _args['mysql'].execute('SELECT `id` FROM `characters` WHERE `user_id` = %s', [user['id']])
    if _args['mysql'].rowcount > 2:
        raise Exception('User attempted to create a character while already having the maximum amount of allowed characters')
    
    # Check the character type is between 1 and 3
    elif character_type < 1 or character_type > 3:
        raise Exception('User sent an invalid character type')
    
    # Create a new packet with the character creation result command
    packet = PacketWrite()
    packet.AddHeader(bytearray([0xE2, 0x2E]))
    
    # Check if the name has been taken
    _args['mysql'].execute('SELECT `id` FROM `characters` WHERE `name` = %s', [character_name])
    if _args['mysql'].rowcount > 0:
        packet.AppendBytes(character_create_name_taken)
    elif not re.match('^[a-zA-Z0-9]+$', character_name) or len(character_name) < 4 or len(character_name) > 13:
        packet.AppendBytes(character_create_name_error)
    else:
        packet.AppendBytes(character_create_success)
        
        # Insert the new character in the database
        _args['mysql'].execute("""INSERT INTO `characters` (`user_id`, `name`, `type`) VALUES (%s, %s, %s)""",
                       [user['id'], character_name, character_type])

        # Retrieve character id of the character we just built and create a new wearing and inventory table for our character
        character_id = _args['mysql'].lastrowid
        _args['mysql'].execute('INSERT INTO `character_wearing` (`character_id`) VALUES (%s)', [character_id])
        _args['mysql'].execute('INSERT INTO `inventory` (`character_id`) VALUES (%s)', [character_id])
    
    # Send the result with the status code to the client
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

def ping(server, client):

    while client in server.clients:
        pack = PacketWrite()
        pack.AddHeader([0x01, 0x00])
        pack.AppendBytes([0xCC])
        client['socket'].send(pack.packet)
        time.sleep(3)