from Packet.Write import Write as PacketWrite

def route(client, packet):

    packets = {
        '35a0': add_peer_info
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