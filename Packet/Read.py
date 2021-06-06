#/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

import binascii
import socket as Socket

"""
This class is responsible for the reading of packets
"""
class Read:

    """
    Packet constructor
    """
    def __init__(self, socket):
        
        try:

            """
            Check to see if we are receiving at least 4 bytes
            """
            if not socket.recv(4, Socket.MSG_PEEK):
                raise Exception('Received an invalid packet')
            
            """
            Receive the first two bytes that represent the packet ID
            Packet IDs should be converted to hexdecimal
            """
            self.id = "".join(map(chr, binascii.hexlify(socket.recv(2))))
            
            """
            Receive the next two bytes that represent the packet length
            This contains an unsigned short (max length is 65535 bytes)
            Also remove null bytes from the legth bytes to avoid it reading them
            """
            self.length = int.from_bytes(socket.recv(2), 'little')
            
            """
            Validate packet length. Check if the amount of bytes are really available
            """
            if (not socket.recv(self.length, Socket.MSG_PEEK)):
                raise Exception('Invalid packet length')
            
            """
            Receive additional data from the client based on the received
            packet length
            """
            self.data = socket.recv(self.length)
            if not self.data:
                raise Exception('Unable to receive data')
            
            """
            This defines the current position for reading
            """
            self.position = 0
            
        except OSError as e:
            raise Exception('Unable to read client packet: The connection which we tried to read data from no longer exists')

        except Exception as e:
            raise Exception('Unable to read client packet:', e)

    """
    This method will read a string from the packet buffer
    """
    def ReadString(self, skip = 0):

        # Initialize result
        result = ""
        
        # Skip specific amount of bytes, if specified
        if skip > 0:
            self.SkipBytes(skip)

        # Automatically skip null bytes
        self.SkipNullBytes()

        # Loop through bytes until a null byte is hit
        for index, byte in enumerate(self.data):
            if index < self.position:
                continue

            # Stop when we hit a null byte
            if int(byte) == 0:
                break

            # Add ASCII character to the result
            result += chr(byte)
            self.position = self.position + 1

        return result

    def ReadStringByRange(self, start=0, end=1):
        result = ""

        if self.length < end:
            raise Exception("Attempted to read packet string by range {} to {}, but the length is only {}".format(start, end, self.length))

        for i in range(start, end):
            if self.data[i] == 0x00:
                continue

            result += chr(self.data[i])
        return result

    """
    This method will skip null bytes and jump to the first position that does not have a null byte
    """
    def SkipNullBytes(self):
        for index, byte in enumerate(self.data):
            if index < self.position:
                continue

            # Stop iteration if there is not a null byte to skip
            if int(byte) != 0:
                break
            
            self.position = self.position + 1
            
    """
    This method will skip a specific amount of bytes
    """
    def SkipBytes(self, bytes):
        self.position = self.position + bytes

    """
    This method will get a byte from a specific position
    """
    def GetByte(self, position, length = 1):
        return self.data[position]

    """
    This method will get multiple bytes from start to end and parse them as an integer
    """
    def ReadInteger(self, start, end = 1, order='little'):

        bytes = bytearray()

        for i in range(end):
            bytes.append(self.data[start + (i - 1)])

        print(bytes)

        return int.from_bytes(bytes, byteorder=order)
