from Packet.Write import Write as PacketWrite
from GameServer.Controllers.Room import get_slot
import datetime


def route(client, packet):
    packets = {
        '34a0': ping,
        '35a0': add_peer_info,
        '38a0': relay_action
    }.get(packet.id, unknown)(**locals())


''' Handle unknown packets by redirecting its contents to stdout'''


def unknown(**_args):
    print("[{0}]: Unknown packet: <0x{1}[len={3}]::{2}>".format(_args['client']['server'].name, _args['packet'].id,
                                                                _args['packet'].data, len(_args['packet'].data)))


def ping(**_args):
    # Read relay client ID
    relay_id = int.from_bytes(_args['packet'].data[:2], byteorder='little')

    # Retrieve our relay client and update the last_ping timestamp with now
    for client in _args['client']['server'].relay.clients:

        # If the client ID matches the relay ID we received (and the UDP remote address is equal to the client
        # then we can update the timestamp
        if client['id'] == relay_id and client['socket'].getpeername()[0] == _args['client']['address'][0]:
            client['last_ping'] = datetime.datetime.now()


''' Add peer information to the state of the relay TCP client so we can access that information later'''


def add_peer_info(**_args):
    # Read relay client ID
    relay_id = int.from_bytes(_args['packet'].data[:2], byteorder='little')

    # Find our client and assign the peer information to it
    for client in _args['client']['server'].relay.clients:

        if client['id'] == relay_id and client['socket'].getpeername()[0] == _args['client']['address'][0]:
            client['peer_info'] = {
                'ip': _args['client']['address'][0],
                'port': _args['client']['address'][1]
            }

            # Create the acknowledgment response and send it to our client
            acknowledgment = PacketWrite()
            acknowledgment.add_header(bytes=[0x1D, 0xA4])
            acknowledgment.append_bytes(bytes=[0x01, 0xCC])
            _args['client']['server'].socket.sendto(acknowledgment.packet, _args['client']['address'])
            break


''' Send relay packet to the destinations in the relay array for our player'''


def relay_action(**_args):
    # Read relay client ID
    relay_id = int.from_bytes(_args['packet'].data[:2], byteorder='little')

    # Unknown, presumably checks of some kind
    unk1 = int.from_bytes(_args['packet'].data[10:2], byteorder='little')
    unk2 = int.from_bytes(_args['packet'].data[12:2], byteorder='little')

    # Create new packet
    action = PacketWrite()
    action.append_integer(unk1, 2, 'little')
    action.append_integer(unk2, 2, 'little')
    action.append_bytes(bytes=_args['packet'].data)

    # Construct final packet needed
    answer = action.data[12:(12 + _args['packet'].length)]

    # Retrieve our relay client to find the room we are in
    for client in _args['client']['server'].relay.clients:

        if client['id'] == relay_id and client['socket'].getpeername()[0] == _args['client']['address'][0]:

            # Create a reference to the game client for easier access
            game_client = client['game_client']
            game_server = client['game_server']

            # If the game_client is not in a room, don't do anything.
            if 'room' not in game_client:
                return

            # Retrieve room and slot number
            room = game_server.rooms[str(game_client['room'])]
            slot = room['slots'][str(get_slot({'client': game_client}, room))]

            # Retrieve the relay ids for the slot and loop through them to finally send the packet
            relay_ids = slot['relay_ids']
            for id in relay_ids:
                for client_id in _args['client']['server'].relay.clients:

                    # Check if the id matches and if the client's game_client has p2p information assigned to it.
                    # It is possible the client adds themselves to the id list before having p2p information.
                    if client_id['id'] == id and 'p2p_host' in client_id['game_client']:
                        # Retrieve peer host information and forward packet
                        p2p_host = client_id['game_client']['p2p_host']
                        _args['client']['server'].room.socket.sendto(answer, (p2p_host['ip'], p2p_host['port']))
                        break
            break
