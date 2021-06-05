#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite

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

def AddSlot(_args, room_id, client):

    # Find room
    room = _args['server'].rooms[str(room_id)]

    # Get first available slot number
    slot = 1

    # Append to slots
    room['slots'][str(slot)] = {
        "client": client,
        "loaded": False
    }

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

    # Set room id for current client to indicate that our client is in a room
    _args['client']['room'] = room_ids['slot']

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

    start = PacketWrite()
    start.AddHeader(bytearray([0x67, 0x66]))
    start.AppendBytes(bytearray([0x73, 0x68, 0x6C, 0x02]))
    for _ in range(30):
        start.AppendBytes(bytearray([0x00]))
    _args['connection_handler'].SendRoomAll(_args['client']['room'], start.packet)

    start = PacketWrite()
    start.AddHeader(bytearray([0xF3, 0x2E]))
    start.AppendBytes(bytearray([0x01, 0x00]))
    start.AppendInteger(room['client_id'], 2, 'little')
    start.AppendInteger(room['level'], 2, 'little')
                                                                    # spec_trans
    start.AppendBytes(bytearray([0x03, 0x00, 0x01, 0x00, 0x00, 0x00, 0x00, 0x01]))
    _args['connection_handler'].SendRoomAll(_args['client']['room'], start.packet)

    room_info = PacketWrite()
    room_info.AddHeader(bytearray([0x00, 0x00]))
    room_info.AppendBytes(bytearray([0x01, 0x00]))
    room_info.AppendString(room['name'], 27)
    _args['connection_handler'].SendRoomAll(_args['client']['room'], room_info.packet)

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
        if not room['slots'][slot]['loaded']:
            return

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
    RemoveSlot(_args, _args['client']['room'], _args['client'])