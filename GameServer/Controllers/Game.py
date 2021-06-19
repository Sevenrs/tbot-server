#!/usr/bin/env python3
__author__      = 'Icseon'
__copyright__   = 'Copyright (C) 2021 Icseon'
__version__     = '1.0'

from Packet.Write import Write as PacketWrite
from GameServer.Controllers.data.drops import *
from GameServer.Controllers.Room import get_room, get_slot
from GameServer.Controllers.Character import get_items
import random
import time
import _thread

"""
This controller is responsible for handling all game related actions
"""

'''
This method will handle monster deaths and broadcasts an acknowledgement to the room
of the monster being killed.
'''
def monster_kill(**_args):

    # If the client is not in a room or is not its master, drop the packet
    room = get_room(_args, True)
    if not room:
        return

    # Read monster ID from the packet
    monster_id = _args['packet'].GetByte(0)

    # Construct canister drops and drop chances
    drops = [
        (CANISTER_HEALTH,   0.05),
        (CANISTER_REBIRTH,  0.02),
        (CANISTER_STUN,     0.01),
        (CANISTER_BOMB,     0.02),
        (CANISTER_TRANS_UP, 0.01),
        (CANISTER_AMMO,     0.01)
    ]

    # Calculate whether or not we should drop an item based on chance
    monster_drops = []
    for drop, chance in drops:
        if random.random() < chance:
            monster_drops.append(bytes([room['drop_index']]))
            monster_drops.append(drop.to_bytes(length=4, byteorder='little'))
            room['drop_index'] += 1
    drop_bytes = b''.join(monster_drops)

    # Create death response
    death = PacketWrite()
    death.AddHeader(bytes=bytearray([0x25, 0x2F]))
    death.AppendBytes(bytes=bytearray([0x01, 0x00]))
    death.AppendInteger(integer=monster_id, length=2, byteorder='little')

    death.AppendBytes([0x00, 0x00])
    death.AppendInteger(len(monster_drops), length=2, byteorder='little')
    death.AppendBytes(drop_bytes)

    # Broadcast the response to all sockets in the room
    _args['connection_handler'].SendRoomAll(room['id'], death.packet)

'''
This method will handle picking up items which were dropped from monsters
'''
def use_item(**_args):

    # If the client is not in a room, drop the packet
    room = get_room(_args)
    if not room:
        return

    # Read item index and type from packet
    item_index  = _args['packet'].GetByte(2)
    item_type   = _args['packet'].GetByte(3)

    print("Index: {0}, Type: {1}".format(item_index, item_type))

    use_canister = PacketWrite()
    use_canister.AddHeader(bytearray([0x23, 0x2F]))
    use_canister.AppendInteger(get_slot(_args, room) - 1, 2, 'little')
    use_canister.AppendInteger(item_index, 1, 'little')
    use_canister.AppendInteger(item_type, 4, 'little')
    _args['connection_handler'].SendRoomAll(room['id'], use_canister.packet)

'''
This method will handle player deaths.
It works by reading the slot number and broadcasting that the player is dead to all room sockets
'''
def player_death(**_args):

    # If the client is not in a room, drop the packet
    room = get_room(_args)
    if not room:
        return

    # Get slot number from the room
    room_slot = get_slot(_args, room)

    # Update room object and classify the player as dead
    room['slots'][str(room_slot)]['dead'] = True

    # Let the room know about the death of this player
    death = PacketWrite()
    death.AddHeader(bytearray([0x54, 0x2F]))
    death.AppendBytes(bytes=bytearray([0x01, 0x00]))
    death.AppendInteger(integer=(int(room_slot) - 1), length=2, byteorder='little')
    _args['connection_handler'].SendRoomAll(room['id'], death.packet)



'''
This method will handle game ends
'''
def game_end(**_args):

    # If the client is not in a room or is not its master, drop the packet
    room = get_room(_args, True)
    if not room:
        return

    # Check the status by checking the packet header
    status = 0 if _args['packet'].id == '3b2b' else 1

    result = PacketWrite()
    result.AddHeader(bytes=bytearray([0x2A, 0x27]))
    result.AppendInteger(status, 2, 'little')

    _args['connection_handler'].SendRoomAll(room['id'], result.packet)

    # Get wearing items so we can pass them as arguments
    wearing_items = get_items(_args, _args['client']['character']['id'], 'wearing')
    print(wearing_items)

    # Start new thread for the game statistics packets
    _thread.start_new_thread(game_stats, (_args, room, wearing_items,))

'''
This method will show the score board to all players in the room
'''
def game_stats(_args, room, wearing_items):

    time.sleep(6)

    packet = PacketWrite()
    packet.AddHeader(bytearray([0x1F, 0x2F]))

    # result
    packet.AppendBytes(bytearray([0x01, 0x00]))

    # unknown, presumably new experience points
    packet.AppendInteger(0, 2, 'little')

    # new gold amount
    packet.AppendInteger(10, 8, 'little')

    # new level
    packet.AppendInteger(71, 2, 'little')

    # new experience amount
    packet.AppendInteger(0, 4, 'little')

    # new bot stract amount
    packet.AppendInteger(60000, 4, 'little')

    # unknown
    packet.AppendInteger(6550, 4, 'little')

    # item times
    for idx in wearing_items['items']:
        packet.AppendInteger(wearing_items['items'][idx]['duration'], 4, 'little')

    # new attack min
    packet.AppendInteger(2000, 2, 'little')

    # new attack max
    packet.AppendInteger(2000, 2, 'little')

    # new attack max
    packet.AppendInteger(2000, 2, 'little')

    # 8 bytes that tell which player won
    for _ in range(8):
        packet.AppendInteger(0, 1, 'little')

    # 8 bytes that well which player leveled up
    for _ in range(8):
        packet.AppendInteger(0, 1, 'little')

    # another 8 bytes which contain the new levels of said players
    for _ in range(8):
        packet.AppendInteger(71, 1, 'little')

    # new experience points for all players
    for _ in range(8):
        packet.AppendInteger(0, 4, 'little')

    # new health amount for all players
    for _ in range(8):
        packet.AppendInteger(3000, 4, 'little')

    # points
    for _ in range(8):
        packet.AppendInteger(3000, 4, 'little')

    # player kills
    for _ in range(8):
        packet.AppendInteger(0, 4, 'little')

    # mob kills
    for _ in range(8):
        packet.AppendInteger(20, 4, 'little')

    # mvps shown
    packet.AppendBytes(bytearray([0x00, 0x00]))

    _args['connection_handler'].SendRoomAll(room['id'], packet.packet)

    # We must now send the packet to go back to room after 6 seconds
    time.sleep(6)
    game_exit = PacketWrite()
    game_exit.AddHeader(bytearray([0x2A, 0x2F]))
    game_exit.AppendBytes(bytearray([0x00]))
    _args['connection_handler'].SendRoomAll(room['id'], game_exit.packet)
