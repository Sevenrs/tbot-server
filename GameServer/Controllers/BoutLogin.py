#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character, Shop
import MySQL.Interface as MySQL
import re

"""
This method will send the new client its unique ID
"""
def ClientIDRequest(**_args):
    
    # Read account name from packet
    account = _args['packet'].ReadString()
    
    # Get available ID
    id = len(_args['server'].clients) + 1
    
    # Contruct packet and send it back to the client
    response = PacketWrite()
    response.AddHeader(bytearray([0xE0, 0x2E]))
    
    # Add connection ID and send the packet to the client
    response.AppendInteger(id, 2, 'little')
    response.AppendBytes([0x01, 0x00])
    
    _args['socket'].send(response.packet)

    print(_args['socket'])
    
    # Update our socket to use this ID and assign the account to it as well
    _args['client']['id']       = id
    _args['client']['account']  = account
    _args['client']['new']      = 1
    
    # Disconnect all connected sessions with this account name (to stop two or more clients with the same account)
    for session in _args['connection_handler'].GetClients():
        if session['account'] == account and session['socket'] is not _args['socket']:
            _args['connection_handler'].UpdatePlayerStatus(session, 2)
    
    # Add new connection to server client container
    _args['server'].clients.append(_args['client'])
    
"""
This method will obtain the character and return it to the client
"""
def CharacterRequest(**_args):
    print('Character request for', _args['client']['account'])
    
    # Create MySQL connection and get cursor
    connection = MySQL.GetConnection()
    cursor = connection.cursor(dictionary=True, buffered=True)
    
    # Get user from the database
    cursor.execute('SELECT `id`, `username`, `active_bot_slot` FROM `users` WHERE `username` = %s AND `banned` = 0', [
        _args['client']['account']
    ])
    
    # Get user and check if we have a result. Just disconnect the client if we do not
    user = cursor.fetchone()
    if user is None:
        raise Exception('Invalid user given in the character request')
    
    # Check if we have a bot in the active slot (or have a character, at all)
    cursor.execute("""SELECT `character`.* FROM `characters` `character` WHERE character.user_id = %s
                    ORDER BY `character`.`id` ASC LIMIT 1 OFFSET %s""", [
        user['id'],
        user['active_bot_slot']
    ])
    
    # Fetch character row
    character = cursor.fetchone()
    
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
        
        # Success status of 0x01 (true)
        character_information.AppendBytes([0x01, 0x00])

        # Obtain wearing items
        wearing_items = Character.get_items(_args, character['id'], 'wearing')
        
        # Append general character information to packet
        character_information.AppendString(character['name'], 15)
        character_information.AppendInteger(character['type'], 2, 'little')
        character_information.AppendInteger(character['experience'], 4, 'little')
        character_information.AppendInteger(character['level'], 2, 'little')
        character_information.AppendInteger(character['health']
                                            + wearing_items['specifications']['effect_health'], 2, 'little')
        character_information.AppendInteger(character['att_min']
                                            + wearing_items['specifications']['effect_att_min'], 2, 'little')
        character_information.AppendInteger(character['att_max']
                                            + wearing_items['specifications']['effect_att_max'], 2, 'little')
        character_information.AppendInteger(character['att_trans_min']
                                            + wearing_items['specifications']['effect_att_trans_min'], 2, 'little')
        character_information.AppendInteger(character['att_trans_max']
                                            + wearing_items['specifications']['effect_att_trans_max'], 2, 'little')
        
        character_information.AppendBytes([0x00, 0x00])

        # Append character effects to the packet
        character_information.AppendInteger(character['trans_guage']
                                            + wearing_items['specifications']['effect_trans_guage'], 2, 'little')
        character_information.AppendInteger(character['att_critical']
                                            + wearing_items['specifications']['effect_critical'], 2, 'little')
        character_information.AppendInteger(character['att_evade']
                                            + wearing_items['specifications']['effect_critical'], 2, 'little')
        character_information.AppendInteger(character['trans_special']
                                            + wearing_items['specifications']['effect_special_trans'], 2, 'little')
        character_information.AppendInteger(character['speed']
                                            + wearing_items['specifications']['effect_speed'], 2, 'little')
        character_information.AppendInteger(character['trans_def']
                                            + wearing_items['specifications']['effect_trans_bot_defense'], 2, 'little')
        character_information.AppendInteger(character['trans_att']
                                            + wearing_items['specifications']['effect_trans_bot_attack'], 2, 'little')
        character_information.AppendInteger(character['trans_speed']
                                            + wearing_items['specifications']['effect_trans_speed'], 2, 'little')
        character_information.AppendInteger(character['att_ranged']
                                            + wearing_items['specifications']['effect_ranged_attack'], 2, 'little')
        character_information.AppendInteger(character['luck']
                                            + wearing_items['specifications']['effect_luck'], 2, 'little')

        # Append the amount of botstract to the packet
        character_information.AppendInteger(character['currency_botstract'], 4, 'little')
        
        for i in range(4):
            character_information.AppendBytes([0x00, 0x00, 0x00, 0x00])

        for i in range(0, 3):
            item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
            character_information.AppendInteger(item['id'], 4, 'little')
            character_information.AppendInteger(item['duration'], 4, 'little')
            character_information.AppendInteger(item['duration_type'], 1, 'little')
            
        character_information.AppendBytes([0x01, 0x00, 0x00])

        inventory = Character.get_items(_args, character['id'], 'inventory')
        for item in inventory:
            character_information.AppendInteger(inventory[item]['id'], 4, 'little')
            character_information.AppendInteger(inventory[item]['duration'], 4, 'little')
            character_information.AppendInteger(inventory[item]['duration_type'], 1, 'little')

        for i in range(904):
            character_information.AppendBytes([0x00])
        
        # Gigas
        character_information.AppendInteger(character['currency_gigas'], 4, 'little')
        
        for i in range(242):
            character_information.AppendBytes([0x00])

        for i in range(3, 17):
            item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
            character_information.AppendInteger(item['id'], 4, 'little')
            character_information.AppendInteger(item['duration'], 4, 'little')
            character_information.AppendInteger(item['duration_type'], 1, 'little')
            
        for i in range(200):
            character_information.AppendBytes([0x00])
        
        for i in range(2):
            character_information.AppendInteger(0, 4, 'little')
            character_information.AppendInteger(0, 4, 'little')
            character_information.AppendInteger(0, 1, 'little')
            
        for i in range(30):
            character_information.AppendBytes([0x00])
            
        character_information.AppendInteger(2, 1, 'little')
        
        for i in range(50):
            character_information.AppendInteger(0, 4, 'little')
            character_information.AppendInteger(0, 4, 'little')
            character_information.AppendInteger(0, 1, 'little')
            
        for i in range(27):
            character_information.AppendBytes([0x00, 0x00, 0x00, 0x00])
            
        character_information.AppendInteger(character['rank_exp'], 4, 'little')
        character_information.AppendInteger(character['rank'], 4, 'little')
    
        _args['socket'].send(character_information.packet)
        
    connection.close()

"""
This method will handle new character creation requests
"""
def CreateCharacterRequest(**_args):
    
    # Character creation results
    CHARACTER_CREATE_SUCCESS      = bytearray([0x01, 0x00])
    CHARACTER_CREATE_NAME_TAKEN   = bytearray([0x00, 0x36])
    CHARACTER_CREATE_NAME_ERROR   = bytearray([0x00, 0x33])
    
    character_type  = int(_args['packet'].GetByte(2))
    username        = _args['packet'].ReadString(6)[1:]
    character_name  = _args['packet'].ReadString()
    
    print("Username", username)
    print("Character", character_name)
    
    # Create MySQL connection and get cursor
    connection = MySQL.GetConnection()
    cursor = connection.cursor(dictionary=True, buffered=True)
    
    # Check if the username exists in the user table, close the connection if this fails
    cursor.execute('SELECT `id`, `banned` FROM `users` WHERE `username` = %s', [username])
    user = cursor.fetchone()
    
    # Check if the row has been found and if it has been, check if the user has been banned
    if user is None:
        raise Exception('User was not found while trying to create a character')
    
    # Check if the user has been banned
    elif user['banned'] == 1:
        raise Exception('User has been banned and attempted to create a character')
    
    # Check if there's already a character connected to this account
    cursor.execute('SELECT `id` FROM `characters` WHERE `user_id` = %s', [user['id']])
    if cursor.rowcount > 2:
        raise Exception('User attempted to create a character while already having the maximum amount of allowed characters')
    
    # Check the character type is between 1 and 3
    elif character_type < 1 or character_type > 3:
        raise Exception('User sent an invalid character type')
    
    #TODO: [Close connection] - Check if we're authorized to create a character for this username
    
    # Create a new packet with the character creation result command
    packet = PacketWrite()
    packet.AddHeader(bytearray([0xE2, 0x2E]))
    
    # Check if the name has been taken
    cursor.execute('SELECT `id` FROM `characters` WHERE `name` = %s', [character_name])
    if cursor.rowcount > 0:
        packet.AppendBytes(CHARACTER_CREATE_NAME_TAKEN)
    elif not re.match('^[a-zA-Z0-9]+$', character_name) or len(character_name) < 4 or len(character_name) > 13:
        packet.AppendBytes(CHARACTER_CREATE_NAME_ERROR)
    else:
        packet.AppendBytes(CHARACTER_CREATE_SUCCESS)
        
        # Insert the new character in the database
        cursor.execute('INSERT INTO `characters` (`user_id`, `name`, `type`) VALUES (%s, %s, %s)',
                       [user['id'], character_name, character_type])
    
    # Send the result with the status code to the client
    _args['socket'].send(packet.packet)

"""
This method will handle exit server requests
"""
def ExitServerRequest(**_args):
    
    # Send acknowledgement to the client
    exit = PacketWrite()
    exit.AddHeader(bytearray([0x0A, 0x2F]))
    exit.AppendBytes(bytearray([0x01, 0x00]))
    _args['socket'].send(exit.packet)
    
    # Disconnect the client, in case the connection is still alive
    _args['connection_handler'].UpdatePlayerStatus(_args['client'], 2)

