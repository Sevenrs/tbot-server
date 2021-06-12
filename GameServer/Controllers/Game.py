#!/usr/bin/env python3
__author__      = 'Icseon'
__copyright__   = 'Copyright (C) 2021 Icseon'
__version__     = '1.0'

from Packet.Write import Write as PacketWrite

"""
This controller is responsible for handling all game related actions
"""

'''
This method will check if the client is in a room.
Additionally, the master flag will dictate whether or not a client should be a room master
'''
def in_room(_args, master=False):

    # The client sending the packet must be in a room
    if 'room' not in _args['client']:
        return False

    # Find room and check if the client is the room master
    if master:
        room = _args['server'].rooms[str(_args['client']['room'])]
        if room['master']['id'] != _args['client']['id']:
            return False

    return True

'''
This method will handle monster deaths and broadcasts an acknowledgement to the room
of the monster being killed.
'''
def monster_kill(**_args):

    # If the client is not in a room or is not its master, drop the packet
    if not in_room(_args, True):
        return

    # Read monster ID from the packet
    monster_id = _args['packet'].GetByte(0)

    # Create death response
    death = PacketWrite()
    death.AddHeader(bytes=bytearray([0x25, 0x2F]))
    death.AppendBytes(bytes=bytearray([0x01, 0x00]))
    death.AppendInteger(integer=monster_id, length=1, byteorder='little')
    death.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00])) #todo: handle drops

    # Broadcast the response to all sockets in the room
    _args['connection_handler'].SendRoomAll(_args['client']['room'], death.packet)

'''
This method will handle game ends
'''
def game_end(**_args):

    # If the client is not in a room or is not its master, drop the packet
    if not in_room(_args=_args, master=True):
        return

    result = PacketWrite()
    result.AddHeader(bytes=bytearray([0x2A, 0x27]))
    result.AppendBytes([0x01])
    _args['connection_handler'].SendRoomAll(_args['client']['room'], result.packet)