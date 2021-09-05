#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

import socket
import _thread
from . import Client
from GameServer import Connection

class Socket:

    """
    RoomHost contructor
    """
    def __init__(self, port, game_server):
        self.port           = port
        self.game_server    = game_server
        self.socket         = None

    """
    This method will listen for new connections
    """
    def listen(self):
        try:
            
            # Create Datagram server socket to act as as channel server
            server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            server.bind(('0.0.0.0', self.port))
            self.socket = server
            
            print('[RoomHostServer]: Started on port', self.port)
            
            # Continue to listen for new connections
            while True:
                
                # Accept the new client and handle the connection in a separate thread
                message, address = server.recvfrom(12)
                _thread.start_new_thread(Client.Client, (message, address, server, self.game_server, Connection.Handler(self.game_server)))
                
            # Free socket on application termination
            server.close()
        except Exception as e:
            print('[RoomHostServer]: Failed to start Room Host Server. Perhaps the port is already in use. Exception:', e)
