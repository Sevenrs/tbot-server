#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite

"""
This method will execute a command based on the received command ID
"""
def execute(server, address, game_server, connection_handler, packet):
    packets = {
        'c800': ping,
        'c900': host_update
    }.get(packet.id, unknown)(**locals())

''' This handler will handle unknown packets by printing its information to stdout '''
def unknown(**_args):
    print('[RoomHostServer] Unknown packet: <0x{0}::{1}>'.format(_args['packet'].id, _args['packet'].data))

''' This handler will handle ping packets '''
def ping(**_args):

    # Read client id from packet and respond with a response containing this client id
    client_id = int.from_bytes(_args['packet'].data[2:], byteorder='little')

    # Construct pong packet and send it back to the client
    pong = PacketWrite()
    pong.AddHeader(bytes=bytearray([0xC8, 0x00]))
    pong.AppendBytes(bytes=bytearray([0x01, 0x00]))
    pong.AppendInteger(integer=client_id, length=2, byteorder='little')
    _args['server'].sendto(pong.packet, _args['address'])

''' This handler will handle host updates '''
def host_update(**_args):

    """     This packet sends a number that identifies the client by identification number.
            We have to re-assign the host and port for this specific client and tell everyone in the room they are in about the change."""
    client_id = int.from_bytes(_args['packet'].data, byteorder='little')

    # Now that we have the client ID, update the host and tell the room about it
    for client in _args['game_server'].clients:

        if client['id'] == client_id and 'room' in client:
            client['p2p_host'] = {'ip': _args['address'][0], 'port': _args['address'][1]}

            # Find room
            room = _args['game_server'].rooms[str(client['room'])]

            # Send p2p ports to all clients in the room
            ports = PacketWrite()
            ports.AddHeader(bytearray([0x39, 0x27]))
            for i in range(0, 8):
                if str((i + 1)) in room['slots']:

                    # Get client and p2p port number and append to packet, if it exists
                    room_client = room['slots'][str((i + 1))]['client']
                    ports.AppendInteger(0 if 'p2p_host' not in room_client else room_client['p2p_host']['port'], 2, 'big')
                else:
                    ports.AppendInteger(0, 2, 'big')
            client['socket'].sendall(ports.packet)
            break