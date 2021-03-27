#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

import socket
import _thread
from . import Client

class Socket:

    """
    RoomUDPServer contructor
    """
    def __init__(self, port):
        self.port = port

        # Start the server
        self.listen()

    """
    This method will listen for new connections
    """
    def listen(self):
        try:
            
            # Create Datagram server socket to act as as channel server
            server = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)
            server.bind(('0.0.0.0', self.port))
            
            print('[RoomUDPServer]: Started on port', self.port)
            
            # Continue to listen for new connections
            while True:
                
                # Accept the new client and handle the connection in a seperate thread
                message, address = server.recvfrom(12)
                _thread.start_new_thread(Client.Client, (message, address, server,))
                
            # Free socket on application termination
            server.close()
        except Exception as e:
            print('[RoomUDPServer]: Failed to start Room UDP Server. Perhaps the port is already in use. Exception:', e)
