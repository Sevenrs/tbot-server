#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character

"""
This controller is responsible for handling all room related requests
"""


def GetList(_args, mode=2, page=0):

    # Calculate mode to the mode used in room storage
    if mode > 0:
        mode = mode + 1

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

    _args['socket'].send(result.packet)

"""
This method will get the first free room id
"""
def GetAvailableRoomNumber(_args, game_type):

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

def ConstructRoomPlayers(_args, packet, character, slot_num):

    # Send character level
    packet.AppendInteger(character['level'], 2, 'little')

    # Obtain wearing items
    wearing_items = Character.get_items(_args, character['id'], 'wearing')

    for i in range(19):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        packet.AppendInteger(item['id'], 4, 'little')

    # unknown, but needed
    packet.AppendInteger(2, 2, 'little')
    packet.AppendBytes(bytearray([0x00]))

    # slot index
    packet.AppendInteger(slot_num - 1)

    # p2p ip addr (0.0.0.0 for now)
    packet.AppendBytes(bytearray([0x7F, 0x00, 0x00, 0x01]))

    for _ in range(10):
        packet.AppendBytes(bytearray([0x00]))

    # p2p port, idk for now
    if slot_num == 1:
        packet.AppendInteger(0, 2, 'little')
    else:
        packet.AppendInteger(43342, 2, 'little')

    # p2p ip addr (127.0.0.1 for now)
    packet.AppendBytes(bytearray([0x7F, 0x00, 0x00, 0x01]))

    for _ in range(10):
        packet.AppendBytes(bytearray([0x00]))

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
    packet.AppendString("guild name", 21)

    for _ in range(4):
        packet.AppendBytes(bytearray([0x00]))

    packet.AppendInteger(character['rank'], 2, 'little')
    for _ in range(6):
        packet.AppendBytes(bytearray([0x00]))

def AddSlot(_args, room_id, client, broadcast=False):

    # Find room
    room = _args['server'].rooms[str(room_id)]

    # Get first available slot number
    available_slot = 0

    for i in range(1, 8):
        if str(i) not in room['slots']:
            available_slot = i
            break

    # Append to slots
    room['slots'][str(available_slot)] = {
        "client": client,
        "loaded": False
    }

    if broadcast:

        # Define the slot and character for easy access
        slot        = room['slots'][str(available_slot)]
        character   = slot['client']['character']

        join = PacketWrite()
        join.AddHeader([0x29, 0x27])

        ConstructRoomPlayers(_args, join, character, available_slot)
        _args['connection_handler'].SendRoomAll(room['id'], join.packet)

    # Tell our client about the room
    if broadcast:

        players = PacketWrite()
        players.AddHeader([0x28, 0x2F])
        players.AppendBytes([0x01, 0x00])

        # Loop through all players in the room
        for i in range(0, 8):

            # Get slot and character
            if str((i + 1)) in room['slots']:
                print("slot {0} found".format(str(i)))
                character = room['slots'][str((i + 1))]['client']['character']
                ConstructRoomPlayers(_args, players, character, (i + 1))
            else:
                print("slot {0} not found".format(str(i)))
                for _ in range(221):
                    players.AppendBytes([0x00])

        players.AppendInteger(room['client_id'] + 1, 2, 'little')
        players.AppendString(room['name'], 27)
        players.AppendString(room['password'], 11)
        players.AppendInteger(room['game_type'], 1)
        for _ in range(7):
            players.AppendBytes([0x00])
        players.AppendBytes([0x00])

        # Notify our client about all players in the room
        client['socket'].send(players.packet)

     # Set room id for current client to indicate that our client is in a room
    _args['client']['room'] = room['id']




def RemoveSlot(_args, room_id, client):

    # Find room
    room = _args['server'].rooms[str(room_id)]

    # Find our slot and remove it from the room
    for key, slot in room['slots'].items():
        if slot['client']['id'] == client['id']:
            del room['slots'][key]

            # Send the exit packet to the client who was in the slot
            exit = PacketWrite()
            exit.AddHeader(bytearray([0x2E, 0x27]))
            exit.AppendBytes(bytearray([0x01, 0x00, (int(key) - 1), 0x01]))
            client['socket'].send(exit.packet)
            #_args['connection_handler'].SendRoomAll(room['id'], exit.packet)

            # Remove the room from the client so the client is no longer in the room
            client.pop('room')

            break

    # If the room has no more slots left, delete the room
    if len(room['slots']) == 0:
        del _args['server'].rooms[str(room_id)]


"""
This method will create a new room
"""

def Create(**_args):

    # Check if our current client is already in a room
    if 'room' in _args['client']:
        return

    print(_args['packet'].data)

    # Get parameters from the incoming packet
    room_name = _args['packet'].ReadStringByRange(0, 27)
    room_password = _args['packet'].ReadStringByRange(27, 38)
    room_gametype = _args['packet'].GetByte(39)
    room_time = _args['packet'].GetByte(41)
    room_ids = GetAvailableRoomNumber(_args, room_gametype)

    # Store room in the room container
    room = {
        "slots": {},
        "name": room_name,
        "password": room_password,
        "game_type": room_gametype,
        "time": room_time,
        "id": room_ids['slot'],
        "client_id": room_ids['client_id'],
        "master": _args['client'],
        "level": 0,
        "difficulty": 0,
        "status": 0
    }

    _args['server'].rooms[str(room_ids['slot'])] = room

    # Add ourselves to slots
    AddSlot(_args, room_ids['slot'], _args['client'])

    room = PacketWrite()
    room.AddHeader(bytearray([0xEE, 0x2E]))
    room.AppendBytes(bytearray([0x01, 0x00]))
    room.AppendInteger(room_ids['client_id'] + 1, 2, 'little')
    room.AppendString("0.0.0.0")

    _args['socket'].send(room.packet)

"""
This method will set the level for the room
"""
def SetLevel(**_args):

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

    # Set level for the room and broadcast to all clients in this room
    room['level'] = selected_level
    level = PacketWrite()
    level.AddHeader(bytearray([0x4A, 0x2F]))
    level.AppendBytes(bytearray([0x01, 0x00]))
    level.AppendInteger(selected_level, 2, 'little')
    _args['connection_handler'].SendRoomAll(_args['client']['room'], level.packet)


def set_difficulity(**_args):

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
    print(new_difficulty)

    room['difficulty'] = new_difficulty
    result = PacketWrite()
    result.AddHeader(bytearray([0x62, 0x2F]))
    result.AppendBytes(bytearray([0x01, 0x00]))
    result.AppendInteger(new_difficulty, 2, 'little')
    _args['connection_handler'].SendRoomAll(_args['client']['room'], result.packet)

"""
This method will start the game
"""
def StartGame(**_args):

    # Check if we are in a room
    if 'room' not in _args['client']:
        return

    # Get room from ID
    room = _args['server'].rooms[str(_args['client']['room'])]

    # Check if we are the room master
    if room['master']['id'] != _args['client']['id']:
        return

    room_info = PacketWrite()
    room_info.AddHeader(bytearray([0x67, 0x66]))
    room_info.AppendBytes(bytearray([0x65, 0x68]))
    room_info.AppendString(room['name'], 27)
    _args['connection_handler'].SendRoomAll(_args['client']['room'], room_info.packet)

    start = PacketWrite()
    start.AddHeader(bytearray([0x67, 0x66]))
    start.AppendBytes(bytearray([0x73, 0x68, 0x6C, 0x02]))
    for _ in range(30):
        start.AppendBytes(bytearray([0x00]))
    _args['connection_handler'].SendRoomAll(_args['client']['room'], start.packet)

    start = PacketWrite()
    start.AddHeader(bytearray([0x67, 0x66]))
    start.AppendBytes(bytearray([0x74, 0x68, 0x03]))
    _args['connection_handler'].SendRoomAll(_args['client']['room'], start.packet)

    start = PacketWrite()
    start.AddHeader(bytearray([0xF3, 0x2E]))
    start.AppendBytes(bytearray([0x01, 0x00]))
    start.AppendInteger(room['client_id'] + 1, 2, 'little')
    start.AppendInteger(room['level'], 2, 'little')
    start.AppendInteger(room['game_type'], 1)

    start.AppendInteger(0, 2, 'little')     # Start X
    start.AppendInteger(0, 2, 'little')     # Start Z
    start.AppendBytes([0x00])               # Start direction

    start.AppendBytes([0x02]) # Special trans
    start.AppendBytes([0x01]) # Boss event

    for _ in range(2):
        start.AppendBytes(bytearray([0x00, 0x00]))

    _args['connection_handler'].SendRoomAll(_args['client']['room'], start.packet)

    print('second done')

def GameLoadFinish(**_args):

    # Check if we are in a room
    if 'room' not in _args['client']:
        return

    room = _args['server'].rooms[str(_args['client']['room'])]
    for slot in room['slots']:

        # Set loaded status for our own client to true
        if room['slots'][slot]['client'] == _args['client']:
            room['slots'][slot]['loaded'] = True

        # If a client hasn't indicated loading has finished, we continue waiting
        #if not room['slots'][slot]['loaded']:
        #    return


    print(room['slots'])

    ready = PacketWrite()
    ready.AddHeader(bytearray([0x24, 0x2F]))
    ready.AppendBytes(bytearray([0x00]))
    _args['connection_handler'].SendRoomAll(_args['client']['room'], ready.packet)

def MonsterKill(**_args):

    # Check if we are in a room
    if 'room' not in _args['client']:
        return

    # Get room from ID
    room = _args['server'].rooms[str(_args['client']['room'])]

    # Check if we are the room master
    if room['master']['id'] != _args['client']['id']:
        return

    print(_args['packet'].data)

    # Read mob ID
    mob_id = _args['packet'].GetByte(0)

    kill = PacketWrite()
    kill.AddHeader(bytearray([0x25, 0x2F]))
    kill.AppendBytes(bytearray([0x01, 0x00]))
    kill.AppendInteger(mob_id, 1, 'little')
    kill.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
    _args['connection_handler'].SendRoomAll(_args['client']['room'], kill.packet)

def ExitRoom(**_args):

    # Check if we are in a room
    if 'room' not in _args['client']:
        return

    RemoveSlot(_args, _args['client']['room'], _args['client'])

def JoinRoom(**_args):

    print(_args['packet'].data)

    # Read information from join packet
    room_client_id  = int(_args['packet'].ReadInteger(1, 2, 'little')) - 1
    room_name       = _args['packet'].ReadStringByRange(2, 29)
    room_password   = _args['packet'].ReadStringByRange(29, 40)

    # Find room
    print(_args['server'].rooms)

    for key in _args['server'].rooms:

        room = _args['server'].rooms[key]

        if room['client_id'] == room_client_id:
            print('Room found. Attempt to join the room')
            AddSlot(_args, room['id'], _args['client'], True)

            break