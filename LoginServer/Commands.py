#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from LoginServer.Packets import Login

"""
This method will execute a command based on the received command ID
"""
def execute(socket, packet):
    
    """
    Check the command ID and execute the correct action based on that
    """
    if (packet.id == 'f82a'):
        Login.Authenticate(socket, packet)

    else:
        print('Unknown packet ID:', packet.id)
