#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character

def request_cash(**_args):

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

'''
This method allows users to purchase gold items
'''
def purchase_gold_item(**_args):

    # Read item id from the packet
    item_id = int(_args['packet'].ReadInteger(39, 3, 'little'))

    # Attempt to find the item in the database
    _args['mysql'].execute('''SELECT `id`, `item_id`, `buyable`, `gold_price` FROM `game_items` WHERE `item_id` = %s''', [item_id])
    item = _args['mysql'].fetchone()

    # Construct purchase result packet
    result = PacketWrite()
    result.AddHeader(bytearray([0xEA, 0x2E]))

    # Define error
    error = None

    # Retrieve our inventory and check if we have a remaining slot available
    inventory       = Character.get_items(_args, _args['client']['character']['id'], 'inventory')
    available_slot  = Character.get_available_inventory_slot(inventory)

    # Define an error if the item has not been found or can not be purchased
    if item is None or item['buyable'] != 1: error = 66

    # Define another error if we have no available inventory slot for this operation
    if available_slot is None: error = 68

    # Check if we have enough currency to purchase this item
    if _args['client']['character']['currency_gigas'] < int(item['gold_price']): error = 65

    # If an error has been defined, send the error
    if error is not None:
        result.AppendBytes(bytearray([0x00]))
        result.AppendInteger(error, 1, 'little')
        return _args['socket'].send(result.packet)

    # Decrease character currency and update local state with new value
    _args['client']['character']['currency_gigas'] = _args['client']['character']['currency_gigas'] \
                                                     - int(item['gold_price'])
    _args['mysql'].execute('''UPDATE `characters` SET `currency_gigas` = (`currency_gigas` - %s) WHERE `id` = %s''', [
        int(item['gold_price']),
        _args['client']['character']['id']
    ])

    # If there are no errors, proceed to create an instance of character_items and insert the item into our inventory
    Character.add_item(_args, item, available_slot)

    # Send packet to sync the inventory and currency state
    result.AppendBytes(bytearray([0x01, 0x00]))
    result.AppendBytes([0x01, 0x00, 0x00])

    inventory = Character.get_items(_args, _args['client']['character']['id'], 'inventory')
    for item in inventory:
        result.AppendInteger(inventory[item]['id'], 4, 'little')
        result.AppendInteger(inventory[item]['duration'], 4, 'little')
        result.AppendInteger(inventory[item]['duration_type'], 1, 'little')

    for _ in range(180):
        result.AppendBytes([0x00])

    result.AppendInteger(_args['client']['character']['currency_gigas'], 4, 'little')
    _args['socket'].send(result.packet)

'''
This method allows users to wear items
'''
def wear_item(**_args):

    """
    This dictionary contains the location of the slot id in the packet as well as the command id to reply with
    Structure: packet id, [slot location, response header]
    """
    type_data = {

        # Parts
        'fc2a': [26],

        # Accessories
        '322b': [3],

        # Skills
        '342b': [3]

    }

    # Read slot number from packet
    slot = int(_args['packet'].ReadInteger(type_data[_args['packet'].id][0], 1, 'little'))

    # Retrieve our inventory to obtain more information about the item
    wearing_items   = Character.get_items(_args, _args['client']['character']['id'], 'wearing')
    inventory       = Character.get_items(_args, _args['client']['character']['id'], 'inventory')

    item = inventory[slot]

    # Check if we have anything wearing in the slot we are trying to overwrite. If we are, do not replace the inventory
    # slot with 0, but replace it with the item we are wearing
    wearing_item = 0
    for wearing_idx in wearing_items['items']:
        if item['type'] == wearing_items['items'][wearing_idx]['type']:
            wearing_item = wearing_items['items'][wearing_idx]['character_item_id']
            break

    # Wear the item we wish to wear and replace the inventory slot with nothing, or if applicable, the item we are already wearing
    _args['mysql'].execute(
        """UPDATE `character_wearing` `character` INNER JOIN `inventory` inventory ON (`character`.`id` = `inventory`.`character_id`)
            SET `character`.`{0}` = %s, `inventory`.`item_{1}` = %s
                WHERE `character`.`id` = %s""".format(item['type'], str(slot + 1)), [
            item['character_item_id'],
            wearing_item,
            _args['client']['character']['id']
        ])

    # Construct the response packet
    result = PacketWrite()
    result.AddHeader(bytearray([0x19, 0x2F]))
    result.AppendBytes([0x01, 0x00])
    result.AppendBytes(Character.construct_bot_data(_args, _args['client']['character']))
    _args['socket'].send(result.packet)