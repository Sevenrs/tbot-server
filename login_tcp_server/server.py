#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2021 Icseon"
__version__ = "2.0"

'''
This file is responsible for starting the Login server
'''

import socket
import _thread
from login_tcp_server import router
from Packet.Read import Read as PacketRead

class LoginTCPServer:

    def __init__(self, port):
        self.port = port
        self.name = 'LoginTCPServer'

    def listen(self):
        try:

            ''' Bind a socket on the specified port and listen for new connections '''
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
                server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                server.bind(('0.0.0.0', self.port))
                server.listen()

                print('[{0}]: Started on port {1}'.format(self.name, self.port))

                # Keep accepting new connections in a new thread
                while True:
                    client, address = server.accept()
                    _thread.start_new_thread(LoginTCPConnection, (client, address, self,))

        except Exception as e:
            print("[{0}]: Failed to bind because: {1}".format(self.name, e))

class LoginTCPConnection:

    def __init__(self, socket, address, server):
        self.socket     = socket
        self.address    = address
        self.server     = server

        # Handle connection
        self.handle()

    ''' This method will handle new connections '''
    def handle(self):
        print("[{0}]: New connection from {1}:{2}".format(self.server.name, self.address[0], self.address[1]))

        # Keep reading data
        while True:
            try:
                packet = PacketRead(self.socket)
                router.route(self.__dict__, packet)

            except Exception as e:
                print(e)
                break