#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from ChannelServer.Packets import Channels

"""
This method will execute a command based on the received command ID
"""
def execute(server, address, packet, game_server):
    
    if packet.id == 'fa2a':
        Channels.GetChannels(server, address, packet, game_server)
    else:
        print('[ChannelServer] Unknown command ID', packet.id)
