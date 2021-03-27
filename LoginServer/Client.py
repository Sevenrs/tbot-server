#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Read import Read as PacketRead
from . import Commands

class Client:

    """
    LoginServer client constructor
    """
    def __init__(self, socket, addr):
        self.socket = socket
        self.address = addr
        
        # Immediately handle the new client's connection
        self.handle()

    """
    This method will handle the client's data
    """
    def handle(self):
        print('New connection from:', self.address)

        # Receive data from the client
        while True:
            try:
                packet = PacketRead(self.socket)
                Commands.execute(self.socket, packet)
            except Exception as e:
                print(self.address, 'has disconnected')
                self.socket.close()
                break
