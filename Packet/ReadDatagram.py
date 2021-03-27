#/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

import binascii

class ReadDatagram:
    
    def __init__(self, packet):
        
        try:
            self.packet = packet
        
            # Bout packets must be at least 4 bytes long
            if (len(self.packet) < 4):
                raise Exception('Received an invalid packet')
            
            # Attempt to read the first two bytes which identify the packet by ID
            self.id = "".join(map(chr, binascii.hexlify(self.packet[0:2])))
            
            # Obtain the packet length
            self.length = int.from_bytes(self.packet[2:4], 'little')
            
            # Validate packet length.
            # Remove 4 from the length because that is not relevant
            if len(self.packet) - 4 != self.length:
                raise Exception('Invalid packet length received. Got: {}, Expected: {}'.format(len(self.packet) - 4, self.length))
            
            # Get packet data
            self.data = self.packet[4:(4+ self.length)]
            
        except Exception as e:
            print('Failed to parse datagram packet because', e)
