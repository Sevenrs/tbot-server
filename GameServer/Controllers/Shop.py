#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character

def RequestCash(**_args):

    # Get amount of cash(coins) from the database
    _args['mysql'].execute('SELECT `cash` FROM `users` WHERE `username` = %s', [
        _args['client']['account']
    ])
    
    # Fetch the result
    result = _args['mysql'].fetchone()
    
    # Create coin packet and send it to our client
    coin_packet = PacketWrite()
    coin_packet.AddHeader(bytearray([0x37, 0x2F]))
    coin_packet.AppendBytes(bytearray([0x01, 0x00]))
    coin_packet.AppendInteger(result['cash'], 4, 'little')
    _args['socket'].send(coin_packet.packet)

    # Test giga purchase packet
    test = PacketWrite()
    test.AddHeader(bytearray([0xEA, 0x2E]))
    test.AppendBytes(bytearray([0x01, 0x00]))
    test.AppendBytes([0x01, 0x00, 0x00])

    inventory = Character.get_items(_args, _args['client']['character']['id'], 'inventory')
    for item in inventory:
        test.AppendInteger(inventory[item]['id'], 4, 'little')
        test.AppendInteger(inventory[item]['duration'], 4, 'little')
        test.AppendInteger(inventory[item]['duration_type'], 1, 'little')

    for _ in range(180):
        test.AppendBytes([0x00])

    test.AppendInteger(42069, 4, 'little')
    #_args['socket'].send(test.packet)