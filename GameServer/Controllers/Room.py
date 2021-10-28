#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character, Guild, Lobby
from GameServer.Controllers.data.planet import PLANET_MAP_TABLE
from GameServer.Controllers.data.deathmatch import DEATHMATCH_MAP_TABLE
from GameServer.Controllers.data.battle import BATTLE_MAP_TABLE
from GameServer.Controllers.data.military import MILITARY_MAP_TABLE
from GameServer.Controllers.data.game import *
from GameServer.Controllers.Game import game_end, load_finish, load_finish_thread
import math, os, time, datetime, _thread
from random import randrange

"""
This controller is responsible for handling all room related requests
"""

def get_list_page_by_room_id(room_id, game_mode):
    return int(math.floor((room_id - (0 if game_mode == 1 else game_mode * 600)) / 6.0))

def get_list(_args, mode=2, page=0, local=True):

    # Calculate mode to the mode used in room storage
    if mode > 0: mode = mode + 1

    rooms = []

    # Get rooms in the range
    start_range = (mode * 600 + (page * 6))

    for i in range(start_range, (start_range + 6)):
        if str(i) in _args['server'].rooms:
            rooms.append(_args['server'].rooms[str(i)])
        else:
            rooms.append(None)

    result = PacketWrite()
    result.AddHeader(bytearray([0xEF, 0x2E]))
    result.AppendBytes(bytearray([0x01, 0x00]))
    for room in rooms:
        if room is None:
            for _ in range(50):
                result.AppendBytes(bytearray([0x00]))
        else:
            result.AppendInteger((room['client_id'] + 1), 2, 'little')
            result.AppendString(room['name'], 27)
            if len(room['password']) == 0:
                for _ in range(11):
                    result.AppendBytes(bytearray([0x00]))
            else:
                result.AppendString('hidden', 11)
            result.AppendInteger(room['game_type'], 1, 'little')
            result.AppendBytes(bytearray([0x08]))                   # Unknown
            result.AppendInteger(room['status'], 1, 'little')
            result.AppendInteger(room['master']['character']['level'], 2, 'little')
            result.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00, 0x00]))

    # If our own client is requesting the list, send the list to our client only.
    if local:
        _args['client']['lobby_data'] = {'mode': mode, 'page': page}
        print(_args['client']['lobby_data'])
        _args['socket'].send(result.packet)

    # Otherwise, send the room list to all sockets in the lobby and those able to see this specific room
    else:
        for client in _args['server'].clients:

            # Check if the client is not in a room and if the client is able to see this change at all
            if 'room' not in client and client['lobby_data'] == {'mode': mode, 'page': page}:
                try:
                    client['socket'].send(result.packet)
                except Exception:
                    pass

"""
This method will get the first free room id
"""
def get_available_room_number(_args, game_type):

    # If the type is team battle, we need to use game_type 0 instead
    if game_type == 1:
        game_type = 0

    # Simply do type times 600 (every mode can contain 600 rooms)
    base_number = game_type * 600

    # Loop through the rooms and find the first available room ID
    for i in range(base_number, base_number + 600):
        if str(i) in _args['server'].rooms:
            continue
        else:
            client_room_id = i

            # Calculate the ID that the client sees
            if game_type == 2 or game_type == 3:
                client_room_id = (client_room_id - 600)
            elif game_type == 4:
                client_room_id = (client_room_id - 900)

            return {
                "slot": i,
                "client_id": client_room_id
            }

def construct_room_players(_args, packet, character, slot_num, client, room):

    # Send character level
    packet.AppendInteger(character['level'], 2, 'little')

    # Obtain wearing items
    wearing_items = Character.get_items(_args, character['id'], 'wearing')

    for i in range(19):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        packet.AppendInteger(item['id'], 4, 'little')

    # unknown, but needed
    packet.AppendInteger(2, 2, 'big')

    # Room number
    packet.AppendInteger(room['client_id'] + 1, 2, 'little')

    # Split IP address so we can append it in a packet
    p2p_ip = client['socket'].getpeername()[0].split('.')

    # Peer IP address
    for number in p2p_ip:
        packet.AppendInteger(int(number))

    for _ in range(10):
        packet.AppendBytes(bytearray([0x00]))

    # Peer port
    if 'p2p_host' in client:
       packet.AppendInteger(client['p2p_host']['port'], 2, 'little')
    else:
       packet.AppendInteger(0, 2, 'little')

    # Peer IP address
    for number in p2p_ip:
        packet.AppendInteger(int(number), 1)

    for _ in range(4):
        packet.AppendBytes(bytearray([0x00]))

    # Team
    team = room['slots'][str(slot_num)]['team']
    packet.AppendBytes([0x74 if team == 1 else 0x78 if team == 2 else 0x00, 0x00])

    for _ in range(4):
            packet.AppendBytes(bytearray([0x00]))

    if room['master'] is client:
        packet.AppendBytes(bytearray([0x70]))
    else:
        packet.AppendBytes(bytearray([0x50]))

    for _ in range(21):
        packet.AppendBytes(bytearray([0x00]))

    packet.AppendInteger(character['att_min'] + wearing_items['specifications']['effect_att_min'], 2, 'little')
    packet.AppendInteger(character['att_max'] + wearing_items['specifications']['effect_att_max'], 2, 'little')
    packet.AppendInteger(character['att_trans_min'] + wearing_items['specifications']['effect_att_trans_min'], 2,
                       'little')
    packet.AppendInteger(character['att_trans_max'] + wearing_items['specifications']['effect_att_trans_max'], 2,
                       'little')
    packet.AppendInteger(character['health'] + wearing_items['specifications']['effect_health'], 2, 'little')

    # Defense
    packet.AppendInteger(512, 2, 'little')

    packet.AppendInteger(character['trans_guage'] + wearing_items['specifications']['effect_trans_guage'], 2, 'little')
    packet.AppendInteger(character['att_critical'] + wearing_items['specifications']['effect_critical'], 2, 'little')
    packet.AppendInteger(character['att_evade'] + wearing_items['specifications']['effect_critical'], 2, 'little')
    packet.AppendInteger(character['trans_special'] + wearing_items['specifications']['effect_special_trans'], 2,
                       'little')
    packet.AppendInteger(character['speed'] + wearing_items['specifications']['effect_speed'], 2, 'little')
    packet.AppendInteger(character['trans_def'] + wearing_items['specifications']['effect_trans_bot_defense'], 2,
                       'little')
    packet.AppendInteger(character['trans_att'] + wearing_items['specifications']['effect_trans_bot_attack'], 2, 'little')
    packet.AppendInteger(character['trans_speed'] + wearing_items['specifications']['effect_trans_speed'], 2, 'little')
    packet.AppendInteger(character['att_ranged'] + wearing_items['specifications']['effect_ranged_attack'], 2, 'little')
    packet.AppendInteger(character['luck'] + wearing_items['specifications']['effect_luck'], 2, 'little')

    packet.AppendInteger(character['type'], 2, 'little')

    packet.AppendInteger(slot_num - 1)

    for _ in range(4):
        packet.AppendBytes(bytearray([0x00]))

    packet.AppendString(character['name'], 15)

    # Fetch character guild membership and get the name of the guild
    guild = Guild.FetchGuild(_args, character['id'])
    packet.AppendString('' if guild is None else guild['name'], 21)

    for _ in range(4):
        packet.AppendBytes(bytearray([0x00]))

    packet.AppendInteger(character['rank'], 2, 'little')
    for _ in range(6):
        packet.AppendBytes(bytearray([0x00]))

def add_slot(_args, room_id, client, broadcast=False):

    # Find room
    room = _args['server'].rooms[str(room_id)]

    # Construct packet that will be sent to our client if we are joining a room
    room_info = PacketWrite()
    room_info.AddHeader([0x28, 0x2F])

    # Attempt to get the first available slot number
    available_slot = 0
    for i in range(1, 9):
        if str(i) not in room['slots'] and i not in room['closed_slots']:
            available_slot = i
            break

    # Append to slots if the available slot is greater than 0
    if available_slot > 0:
        room['slots'][str(available_slot)] = {
            'client':                   client,
            'loaded':                   False,
            'dead':                     False,
            'won':                      False,
            'ready':                    False,
            'shop':                     False,
            'team':                     (randrange(1, 3) if available_slot > 1 else 1)  # If the slot number is 1, the client needs to be red team no matter what.
                                            if room['game_type'] in [1, 3] else 0, # If the game mode is either team Battle or Military, assign a team to the current slot
            'in_shop':                  False,
            'file_validation_passed':   False,
            'monster_kills':            0,
            'player_kills':             0,
            'deaths':                   0,
            'points':                   0,
            'relay_ids':                []
        }

        # Set room id for current client to indicate that our client is in a room
        _args['client']['room'] = room['id']

        # Update player status to be in room
        _args['connection_handler'].UpdatePlayerStatus(client, 0)

    # Tell all the sockets about the player and tell our client about the room
    if broadcast:

        # If the available slot is not greater than 0, tell our client that the room is full and stop the process
        if available_slot < 1:
            room_info.AppendBytes([0x00, 0x51])
            client['socket'].send(room_info.packet)
            return

        # Tell our client about the room and its players
        room_info.AppendBytes([0x01, 0x00])

        # Loop through all players in the room
        for i in range(0, 8):

            # Get slot and character
            if str((i + 1)) in room['slots']:
                remote_client = room['slots'][str((i + 1))]['client']
                character = remote_client['character']
                construct_room_players(_args, room_info, character, (i + 1), remote_client, room)
            else:
                for _ in range(221):
                    room_info.AppendBytes([0x00])

        room_info.AppendInteger(room['client_id'] + 1, 2, 'little')
        room_info.AppendString(room['name'], 27)
        room_info.AppendString(room['password'], 11)
        room_info.AppendInteger(room['game_type'], 1)
        for _ in range(9):
            room_info.AppendBytes([0x00])

        # Find room master slot number and append it to the packet
        for key, slot in room['slots'].items():
            if slot['client'] is room['master']:
                room_info.AppendInteger(int(key) - 1, 1, 'little')

        # DeathMatch countdown times
        if room['game_type'] == 4:

            # Array containing the amount of seconds
            countdown_times = [
                [0xB4, 0x00], # 3 minutes
                [0x2C, 0x01]  # 5 minutes
            ]

            room_info.AppendBytes(countdown_times[room['time']])

        # Notify our client about the room
        client['socket'].send(room_info.packet)

        # Define the slot and character for easy access
        slot = room['slots'][str(available_slot)]
        character = slot['client']['character']

        # Tell all the players in the room about the new player
        join = PacketWrite()
        join.AddHeader([0x29, 0x27])
        construct_room_players(_args, join, character, available_slot, client, room)
        _args['connection_handler'].SendRoomAll(room['id'], join.packet)

    # Send a message to the client about the commands they can use
    Lobby.ChatMessage(_args['client'], 'There are commands available. Type @help for a list of commands.', 2)

'''
This method will remove a player from the room
'''
def remove_slot(_args, room_id, client, reason=1):

    # Find room
    room = _args['server'].rooms[str(room_id)]

    # Find our slot and remove it from the room
    for key, slot in room['slots'].items():
        if slot['client'] is client:

            # Remove slot from the room
            del room['slots'][key]

            # If we are the room master, re-assign the room master to the first available slot
            if slot['client'] is room['master']:
                for k, s in sorted(room['slots'].items()):
                    room['master'] = s['client']
                    break

            # Construct exit packet
            exit = PacketWrite()
            exit.AddHeader(bytearray([0x2E, 0x27]))
            exit.AppendBytes(bytearray([0x01, 0x00]))       # Success status
            exit.AppendInteger(int(key) - 1, 1, 'little')   # Slot number
            exit.AppendInteger(reason, 1, 'little')         # Change ID

            # Construct ranks
            for i in range(1, 9):
                if str(i) in room['slots']:
                    exit.AppendBytes([0x70] if room['slots'][str(i)]['client'] is room['master'] else [0x50])
                else:
                    exit.AppendBytes([0x00])
                exit.AppendBytes([0x00])

            _args['connection_handler'].SendRoomAll(room['id'], exit.packet)

            # Remove the room from the client so the client is no longer in the room
            client.pop('room')

            # If the reason is not equal to 6 (forced to log out), update the player status to not be in a room
            if reason != 6:
                _args['connection_handler'].UpdatePlayerStatus(client, 1)

            # Remove peer information as we most likely need to assign new information later
            if 'p2p_host' in client:
                client.pop('p2p_host')

            # Ensure the relay ID of this client is removed from the relay ID array of everyone else in the room
            if 'relay_client' in client:
                relay_id = client['relay_client']['id']
                for k, s in room['slots'].items():
                    if relay_id in s['relay_ids']:
                        s['relay_ids'].remove(relay_id)
            break

    # If the room has no more slots left, delete the room and send the new room list to the lobby
    if len(room['slots']) == 0:
        del _args['server'].rooms[str(room_id)]
        get_list(_args, mode=0 if room['game_type'] in [0, 1] else room['game_type'] - 1,
                 page=get_list_page_by_room_id(room['id'], room['game_type']), local=False)
    else:
        sync_state(_args, room)

"""
This method will create a new room by creating a new room instance and having it in the room container
"""
def create(**_args):

    # Check if our current client is already in a room
    if 'room' in _args['client']:
        return

    # Retrieve all information from the packet
    name        = _args['packet'].ReadStringByRange(0, 27)
    password    = _args['packet'].ReadStringByRange(27, 38)
    game_type   = _args['packet'].GetByte(39)
    time        = _args['packet'].GetByte(41)

    # Retrieve available room number
    room_ids = get_available_room_number(_args, game_type)

    # Retrieve our map table based on the game type
    maps = {
        0: BATTLE_MAP_TABLE,
        1: BATTLE_MAP_TABLE, # Team Battle
        2: PLANET_MAP_TABLE,
        3: MILITARY_MAP_TABLE,
        4: DEATHMATCH_MAP_TABLE
    }.get(game_type, PLANET_MAP_TABLE)

    # Store room in the room container
    room = {
        'slots':                {},
        'closed_slots':         [],
        'name':                 name,
        'password':             password,
        'game_type':            game_type,
        'time':                 time,
        'id':                   room_ids['slot'],
        'client_id':            room_ids['client_id'],
        'master':               _args['client'],
        'level':                0,
        'difficulty':           0,
        'status':               0,
        'drop_index':           1,
        'drops':                {},
        'game_over':            False,
        'game_loaded':          False,
        'experience_modifier':  1.0,
        'maps':                 maps,
        'killed_mobs':          [],
        'network_state_requests': {},
        'start_time':             None
    }

    # Pass the room to the server room container and notify any client that may see this change in the lobby
    _args['server'].rooms[str(room_ids['slot'])] = room
    get_list(_args, mode=0 if room['game_type'] in [0, 1] else room['game_type'] - 1,
             page=get_list_page_by_room_id(room['id'], room['game_type']), local=False)

    # Add ourselves to slots
    add_slot(_args, room_ids['slot'], _args['client'])

    # Send room information to our own client
    room = PacketWrite()
    room.AddHeader(bytearray([0xEE, 0x2E]))
    room.AppendBytes(bytearray([0x01, 0x00]))
    room.AppendInteger(room_ids['client_id'] + 1, 2, 'little')

    local_address = _args['socket'].getpeername()[0].split('.')
    for number in local_address:
        room.AppendInteger(int(number))

    _args['socket'].send(room.packet)

'''
This method will handle quick join requests
'''
def quick_join(**_args):

    # Check if our current client is already in a room
    if 'room' in _args['client']:
        return

    # Retrieve mode from our client
    mode = _args['client']['lobby_data']['mode']

    # Calculate room range based on the mode
    start_range = mode * 600

    # Attempt to join 600 rooms for the mode we are currently in
    for i in range(start_range, (start_range + 600)):

        # If a room was not found, skip the iteration
        if not str(i) in _args['server'].rooms:
            continue

        # Retrieve the room from the room container
        room = _args['server'].rooms[str(i)]

        # If the room is full, has a password or has started, skip the iteration
        if (len(room['slots']) + len(room['closed_slots'])) >= 8 or len(room['password']) > 0 or room['status'] != 0:
            continue

        # If we have passed all the checks, we can join the room
        add_slot(_args, room['id'], _args['client'], True)
        sync_state(_args, room)
        return

    # If we have no results, create our own room instead
    create_room = PacketWrite()
    create_room.AddHeader([0x28, 0x2F])
    create_room.AppendBytes([0x00, 0x3A])
    _args['socket'].send(create_room.packet)

"""
This method will set the level for the room
"""
def set_level(**_args):

    # Check if we are in a room
    if 'room' not in _args['client']:
        return

    # Get room from ID
    room = _args['server'].rooms[str(_args['client']['room'])]

    # Check if we are the room master
    if room['master']['id'] != _args['client']['id']:
        return

    # Read level from the incoming packet
    selected_level = int(_args['packet'].GetByte(2))

    # Check if the selected level is in our map table
    if selected_level not in room['maps']:
        selected_level = 0

        # Create error packet for the room master to tell them that their request has been denied
        error = PacketWrite()
        error.AddHeader(bytearray([0xF3, 0x2E]))
        error.AppendBytes(bytearray([0x00, 0x3D]))
        _args['socket'].send(error.packet)

    # Set level for the room and broadcast to all clients in this room
    room['level'] = selected_level

    # Construct level packet
    level = PacketWrite()
    level.AddHeader(bytearray([0x4A, 0x2F]))
    level.AppendBytes(bytearray([0x01, 0x00]))
    level.AppendInteger(selected_level, 2, 'little')
    _args['connection_handler'].SendRoomAll(_args['client']['room'], level.packet)


def set_difficulty(**_args):

    # Check if we are in a room
    if 'room' not in _args['client']:
        return

    # Get room from ID
    room = _args['server'].rooms[str(_args['client']['room'])]

    # Check if we are the room master
    if room['master']['id'] != _args['client']['id']:
        return

    # Read difficulty from the incoming packet
    new_difficulty = int(_args['packet'].GetByte(2))
    room['difficulty'] = new_difficulty

    result = PacketWrite()
    result.AddHeader(bytearray([0x62, 0x2F]))
    result.AppendBytes(bytearray([0x01, 0x00]))
    result.AppendInteger(new_difficulty, 2, 'little')
    _args['connection_handler'].SendRoomAll(_args['client']['room'], result.packet)

'''
This method allows users to change their status
'''
def set_status(**_args):

    # Retrieve the room should be in
    room = get_room(_args)
    if not room:
        return

    # Get our own slot number
    slot = get_slot(_args, room)

    # Read status type from the packet
    status_type = int(_args['packet'].ReadInteger(6, 2, 'big'))

    if status_type == 0 and room['master'] is _args['client']:

        # Retrieve the target slot number from the packet
        target_slot = int(_args['packet'].ReadInteger(3, 1, 'little')) + 1

        # Check if the target slot is empty and check if the slot is equal to our own slot
        if str(target_slot) in room['slots'] or target_slot == slot:
            return

        # Overwrite our slot with the target slot number for further operations
        slot = target_slot

        # Append to or remove from the room's closed slots
        if not slot in room['closed_slots']:
            room['closed_slots'].append(slot)
        else:
            room['closed_slots'].remove(slot)

    # Handle ready requests
    elif status_type == 1:
        room['slots'][str(slot)]['ready'] = not room['slots'][str(slot)]['ready']

    # Handle team change requests
    elif status_type == 2 and room['game_type'] in [MODE_TEAM_BATTLE, MODE_MILITARY]:
        room['slots'][str(slot)]['team'] = 1 if room['slots'][str(slot)]['team'] == 2 else 2

    # Broadcast the status change to the room
    status = PacketWrite()
    status.AddHeader(bytearray([0x20, 0x2F]))
    status.AppendInteger(slot - 1, 2, 'little')
    status.AppendBytes(bytearray([0x00, 0x00]))
    status.AppendInteger(1 if slot in room['closed_slots'] else 0, 2, 'little')
    status.AppendInteger(room['slots'][str(slot)]['ready'] if str(slot) in room['slots'] else 0, 2, 'little')
    status.AppendInteger(room['slots'][str(slot)]['team'] if str(slot) in room['slots'] else 0, 2, 'little')
    _args['connection_handler'].SendRoomAll(_args['client']['room'], status.packet)

'''
This method allows users to enter the shop. This will notify any other client in the room of that status as well
'''
def enter_shop(**_args):

    # Get room and check if we are actually in a room
    room = get_room(_args)
    if not room:
        return

    # Retrieve our slot number
    slot = get_slot(_args, room)

    # Construct enter shop packet
    result = PacketWrite()
    result.AddHeader(bytearray([0x60, 0x2F]))
    result.AppendBytes(bytearray([0x01, 0x00]))
    result.AppendInteger(slot - 1, 2, 'little')
    room['slots'][str(slot)]['in_shop'] = True
    _args['connection_handler'].SendRoomAll(_args['client']['room'], result.packet)

    # If the slot is ready, change it to become unready and send a slot update
    if room['slots'][str(slot)]['ready']:
        room['slots'][str(slot)]['ready'] = False

        # Construct slot update packet
        status = PacketWrite()
        status.AddHeader(bytearray([0x20, 0x2F]))
        status.AppendInteger(slot - 1, 2, 'little')
        status.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00]))
        status.AppendInteger(room['slots'][str(slot)]['ready'], 2, 'little')
        status.AppendInteger(room['slots'][str(slot)]['team'], 2, 'little')
        _args['connection_handler'].SendRoomAll(_args['client']['room'], status.packet)

'''
This method allows users to exit the shop. This will notify all the other clients of the new character state as well
'''
def exit_shop(**_args):

    # Get room and check if we are inside of a room
    room = get_room(_args)
    if not room:
        return

    # Get our slot number
    slot = get_slot(_args, room)

    # Construct exit shop packet
    result = PacketWrite()
    result.AddHeader(bytearray([0x61, 0x2F]))
    result.AppendBytes(bytearray([0x01, 0x00]))
    result.AppendInteger(slot - 1, 2, 'little')
    result.AppendBytes(bytearray([0x00, 0x00]))

    result.AppendInteger(_args['client']['id'], 2, 'little')

    wearing_items = Character.get_items(_args, _args['client']['character']['id'], 'wearing')
    for i in range(19):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        result.AppendInteger(item['id'], 4, 'little')

    room['slots'][str(slot)]['in_shop'] = False
    _args['connection_handler'].SendRoomAll(_args['client']['room'], result.packet)

"""
This method will start the game
"""
def start_game(**_args):

    # Get room and check if we are the room master
    room = get_room(_args, True)
    if not room:
        return

    # Create start packet which will be used for errors
    start = PacketWrite()
    start.AddHeader(bytearray([0xF3, 0x2E]))

    # If we are in Battle or Deathmatch mode, we'll have to check if we have more than one player
    if room['game_type'] in [MODE_BATTLE, MODE_DEATHMATCH] and len(room['slots']) < 2:
        start.AppendBytes([0x00, 0x50])
        return _args['client']['socket'].send(start.packet)

    # If we are in a game mode that relies on teams, check if each team has at least one player available
    elif room['game_type'] in [MODE_TEAM_BATTLE, MODE_MILITARY]:

        # Retrieve how many players each team has
        team_players = { TEAM_RED: 0, TEAM_BLUE: 0 }
        for slot in room['slots']:
            team_players[room['slots'][slot]['team']] += 1

        # Check if one team has no players
        for team in team_players:
            if team_players[team] == 0:
                start.AppendBytes([0x00, 0x6F])
                return _args['client']['socket'].send(start.packet)

    # Check if everyone is ready
    for key, slot in room['slots'].items():
        if not slot['ready'] and slot['client']['id'] != room['master']['id'] and int(_args['client']['character']['position']) != 1:
            start.AppendBytes(bytearray([0x00, 0x6C]))
            return _args['client']['socket'].send(start.packet)

    # If the game mode is not equal to planet, determine if we should randomize the map or not
    map = room['level']
    if room['game_type'] != 2:
        map = int(map) - 1 if map > 0 else randrange(0, len(room['maps']) - 1)

    # Construct start packet and send to entire room
    start = PacketWrite()
    start.AddHeader(bytearray([0xF3, 0x2E]))

    # Finish start packet and broadcast to room
    start.AppendBytes(bytearray([0x01, 0x00]))
    start.AppendInteger(room['client_id'] + 1, 2, 'little')
    start.AppendInteger(map, 2, 'little')
    start.AppendInteger(room['game_type'], 1)

    start.AppendInteger(0, 2, 'little')  # Start X
    start.AppendInteger(0, 2, 'little')  # Start Z
    start.AppendBytes([0x00])  # Start direction

    # Calculate special transformation
    special_transformation = randrange(5)
    start.AppendInteger(special_transformation, 1, 'little')
    start.AppendBytes([0x00])  # Event boss

    for _ in range(2):
        start.AppendBytes(bytearray([0x00, 0x00]))

    # Send start packet to entire room
    _args['connection_handler'].SendRoomAll(_args['client']['room'], start.packet)
    _args['connection_handler'].SendRoomAll(_args['client']['room'], bytearray([0x28, 0x27, 0x02, 0x00, 0x01, 0x00]))

    # Determine whether or not it is weekend. Based on that result, a 1.5x experience buff will be enabled
    # Additionally, this will only be in effect in planet gameplay
    room['experience_modifier'] = 1.0 if not datetime.datetime.today().weekday() >= 5 or \
                                         room['game_type'] != 2 else 1.5

    _args['connection_handler'].SendRoomAll(room['id'], bytearray(
        [0x28, 0x27, 0x02, 0x00, 0x01 if room['experience_modifier'] > 1.0 else 0x00, 0x00]))

    # Set room status
    room['status'] = 3
    room['start_time'] = datetime.datetime.now()
    get_list(_args, mode=0 if room['game_type'] in [0, 1] else room['game_type'] - 1,
             page=get_list_page_by_room_id(room['id'], room['game_type']), local=False)

    # Start load_finish_thread to check clients' loaded status in the background without relying on the RPCs
    _thread.start_new_thread(load_finish_thread, (_args, room,))

'''
This method will reset the room by making sure nobody is ready anymore, drops are set back at their standard
values, etc.
'''
def reset(room):

    # Reset room variables
    room['drop_index']              = 1
    room['game_over']               = False
    room['game_loaded']             = False
    room['killed_mobs']             = []
    room['network_state_requests']  = {}
    room['start_time']              = None

    # Reset player status
    for slot in room['slots']:
        slot = room['slots'][slot]
        slot['ready']                   = 0
        slot['in_shop']                 = False
        slot['loaded']                  = False
        slot['dead']                    = False
        slot['won']                     = False
        slot['file_validation_passed']  = False
        slot['monster_kills']           = 0
        slot['player_kills']            = 0
        slot['deaths']                  = 0
        slot['points']                  = 0

'''
This method allows room masters to kick players out of their rooms
'''
def kick_player(**_args):

    # Obtain room. If we are not in a room, drop the packet entirely
    room = get_room(_args)
    if not room:
        return

    # In the event we need to send an error packet, construct it here
    error = PacketWrite()
    error.AddHeader(bytearray([0xF3, 0x2E]))

    # If we are not the room master, send an error packet that does nothing so that the client will not lock up
    if room['master']['id'] != _args['client']['id']:
        error.AppendBytes(bytearray([0x00, 0x3A]))
        return _args['client']['socket'].send(error.packet)

    # Read slot number from the packet
    slot = int(_args['packet'].ReadInteger(18, 1, 'little'))

    # Stop the room master from kicking themselves
    if slot + 1 == get_slot(_args, room):
        error.AppendBytes(bytearray([0x00, 0x73]))
        return _args['client']['socket'].send(error.packet)

    # Read slot number and remove player from the room
    if str(slot +1) in room['slots']:
        remove_slot(_args=_args, room_id=room['id'], client=room['slots'][str(slot + 1)]['client'], reason=2)

'''
This method allows users to exit a room
'''
def exit_room(**_args):

    # Check if we are in a room
    if 'room' not in _args['client']:
        return

    remove_slot(_args, _args['client']['room'], _args['client'])

'''
This method allows the room master to change the room's password
'''
def change_password(**_args):

    # Get room. Drop packet if we are not its master or if we are not in a room
    room = get_room(_args, master=True)
    if not room:
        return

    # Read the new password (and account name, which we won't be using)
    account = _args['packet'].ReadString(2)
    password = _args['packet'].ReadString()

    # If the room does not have a password, drop the packet. Also drop the packet if the new password's length is 0.
    if len(room['password']) == 0 or len(password) not in range(1, 11):
        return

    # Update room password
    room['password'] = password

    # Construct success packet and send to socket
    result = PacketWrite()
    result.AddHeader([0x38, 0x2F])
    result.AppendBytes([0x01, 0x00])
    result.AppendString(password, 10)

    _args['socket'].send(result.packet)



'''
This method allows players to join rooms
'''
def join_room(**_args):

    # If we are in a room, drop the packet
    room = get_room(_args)
    if room:
        return

    # Read information from join packet
    room_client_id  = int(_args['packet'].ReadInteger(1, 2, 'little')) - 1
    room_password   = _args['packet'].ReadStringByRange(29, 40)

    # Find room and join the room
    for key in _args['server'].rooms:
        room = _args['server'].rooms[key]

        if room['client_id'] == room_client_id:

            # Construct room join result
            join_result = PacketWrite()
            join_result.AddHeader([0x28, 0x2F])

            # If the room has a password, check if the entered password is correct
            if len(room['password']) > 0 and room['password'] != room_password and _args['client']['character']['position'] == 0:
                join_result.AppendBytes([0x00, 0x3E])
                return _args['client']['socket'].send(join_result.packet)

            # Check if the game has started
            if room['status'] == 3:
                join_result.AppendBytes([0x00, 0x3B])
                return _args['client']['socket'].send(join_result.packet)

            add_slot(_args, room['id'], _args['client'], True)
            sync_state(_args, room)
            break

'''
This method will sync the state for all the peers inside of it
'''
def sync_state(_args, room):

    # Sync room state if the room status is equal to 0
    if room['status'] == 0:

        # Sync the currently selected map and difficulty
        for data in [
            [0x4A, room['level']],
            [0x62, room['difficulty']],
        ]:
            packet = PacketWrite()
            packet.AddHeader(bytearray([data[0], 0x2F]))
            packet.AppendBytes(bytearray([0x01, 0x00]))
            packet.AppendInteger(data[1], 2, 'little')
            _args['connection_handler'].SendRoomAll(room['id'], packet.packet)

        # Sync player in_shop state and status
        for i in range(1, 9):

            # Send shop packet if the player is in the shop
            if str(i) in room['slots'] and room['slots'][str(i)]['in_shop']:
                shop_state = PacketWrite()
                shop_state.AddHeader(bytearray([0x60, 0x2F]))
                shop_state.AppendBytes(bytearray([0x01, 0x00]))
                shop_state.AppendInteger(i - 1, 2, 'little')
                _args['connection_handler'].SendRoomAll(room['id'], shop_state.packet)

            # Sync slot status
            status = PacketWrite()
            status.AddHeader(bytearray([0x20, 0x2F]))
            status.AppendInteger(i - 1, 2, 'little')
            status.AppendBytes(bytearray([0x00, 0x00]))
            status.AppendInteger(1 if i in room['closed_slots'] else 0, 2, 'little')
            status.AppendInteger(room['slots'][str(i)]['ready'] if str(i) in room['slots'] else 0, 2, 'little')
            status.AppendInteger(room['slots'][str(i)]['team'] if str(i) in room['slots'] else 0, 2, 'little')
            _args['connection_handler'].SendRoomAll(room['id'], status.packet)

    # If the room status is equal to 3 (started)
    elif room['status'] == 3:

        # the game has not loaded yet, check all clients' loaded state again
        if not room['game_loaded']:

            ''' Check every slot's loaded status. If they've all started then send the ready packet to the room.
                       No reason to wait for other clients that may not exist anymore. '''
            for slot in room['slots']:
                if not room['slots'][slot]['loaded']:
                    return

            # Start game if all clients have loaded
            load_finish(_args, room)

        # If we are playing DeathMatch or Battle and there are less than 2 players in the room, end the game
        if room['game_type'] in [MODE_BATTLE, MODE_DEATHMATCH] and len(room['slots']) < 2:

            # If the game type is DeathMatch, the status should be TimeOver else it should be Win
            status = 3 if room['game_type'] == 4 else 1

            game_end(_args=_args, room=room, status=status)

        # If we are playing team battle or military, check if any of the teams have 0 players left
        elif room['game_type'] in [MODE_TEAM_BATTLE, MODE_MILITARY]:

            for team in [TEAM_RED, TEAM_BLUE]:

                # Get amount of players in the team
                players = 0
                for slot in room['slots']:
                    if room['slots'][slot]['team'] == team:
                        players += 1

                # If the player count is equal to 0, end the game
                if players == 0:
                    game_end(_args=_args, room=room, status=1)
                    break




'''
This method will check if the client is in a room.
Additionally, the master flag will dictate whether or not a client should be a room master
If the client is in the room and checks were passed (if any), the room is returned to the stack
'''
def get_room(_args, master=False):

    # The client sending the packet must be in a room
    if 'room' not in _args['client']:
        return False

    # Find room
    room = _args['server'].rooms[str(_args['client']['room'])]

    # If we have to, check if our client is room master
    if master:
        if room['master']['id'] != _args['client']['id']:
            return False

    return room

'''
This method will get the slot number for our current client and return it to the stack
If the client is not assigned to any slot, we'll return False
'''
def get_slot(_args, room=None):

    # Loop through all slots to find our client
    for key, slot in room['slots'].items():
        if slot['client'] is _args['client']:
            return int(key)

    # Finally, if nothing worked return False
    return False