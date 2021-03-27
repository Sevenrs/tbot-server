#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

import socket
import _thread
from . import Client

class Socket:

    """
    LoginServer contructor
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

            # Start the server by binding a TCP socket to the right port
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('0.0.0.0', self.port))
                server.listen()
                
                print('[LoginServer]: Started on port', self.port)

                # Listen for new connections
                while True:
                    
                    # Accept the new client and handle the connection in a seperate thread
                    client, address = server.accept()
                    _thread.start_new_thread(Client.Client, (client, address,))
                    
                # Ensure the socket is freed once the application exits
                server.close()
        except Exception as e:
            print('[LoginServer]: Failed to start Login Server. Perhaps the port is already in use. Exception:', e)
