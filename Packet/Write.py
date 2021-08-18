#/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

import struct

"""
This class is responsible for the writing of packets which are then sent to the game client
"""
class Write:

    """
    Packet Writer Constructor
    """
    def __init__(self):
        self.header = bytearray()
        self.length = bytearray()
        self.data   = bytearray()
        
        # Final packet
        self.packet = bytearray()
        
    """
    This method adds a header to the packet
    """
    def AddHeader(self, bytes):
        self.header = bytes
        
    """
    This method adds data to the packet
    """
    def AddData(self, bytes):
        
        # Add data to packet
        self.data.extend(bytes)
        
        # Calculate new packet length
        self.length = len(self.data).to_bytes(length=2, byteorder='little')
        
        # Build final packet
        packet = bytearray()
        packet.extend(self.header)
        packet.extend(self.length)
        packet.extend(self.data)
        self.packet = packet

    """
    This method will append bytes to the packet
    We are expecting a byte array to extend to the existing packet
    """
    def AppendBytes(self, bytes):
        try:
            self.AddData(bytes)
        except Exception as e:
            print('[PacketWrite@AppendBytes]: Failed because of', e)

    """
    This method will append a string to the packet
    The length argument is used to specify a fixed byte array length
    """
    def AppendString(self, string, length = 0):
        try:
        
            # Initialize the resulting byte array and extend the array with ASCII encoded text
            result = bytearray()
            result.extend(string.encode('windows-1252', errors='replace'))
            
            # If the length of the string is larger than the provided string, fix the length and print a warning
            if length < len(string) and length != 0:
                length = len(string)
                print('[PacketWrite@AppendString]: We got a string larger than the specified length. Automatically increased the length!')
        
            # If the string length is larger than the ASCII string, append null bytes until the length is reached
            for i in range(len(string), length):
                result+= struct.pack('<B', 0x00)
            
            # Append the result (fixed length string) to the packet
            self.AddData(result)
        except Exception as e:
            print('[PacketWrite@AppendString]: Failed because of', e)
        
    """
    This method will append an integer to the packet with a fixed length
    """
    def AppendInteger(self, integer, length = 1, byteorder = 'big'):
        try:
            self.AddData(integer.to_bytes(length=length, byteorder=byteorder))
        except Exception as e:
            print('[PacketWrite@AppendInteger]: Failed because of', e)
