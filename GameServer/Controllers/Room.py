#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character, Guild
from GameServer.Controllers.data.planet import PLANET_MAP_TABLE
import math, os, time

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
            print(client['lobby_data'])
            print(client['lobby_data'] == {'mode': mode, 'page': page})
            print({'mode': mode, 'page': page})
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
    packet.AppendInteger(room['id'], 2, 'little')

    # Split IP address so we can append it in a packet
    p2p_ip = client['socket'].getpeername()[0].split('.')

    # Peer IP address
    for number in p2p_ip:
        packet.AppendInteger(int(number))

    for _ in range(10):
        packet.AppendBytes(bytearray([0x00]))

    # Peer port
    if 'p2p_host' in client and client == room['master']:
       packet.AppendInteger(client['p2p_host']['port'], 2, 'little')
    else:
       packet.AppendInteger(0, 2, 'little')

    # Peer IP address
    for number in p2p_ip:
        packet.AppendInteger(int(number), 1)

    for _ in range(10):
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

    packet.AppendInteger(0, 2, 'little')

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
            'client':           client,
            'loaded':           False,
            'dead':             False,
            'ready':            False,
            'shop':             False,
            'team':             0,
            'in_shop':          False,
            'monster_kills':    0,
            'player_kills':     0
        }

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

     # Set room id for current client to indicate that our client is in a room
    _args['client']['room'] = room['id']

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
                for k, s in room['slots'].items():
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
            client.pop('p2p_host')
            break

    # If the room has no more slots left, delete the room and send the new room list to the lobby
    if len(room['slots']) == 0:
        del _args['server'].rooms[str(room_id)]
        get_list(_args, mode=0 if room['game_type'] in [0, 1] else room['game_type'] - 1,
                 page=get_list_page_by_room_id(room['id'], room['game_type']), local=False)
    else:
        sync_state(_args, room)


"""
This method will create a new room
"""

def create(**_args):

    # Check if our current client is already in a room
    if 'room' in _args['client']:
        return

    print(_args['packet'].data)

    # Get parameters from the incoming packet
    room_name = _args['packet'].ReadStringByRange(0, 27)
    room_password = _args['packet'].ReadStringByRange(27, 38)
    room_gametype = _args['packet'].GetByte(39)
    room_time = _args['packet'].GetByte(41)
    room_ids = get_available_room_number(_args, room_gametype)

    # Store room in the room container
    room = {
        'slots':        {},
        'closed_slots': [],
        'name':         room_name,
        'password':     room_password,
        'game_type':    room_gametype,
        'time':         room_time,
        'id':           room_ids['slot'],
        'client_id':    room_ids['client_id'],
        'master':       _args['client'],
        'level':        0,
        'difficulty':   0,
        'status':       0,
        'drop_index':   1,
        'game_over':    False
    }

    # Pass the room to the server room container and notify any client that may see this change in the lobby
    _args['server'].rooms[str(room_ids['slot'])] = room
    get_list(_args, mode=0 if room['game_type'] in [0, 1] else room['game_type'] - 1,
             page=get_list_page_by_room_id(room['id'], room['game_type']), local=False)

    # Add ourselves to slots
    add_slot(_args, room_ids['slot'], _args['client'])

    room = PacketWrite()
    room.AddHeader(bytearray([0xEE, 0x2E]))
    room.AppendBytes(bytearray([0x01, 0x00]))
    room.AppendInteger(room_ids['client_id'] + 1, 2, 'little')

    ip_addr = _args['socket'].getpeername()[0].split('.')
    for number in ip_addr:
        room.AppendInteger(int(number))

    _args['socket'].send(room.packet)

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
    if selected_level not in PLANET_MAP_TABLE.keys():
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

    elif status_type == 1:
        room['slots'][str(slot)]['ready'] = not room['slots'][str(slot)]['ready']
    elif status_type == 2:
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

    room = get_room(_args)
    slot = get_slot(_args, room)

    result = PacketWrite()
    result.AddHeader(bytearray([0x60, 0x2F]))
    result.AppendBytes(bytearray([0x01, 0x00]))
    result.AppendInteger(slot - 1, 2, 'little')
    room['slots'][str(slot)]['in_shop'] = True
    _args['connection_handler'].SendRoomAll(_args['client']['room'], result.packet)

'''
This method allows users to exit the shop. This will notify all the other clients of the new character state as well
'''
def exit_shop(**_args):

    room = get_room(_args)
    slot = get_slot(_args, room)

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

    # Create start packet
    start = PacketWrite()
    start.AddHeader(bytearray([0xF3, 0x2E]))

    # Check if everyone is ready
    for key, slot in room['slots'].items():
        if not slot['ready'] and slot['client']['id'] != room['master']['id']:
            start.AppendBytes(bytearray([0x00, 0x6C]))
            return _args['client']['socket'].send(start.packet)

    # Finish start packet and broadcast to room
    start.AppendBytes(bytearray([0x01, 0x00]))
    start.AppendInteger(room['client_id'] + 1, 2, 'little')
    start.AppendInteger(room['level'], 2, 'little')
    start.AppendInteger(room['game_type'], 1)

    start.AppendInteger(0, 2, 'little')     # Start X
    start.AppendInteger(0, 2, 'little')     # Start Z
    start.AppendBytes([0x00])               # Start direction

    start.AppendBytes([0x02]) # Special trans
    start.AppendBytes([0x01]) # Event boss

    for _ in range(2):
        start.AppendBytes(bytearray([0x00, 0x00]))

    _args['connection_handler'].SendRoomAll(_args['client']['room'], start.packet)

    # Set room status
    room['status'] = 3
    get_list(_args, mode=0 if room['game_type'] in [0, 1] else room['game_type'] - 1,
             page=get_list_page_by_room_id(room['id'], room['game_type']), local=False)

'''
This method will reset the room by making sure nobody is ready anymore, drops are set back at their standard
values, etc.
'''
def reset(room):

    # Reset room variables
    room['drop_index']  = 1
    room['game_over']   = False

    # Reset player status
    for slot in room['slots']:
        slot = room['slots'][slot]
        slot['ready']           = 0
        slot['in_shop']         = False
        slot['loaded']          = False
        slot['dead']            = False
        slot['monster_kills']   = 0
        slot['player_kills']    = 0

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

def exit_room(**_args):

    # Check if we are in a room
    if 'room' not in _args['client']:
        return

    remove_slot(_args, _args['client']['room'], _args['client'])

def join_room(**_args):

    # Read information from join packet
    room_client_id  = int(_args['packet'].ReadInteger(1, 2, 'little')) - 1
    room_name       = _args['packet'].ReadStringByRange(2, 29)
    room_password   = _args['packet'].ReadStringByRange(29, 40)

    # Find room and join the room
    for key in _args['server'].rooms:
        room = _args['server'].rooms[key]

        if room['client_id'] == room_client_id:

            # TODO: Check if game started and check if the password is correct, if it exists

            add_slot(_args, room['id'], _args['client'], True)
            sync_state(_args, room)
            break

'''
This method will sync the state for all the peers inside of it
'''
def sync_state(_args, room):

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

'''
This method gets the peer to peer port of a client and waits for it to be available.
If after 10 attempts this fails, we kill the connection
'''
def get_peer_port(connection_handler, server, client):

    # Number of attempts
    attempts = 0

    while 'p2p_host' not in client:
        if attempts >= 10 or client not in server.clients:
            print('Disconnecting client due to being too slow')
            connection_handler.CloseConnection(client)
            return 0

        print('[Attempt #{0}] Peer information not found. Trying again in 300ms ...'.format(attempts))
        attempts+=1
        time.sleep(0.300)

    # If we have found the port, return the port
    return int(client['p2p_host']['port'])

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