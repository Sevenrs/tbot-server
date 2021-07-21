#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character

'''
This method will obtain the amount of cash a specific account has
'''
def get_cash(_args):

    # Get amount of cash from the database
    _args['mysql'].execute('SELECT `cash` FROM `users` WHERE `username` = %s', [
        _args['client']['account']
    ])

    return _args['mysql'].fetchone()['cash']

def sync_cash(_args):

    # Get cash amount
    cash = get_cash(_args)

    # Create coin packet and send it to our client
    coin_packet = PacketWrite()
    coin_packet.AddHeader(bytearray([0x37, 0x2F]))
    coin_packet.AppendBytes(bytearray([0x01, 0x00]))
    coin_packet.AppendInteger(cash, 4, 'little')
    _args['socket'].send(coin_packet.packet)

def sync_cash_rpc(**_args):
    sync_cash(_args)
    sync_inventory(_args)

'''
This method will sync the inventory.
'''
def sync_inventory(_args, type='sell', state=1):

    # Packet types
    types = {'sell': 0xEB, 'purchase':  0xEA, 'purchase_cash': 0xEC}

    # Construct response packet
    result = PacketWrite()
    result.AddHeader([types[type], 0x2E])

    # Construct state
    result.AppendInteger(state if state == 1 else 0, 1, 'little')
    result.AppendInteger(0 if state == 1 else state, 1, 'little')

    # If there is an error, send the packet right now.
    if state != 1:
        _args['socket'].send(result.packet)
        return

    # Otherwise, continue constructing the packet
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
This method allows users to purchase items
'''
def purchase_item(**_args):

    """ This dictionary contains what packet belongs to which item type.
        Each item type has a different item id index. We'll also define what is which for later usage.

       Additionally, there is a database information field for dynamic query construction as we need to update
       different values in different places for different conditions """
    types = {

        '022b': {"item_id_index": 39, "type": "gold", "db_info":
            {"table": "characters", "column": "currency_gigas", "where": "id", "is": _args['client']['character']['id']}},

        '042b': {"item_id_index": 41, "type": "cash", "db_info":
            {"table": "users", "column": "cash", "where": "username", "is": _args['client']['account']}}
    }

    # Retrieve type data
    type_data = types[_args['packet'].id]

    # Read item id from the packet
    item_id = int(_args['packet'].ReadInteger(type_data['item_id_index'], 3, 'little'))

    # Attempt to find the item in the database
    _args['mysql'].execute('''SELECT `id`, `item_id`, `buyable`, `gold_price`, `cash_price`, `part_type`, `duration` FROM `game_items` WHERE `item_id` = %s''', [item_id])
    item = _args['mysql'].fetchone()

    # Construct purchase result packet
    result = PacketWrite()
    result.AddHeader(bytearray([0xEA, 0x2E]))

    # Retrieve our inventory and check if we have a remaining slot available
    inventory       = Character.get_items(_args, _args['client']['character']['id'], 'inventory')
    available_slot  = Character.get_available_inventory_slot(inventory)

    # Define an error if the item has not been found or can not be purchased
    if item is None or item['buyable'] != 1:

        # temporary
        if item is not None:
                _args['mysql'].execute("""UPDATE `game_items` SET `buyable` = 1 WHERE id = %s""", [item['id']])

        return sync_inventory(_args, 'purchase', 66)

    # If the item type is equal to gold or cash but there is no price for assumed type, the request should fail
    if (type_data['type'] == 'gold' and item['gold_price'] == 0) or (type_data['type'] == 'cash' and item['cash_price'] == 0):
        return sync_inventory(_args, 'purchase', 66)

    # Define another error if we have no available inventory slot for this operation
    if available_slot is None:
        return sync_inventory(_args, 'purchase', 68)

    # Retrieve currency
    currency = _args['client']['character']['currency_gigas'] if type_data['type'] == 'gold' \
        else get_cash(_args)

    # Retrieve item price
    price = item['{0}_price'.format(type_data['type'])]

    # Check if we have enough currency to afford this item
    if currency < int(price):
        return sync_inventory(_args, 'purchase', 65)

    # Only update the local value if the type is equal to gold because we use that at other places
    if type_data['type'] == 'gold':
        _args['client']['character']['currency_gigas'] = _args['client']['character']['currency_gigas'] \
                                                         - int(item['gold_price'])

    # Update the database with our new currency value
    _args['mysql'].execute('''UPDATE `{0}` SET `{1}` = (`{1}` - %s) WHERE `{2}` = %s'''.format(
        type_data['db_info']['table'],
        type_data['db_info']['column'],
        type_data['db_info']['where']),
            [int(price), type_data['db_info']['is']])

    # If there are no errors, proceed to create an instance of character_items and insert the item into our inventory
    Character.add_item(_args, item, available_slot)

    # Send packet to sync the inventory and currency state
    sync_inventory(_args, 'purchase' if type_data['type'] == 'gold' else 'purchase_cash')

'''
This method will allow users to sell their items
'''
def sell_item(**_args):

    # Read slot number from the packet
    slot = int(_args['packet'].ReadInteger(39, 1, 'little'))

    # Retrieve inventory and the item
    inventory       = Character.get_items(_args, _args['client']['character']['id'], 'inventory')
    inventory_item  = inventory[slot]

    # If the inventory item is equal to 0, the item does not exist
    if inventory_item == 0:
        return sync_inventory(_args, 'sell', 66)

    # Retrieve item selling price from the database
    _args['mysql'].execute('''SELECT `id`, `item_id`, `selling_price` FROM `game_items` WHERE `item_id` = %s''', [
        inventory_item['id']])
    item = _args['mysql'].fetchone()

    # If the item hasn't been found, there was an error
    if item is None:
        return sync_inventory(_args, 'sell', 66)

    # Gold bars should give cash points
    if item['item_id'] in [6000001, 6000002, 6000003]:
        _args['mysql'].execute("""UPDATE `users` SET `cash` = (`cash` + %s) WHERE `username` = %s""", [
            item['selling_price'] / 10,
            _args['client']['account']
        ])
    else:

        # Increase our currency by the selling amount by mutating our local variable and pushing it to the database as well
        _args['client']['character']['currency_gigas'] = _args['client']['character']['currency_gigas'] + int(item['selling_price'])
        _args['mysql'].execute("""UPDATE `characters` SET `currency_gigas` = (`currency_gigas` + %s) WHERE `id` = %s""", [
            int(item['selling_price']),
            _args['client']['character']['id']
        ])

    # Remove item from our inventory and from character_items
    Character.remove_item(_args, inventory_item['character_item_id'], slot)

    # Create response packet and send it to our socket
    sync_cash(_args)
    sync_inventory(_args, 'sell')


'''
This method allows users to wear their items
'''
def wear_item(**_args):

    """
    This dictionary contains the location of the slot id in the packet as well as the command id to reply with
    Structure: packet id, [slot packet index, response header]
    """
    types = {

        # Parts
        'fc2a': [26, [0xE4, 0x2E]],

        # Accessories
        '322b': [3, [0x19, 0x2F]],

        # Skills
        '342b': [3, [0x1B, 0x2F]]

    }

    # Retrieve type data
    type_data = types[_args['packet'].id]

    # Read slot number from packet
    slot = int(_args['packet'].ReadInteger(type_data[0], 1, 'little'))

    # Retrieve our inventory to obtain more information about the item
    wearing_items   = Character.get_items(_args, _args['client']['character']['id'], 'wearing')
    inventory       = Character.get_items(_args, _args['client']['character']['id'], 'inventory')

    item = inventory[slot]

    print(slot)
    print(item)

    # Check if we have anything wearing in the slot we are trying to overwrite. If we are, do not replace the inventory
    # slot with 0, but replace it with the item we are wearing
    wearing_item = 0
    for wearing_idx in wearing_items['items']:
        if item['type'] == wearing_items['items'][wearing_idx]['type']:
            wearing_item = wearing_items['items'][wearing_idx]['character_item_id']
            break

    ''' If the item has a used state, update it to 1 (if not already updated) and calculate the expiration.
        If we have the amount of remaining seconds stored, use that to calculate the expiration.
        Otherwise, base the expiration off of the duration in game_items instead.'''
    _args['mysql'].execute("""UPDATE `character_items` SET `used` = 1, 
                expiration_date = IF(`remaining_seconds` IS NULL,
                                                                    DATE_ADD(UTC_TIMESTAMP(), INTERVAL (SELECT `duration` FROM `game_items` WHERE `id` = `game_item`) DAY),
                                                                    DATE_ADD(UTC_TIMESTAMP(), INTERVAL `remaining_seconds` SECOND)
                                    ),
                                    `remaining_seconds` = NULL
                                    WHERE `id` = %s AND `used` IS NOT NULL""", [
        item['character_item_id']
    ])

    # If the wearing item is not equal to zero and it has an expire date, calculate the amount of remaining seconds
    if wearing_item != 0:
        unwear_item_calculate_seconds(_args, wearing_item)

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
    result.AddHeader(bytearray(type_data[1]))
    result.AppendBytes([0x01, 0x00])
    result.AppendBytes(Character.construct_bot_data(_args, _args['client']['character']))
    _args['socket'].send(result.packet)

'''
This method allows users to unwear their items
'''
def unwear_item(**_args):

    types = {

        # Parts
        'fd2a': {"type_index": 26, "types": ['head', 'body', 'arms']},
        '332b': {"type_index": 3, "types": ['mini-bot', 'gun', 'ef', 'wing', 'shield', 'shoulder', 'flag1', 'flag2']},
        '352b': {"type_index": 3, "types": ['passive_skill', 'attack_skill', 'field_pack', 'trans_pack', 'merc1', 'merc2']}
    }

    # Retrieve data based on packet id
    data = types[_args['packet'].id]

    # Retrieve item type from the starting index of the packet
    type = data['types'][int(_args['packet'].ReadInteger(data['type_index'], 1, 'little'))]

    # Construct response packet
    result = PacketWrite()
    result.AddHeader([0xE5, 0x2E])

    # Retrieve inventory and the first free inventory slot to put our item in
    inventory       = Character.get_items(_args, _args['client']['character']['id'], 'inventory')
    available_slot  = Character.get_available_inventory_slot(inventory)

    # Return an error if we do not have a slot available for the item to go in
    if available_slot is None:
        result.AppendBytes([0x00, 0x44])
        return _args['socket'].send(result.packet)

    # Retrieve our wearing items so we know what to remove
    wearing = Character.get_items(_args, _args['client']['character']['id'], 'wearing')

    ''' Construct a dictionary with all items. It is constructed as following: 'type': character_item_id
        for easy access and manipulation of the state '''
    items = {}
    for idx in wearing['items']:
        if wearing['items'][idx]['type'] is not None:
            items[wearing['items'][idx]['type']] = wearing['items'][idx]['character_item_id']

    # If the item type we are trying to find is in the dictionary, use the found item id
    wearing_item = items[type] if type in items else 0

    # If the type is equal to head and a coin head exists, the wearing item id should become the coin head's id
    if type == 'head' and 'coin_head' in items:
        wearing_item, type = items['coin_head'], 'coin_head'

    # If the type is equal to mini-bot and a coin_minibot exists, the wearing item id should become that
    elif type == 'mini-bot' and 'coin_minibot' in items:
        wearing_item, type = items['coin_minibot'], 'coin_minibot'

    # Remove the item from our wearing table and send the character information in case our wearing item is not equal to 0
    if wearing_item != 0:
        _args['mysql'].execute(
            """UPDATE `character_wearing` `character` INNER JOIN `inventory` inventory ON (`character`.`id` = `inventory`.`character_id`)
                SET `character`.`{0}` = 0, `inventory`.`item_{1}` = %s
                    WHERE `character`.`id` = %s""".format(type, str(available_slot + 1)), [
                wearing_item,
                _args['client']['character']['id']
            ])

        # In case the item has a used state and the expiration date is set, calculate the remaining seconds and store that.
        # We need this because we do not want to let the time keep going after the user has unweared an item
        unwear_item_calculate_seconds(_args, wearing_item)

    # Send character information back to our client and the removal is complete
    result.AppendBytes([0x01, 0x00])
    result.AppendBytes(Character.construct_bot_data(_args, _args['client']['character']))
    _args['socket'].send(result.packet)

'''
In case the item has a used state and the expiration date is set, calculate the remaining seconds and store that.
We need this because we do not want to let the time keep going after the user has unweared an item
'''
def unwear_item_calculate_seconds(_args, wearing_item):
    _args['mysql'].execute("""UPDATE `character_items`
                    SET     `remaining_seconds` = TIMESTAMPDIFF(SECOND, UTC_TIMESTAMP(), `expiration_date`),
                            `expiration_date` = NULL
                WHERE `id` = %s AND `used` IS NOT NULL""", [wearing_item])