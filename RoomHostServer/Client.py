#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.ReadDatagram import ReadDatagram as ReadDatagram
from . import Commands

class Client:

    """
    ChannelServer datagram client constructor
    """
    def __init__(self, data, addr, server, game_server, connection_handler):
        self.data               = data
        self.address            = addr
        self.server             = server
        self.game_server        = game_server
        self.connection_handler = connection_handler
        
        # Immediately handle the new client's connection
        self.handle()

    """
    This method will handle the client's data
    """
    def handle(self):
        #print('New connection from:', self.address)
        
        # Obtain packet and execute the relevant command for it
        packet = ReadDatagram(self.data)
        Commands.execute(self.server, self.address, self.game_server, self.connection_handler, packet)
