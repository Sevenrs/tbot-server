#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Read import Read as PacketRead
from . import Router

class Client:

    """
    GameServer client constructor
    """
    def __init__(self, socket, addr, server, connection_handler, session_handler):
        self.socket             = socket
        self.address            = addr
        self.server             = server
        self.connection_handler = connection_handler
        self.session_handler    = session_handler
        
        " Create new client dictionary "
        self.client = {
            'id':       None,
            'socket':   self.socket
        }
        
        # Immediately handle the new client's connection
        self.handle()

    """
    This method will handle the client's data
    """
    def handle(self):
        print('[GameServer]: New connection from:', self.address)

        # Receive data from the client
        while True:
            try:
                packet = PacketRead(self.socket)
                Router.route(self.socket, packet, self.server, self.client, self.connection_handler, self.session_handler)
            except Exception as e:
                print(e)
                print(self.address, 'has disconnected')                
                self.connection_handler.UpdatePlayerStatus(self.client, 2)
                break
