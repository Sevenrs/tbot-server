from Packet.Write import Write as PacketWrite
from GameServer.Controllers.Room import get_slot
import datetime


def route(client, packet):
    packets = {
        '34a0': ping,
        '35a0': request_virtual_ip,
        '38a0': command_relay
    }.get(packet.id, unknown)(**locals())


''' Handle unknown packets by redirecting its contents to stdout'''


def unknown(**_args):
    print("[{0}]: Unknown packet: <0x{1}[len={3}]::{2}>".format(_args['client']['server'].name, _args['packet'].id,
                                                                _args['packet'].data, len(_args['packet'].data)))


def ping(**_args):

    # Read relay client ID from the packet
    relay_id = int.from_bytes(_args['packet'].data[:2], byteorder='little')

    # Get our own relay client
    client = _args['client']['server'].relay.clients[relay_id]

    # If the client's address information does not match with our own, we'll drop the packet
    if client['socket'].getpeername()[0] != _args['client']['address'][0]:
        return

    # Set last ping timestamp
    client['last_ping'] = datetime.datetime.now()




def request_virtual_ip(**_args):

    # Create the acknowledgment response and send it to our client. We don't have to do any processing on our end
    # because we're already aware of who we are and what our address information is through the room host server.
    acknowledgment = PacketWrite(header=b'\x1D\xA4')
    acknowledgment.append_bytes(bytes=[0x01, 0xCC])
    _args['client']['server'].socket.sendto(acknowledgment.packet, (_args['client']['address']))


''' Send relay action packet to the destinations in the relay array for our player'''


def command_relay(**_args):

    # Get relay client ID from the information our client has supplied us with
    relay_id = int.from_bytes(_args['packet'].data[:2], byteorder='little')

    # Read action data from the client which starts at offset 8 - this is what we need to send to the clients
    action = _args['packet'].data[8:]

    # Get our own relay client
    client = _args['client']['server'].relay.clients[relay_id]

    # If the client's address information does not match with our own, we'll drop the packet
    if client['socket'].getpeername()[0] != _args['client']['address'][0]:
        return

    # If our client isn't in a room, we'll drop the packet as well
    if 'room' not in client['game_client']:
        return

    # Retrieve room and slot number
    room = client['game_server'].rooms[str(client['game_client']['room'])]
    slot = room['slots'][str(get_slot({'client': client['game_client']}, room))]

    # Loop through the relay IDs and bein sending the action packet to each of them
    for remote_relay_id in slot['relay_ids']:

        # Get our remote client which will be receiving the action packet
        remote_client = _args['client']['server'].relay.clients[remote_relay_id]

        # We'll require p2p_host to be present in the remote's game client object. If this isn't present
        # we can't send them their packet. We'll just wait for it to become present in the next packet.
        if 'p2p_host' not in remote_client['game_client']:
            continue

        # Retrieve peer information from the game client object. This information will be used to send the action packet.
        peer_information = remote_client['game_client']['p2p_host']

        # Send UDP action packet to the peer we have retrieved. We'll send it through the room host server
        _args['client']['server'].room.socket.sendto(action, (peer_information['ip'], peer_information['port']))