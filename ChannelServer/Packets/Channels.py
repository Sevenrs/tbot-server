#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from enum import Enum
import MySQL.Interface as MySQL

"""
This file is responsible sending the channel list
"""

"""
Channel data
"""
NO_CHANNEL = bytearray([
    0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
    0x00, 0x00, 0x00, 0x00, 0x00
])

RELAY_NONE = bytearray([
    0xFF, 0xFF, 0x00, 0x00, 0x00, 0x00
])

"""
This method will authenticate a user
"""


def get_channels(server, address, packet, game_server):

    # Get requested world for channels
    world = int(packet.data[0])

    # Array with relay servers
    relay_servers = []

    # Obtain channels with this world ID
    try:
        connection = MySQL.get_connection()
        cursor = connection.cursor(dictionary=True)

        # Create new packet and add the proper header
        packet = PacketWrite()
        packet.add_header(bytearray([0xEE, 0x2C]))

        # Find channels with this world ID
        cursor.execute('SELECT `name`, `population`, `min_level`, `max_level`, `relay_server_addr` FROM `channels` '
                       'WHERE `world` = %s', [world])

        # Loop through every channel and add to packet
        for channel in cursor:

            # Min and max level and channel name
            # packet.append_integer(channel['population'], 2, 'little')
            packet.append_integer(len(game_server.clients), 2,
                                  'little')  # Temporary population, change when scaling to multiple servers
            packet.append_integer(channel['min_level'])
            packet.append_integer(channel['max_level'])
            packet.append_string(channel['name'], 22)

            # Append relay server to relay servers
            if channel['relay_server_addr'] is not None:
                relay_servers.append(channel['relay_server_addr'])

        # For all channels that do not exist, send over NO_CHANNEL
        for _ in range(12 - cursor.rowcount):
            packet.append_bytes(NO_CHANNEL)

        # Send the array with available relay servers
        for relay_server in relay_servers:
            packet.append_bytes(bytes=[0x00, 0x00])
            ip_addr = relay_server.split('.')
            for oct in ip_addr:
                packet.append_integer(int(oct))

        for _ in range(6 - len(relay_servers)):
            packet.append_bytes(RELAY_NONE)

        server.sendto(packet.packet, address)

    except Exception as e:
        print(e)
