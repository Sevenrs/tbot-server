#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite

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