from Packet.Write import Write as PacketWrite
from GameServer.Controllers.Room import get_slot

def route(client, packet):

    packets = {
        '35a0': add_peer_info,
        '38a0': relay_action
    }.get(packet.id, unknown)(**locals())

''' Handle unknown packets by redirecting its contents to stdout'''
def unknown(**_args):
    print("[{0}]: Unknown packet: <0x{1}[len={3}]::{2}>".format(_args['client']['server'].name, _args['packet'].id,
                                                                _args['packet'].data, len(_args['packet'].data)))

''' Add peer information to the state of the relay TCP client so we can access that information later'''
def add_peer_info(**_args):

    # Read relay client ID
    relay_id = int.from_bytes(_args['packet'].data[:2], byteorder='little')

    # Find our client and assign the peer information to it
    for client in _args['client']['server'].relay.clients:
        if client['id'] == relay_id:
            client['peer_info'] = {
                'ip':   _args['client']['address'][0],
                'port': _args['client']['address'][1]
            }

            # Create the acknowledge response and send it to our client
            acknowledgment = PacketWrite()
            acknowledgment.AddHeader(bytes=[0x1D, 0xA4])
            acknowledgment.AppendBytes(bytes=[0x01, 0xCC])
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
    action.AppendInteger(unk1, 2, 'little')
    action.AppendInteger(unk2, 2, 'little')
    action.AppendBytes(bytes=_args['packet'].data)

    # Construct final packet needed
    answer = action.data[12:(12 + _args['packet'].length - 8)]

    # Retrieve our relay client to find the room we are in
    for client in _args['client']['server'].relay.clients:
        if client['id'] == relay_id:

            # Create a reference to the game client for easier access
            game_client = client['game_client']
            game_server = client['game_server']

            # Retrieve room and slot number
            room    = game_server.rooms[str(game_client['room'])]
            slot    = room['slots'][str(get_slot({'client': game_client}, room))]

            # Retrieve the relay ids for the slot and loop through them to finally send the packet
            relay_ids = slot['relay_ids']
            for id in relay_ids:
                for client_id in _args['client']['server'].relay.clients:
                    if client_id['id'] == id:
                        _args['client']['server'].socket.sendto(answer, (client_id['peer_info']['ip'],
                                                                         client_id['peer_info']['port']))
                        break
            break