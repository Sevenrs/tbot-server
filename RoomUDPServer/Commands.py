#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

"""
This method will execute a command based on the received command ID
"""
def execute(server, address, packet):
    
    if packet.id == 'c800':
        server.sendto(bytearray([0xC8, 0x00, 0x04, 0x00, 0x01, 0x00, 0x00, 0x01]), address)
    else:
        print('Unknown command ID', packet.id)
