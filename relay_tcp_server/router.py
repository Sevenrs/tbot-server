from Packet.Write import Write as PacketWrite
from GameServer.Controllers.Room import get_slot

def route(client, packet):

    packets = {
        '32a0': id_request,
        '36a0': check_connection,
        '37a0': remove_connection
    }.get(packet.id, unknown)(**locals())

'''
Handle unknown packets by redirecting its contents to stdout
'''
def unknown(**_args):
    print("[{0}]: Unknown packet: <0x{1}[len={3}]::{2}>".format(_args['client']['server'].name, _args['packet'].id,
                                                                _args['packet'].data, len(_args['packet'].data)))
'''
Retrieve first available ID and register the client for later access
'''
def id_request(**_args):

    # Retrieve first available ID
    id = 0
    for i in range(65535):
        if i in _args['client']['server'].ids:
            continue

        id = i
        _args['client']['server'].ids.append(id)
        break

    account = _args['packet'].ReadString()[1:]

    # Fill our client object with relevant information
    _args['client']['account']  = account
    _args['client']['id']       = id

    # Add the client to our client container
    _args['client']['server'].clients.append(_args['client'])

    # Send response to client
    result = PacketWrite()
    result.AddHeader(bytes=[0x1A, 0xA4])
    result.AppendBytes([0x01, 0x00])
    result.AppendBytes([id & 0xFF, id >> 8 & 0xFF])
    _args['client']['socket'].send(result.packet)

def check_connection(**_args):

    #client_id   = int(_args['packet'].ReadInteger(0, 2, 'big'))
    #room_number = int(_args['packet'].ReadInteger(4, 2, 'big'))

    for i in range(0, 8):
        start = (17 * i) + 8

        connected       = int(_args['packet'].ReadInteger(start + 2, 1, 'little'))
        character_name  = _args['packet'].ReadStringByRange(start + 2, (start + 17))

        if connected == 0 and len(character_name) > 0:
            room = _args['client']['game_server'].rooms[str(_args['client']['game_client']['room'])]

            # Find our slot
            slot_nr = get_slot({'client': _args['client']['game_client']}, room)
            room_slot = room['slots'][str(slot_nr)]

            # Add relay ID of the player that is not connected
            for client in _args['client']['server'].clients:
                if client['game_client']['character']['name'] == character_name:
                    room_slot['relay_ids'].append(client['id'])

            print(room_slot)

        print("connected for {0} is {1}".format(character_name, connected))

def remove_connection(**_args):
    character_name  = _args['packet'].ReadStringByRange(2, 17)

    # Remove relay ID from the room
    for client in _args['client']['server'].clients:
        if client['game_client']['character']['name'] == character_name:

            # Find our own room and slot number and remove the relay ID from the list
            room = _args['client']['game_server'].rooms[str(_args['client']['game_client']['room'])]
            slot_nr = get_slot({'client': _args['client']['game_client']}, room)
            room_slot = room['slots'][str(slot_nr)]
            room_slot['relay_ids'].remove(client['id'])