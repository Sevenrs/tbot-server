# /usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

import binascii
import socket as sock

"""
This class is responsible for the reading of packets
"""


class Read:
    """
    This method will receive packet data, de-xor it and return it to the stack
    """

    def recv(self, length):

        # Receive data from the socket
        data = self.socket.recv(length, sock.MSG_WAITALL)

        # Initialize result buffer
        result = bytearray()

        # De-xor every byte in the buffer
        # al parecer cada cliente utiliza un porpio metodo de encriptación
        for i in range(len(data)):
            result.append(0x00 ^ data[i])#ohka-bot
            #result.append(0xED ^ data[i])#t-bot 
        

        return result

    """
    Packet constructor
    """

    def __init__(self, socket):

        try:

            # Set socket
            self.socket = socket

            """
            Check to see if we are receiving at least 4 bytes
            """
            if not socket.recv(4, sock.MSG_PEEK):
                raise Exception('Received an invalid packet')

            """
            Receive the first two bytes that represent the packet ID
            Packet IDs should be converted to hexadecimal
            """
            self.id = "".join(map(chr, binascii.hexlify(self.recv(2))))

            """
            Receive the next two bytes that represent the packet length
            This contains an unsigned short (max length is 65535 bytes)
            Also remove null bytes from the length bytes to avoid it reading them
            """
            self.length = int.from_bytes(self.recv(2), 'little')

            """
            Validate packet length. Check if the amount of bytes are really available
            """
            if not socket.recv(self.length, sock.MSG_PEEK):
                raise Exception('Invalid packet length')

            """
            Receive additional data from the client based on the received
            packet length
            """
            self.data = self.recv(self.length)
            if not self.data:
                raise Exception('Unable to receive data')

            """
            This defines the current position for reading
            """
            self.position = 0

        except OSError as e:
            raise Exception(
                'Unable to read client packet: The connection which we tried to read data from no longer exists: ', e)

        except Exception as e:
            raise Exception('Unable to read client packet:', e)

    """
    This method will read a string from the packet buffer
    """

    def read_string(self, skip=0):

        # Initialize result
        bytes = bytearray()

        # Skip specific amount of bytes, if specified
        if skip > 0:
            self.skip(skip)

        # Automatically skip null bytes
        self.skip_null()

        # Loop through bytes until a null byte is hit
        for index, byte in enumerate(self.data):
            if index < self.position:
                continue

            # Stop when we hit a null byte
            if int(byte) == 0:
                break

            # Add byte to result
            bytes.append(byte)
            self.position = self.position + 1

        return bytes.decode('windows-1252', errors='replace')

    def read_string_by_range(self, start=0, end=1):
        bytes = bytearray()

        if self.length < end:
            raise Exception(
                "Attempted to read packet string by range {} to {}, but the length is only {}".format(start, end,
                                                                                                      self.length))

        for i in range(start, end):
            if self.data[i] == 0x00:
                continue

            bytes.append(self.data[i])
        return bytes.decode('windows-1252', errors='replace')

    """
    This method will skip null bytes and jump to the first position that does not have a null byte
    """

    def skip_null(self):
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

    def skip(self, bytes):
        self.position = self.position + bytes

    """
    This method will get a byte from a specific position
    """

    def get_byte(self, position):
        return self.data[position]

    """
    This method will get multiple bytes from start to end and parse them as an integer
    """

    def read_integer(self, start, end=1, order='little'):

        bytes = bytearray()

        for i in range(end):
            bytes.append(self.data[start + i])

        return int.from_bytes(bytes, byteorder=order)
