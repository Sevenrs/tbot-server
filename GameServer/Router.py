#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

# Import MySQL interface to communicate with the database
import MySQL.Interface as MySQL

# Import all packet handlers to use throughout the service
from GameServer.Controllers.data.packets import PACKET_READ, PACKET_NAME, PACKET_HANDLER, PACKET_MYSQL_REQUIRED

"""
This method will link the incoming packet to the right controller
Similar to backends seen in websites
"""

def route(socket, packet, server, client, connection_handler):

    """
    If our client has no connected character with it, it means that the client is attempting to communicate with the server without
    having sent a ID request first.

    We must check if the client exists in the global client container and check if the command ID is equal to the ID request
    and we must check if the client has a character, and if not we must only accept the character create packet
    """
    if client not in server.clients and packet.id != 'f82a' or 'character' not in client and client in server.clients and not (
            packet.id == 'fa2a'):
        raise Exception('Invalid packet received')

    # Default the MySQL connection and cursor to NoneTypes
    mysql_connection, mysql = None, None

    # If the packet is in the PACKET_READ object, handle it
    if packet.id in PACKET_READ:

        received_packet = PACKET_READ[packet.id]
        if received_packet[PACKET_NAME] != 'PACKET_PONG':
            print("[GameServer] Parsing packet :: {0}".format(received_packet[PACKET_NAME]))

        # If we need a MySQL connection, create one
        if received_packet[PACKET_MYSQL_REQUIRED]:
            mysql_connection = MySQL.GetConnection()
            mysql = mysql_connection.cursor(dictionary=True, buffered=True)

        # Handle the packet
        received_packet[PACKET_HANDLER](**locals())

    # If we could not find the packet, handle it otherwise
    else:
        unknown(**locals())

    # If the mysql_connection is not None, close the cursor and connection
    if mysql_connection is not None:
        mysql.close()
        mysql_connection.close()


"""
Handle unknown packets
"""

def unknown(**_args):
    print('[GameServer] Unknown packet: <0x{0}[len={2}]::{1}>'.format(_args['packet'].id, _args['packet'].data, len(_args['packet'].data)))
