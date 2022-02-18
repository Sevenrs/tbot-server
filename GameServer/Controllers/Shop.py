#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Character
from GameServer.Controllers.data.shop import ID_GUILD_EXTEND, ID_GOLD_BAR, ID_CHANGE_RACE
from GameServer.Controllers.data.bot import *
from GameServer.Controllers import Guild

'''
This method will obtain the amount of cash a specific account has
'''
def get_cash(_args):

    # Get amount of cash from the database
    _args['mysql'].execute('SELECT `cash` FROM `users` WHERE `id` = %s', [_args['client']['account_id']])
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

    # Send the unwear packet to sync character statistics in the event that a game with custom statistics has been played
    if _args['client']['needs_sync']:
        sync = PacketWrite()
        sync.AddHeader([0xE5, 0x2E])
        sync.AppendBytes([0x01, 0x00])
        sync.AppendBytes(Character.construct_bot_data(_args, _args['client']['character']))
        _args['socket'].send(sync.packet)

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

        '022b': {"item_id_index": 38, "type": "gold", "db_info":
            {"table": "characters", "column": "currency_gigas", "where": "id", "is": _args['client']['character']['id']}},

        '042b': {"item_id_index": 40, "type": "cash", "db_info":
            {"table": "users", "column": "cash", "where": "id", "is": _args['client']['account_id']}}
    }

    # Retrieve type data
    type_data = types[_args['packet'].id]

    # Read item id from the packet
    item_id = int(_args['packet'].ReadInteger(type_data['item_id_index'], 3, 'little'))

    # Attempt to find the item in the database
    _args['mysql'].execute('''SELECT `id`, `item_id`, `buyable`, `gold_price`, `cash_price`, `part_type`, `duration` FROM `game_items` WHERE `item_id` = %s''', [item_id])
    item = _args['mysql'].fetchone()

    # Retrieve our inventory and check if we have a remaining slot available
    inventory       = Character.get_items(_args, _args['client']['character']['id'], 'inventory')
    available_slot  = Character.get_available_inventory_slot(inventory)

    # Define an error if the item has not been found or can not be purchased
    if item is None or item['buyable'] != 1:
        return sync_inventory(_args, 'purchase', 66)

    # If the item type is equal to gold or cash but there is no price for assumed type, the request should fail
    if (type_data['type'] == 'gold' and item['gold_price'] == 0) or (type_data['type'] == 'cash' and item['cash_price'] == 0):
        return sync_inventory(_args, 'purchase', 66)

    # Define another error if we have no available inventory slot for this operation
    # but only if we aren't purchasing "GuildExtend"
    if available_slot is None \
            and item['item_id'] not in ID_GUILD_EXTEND:
        return sync_inventory(_args, 'purchase', 68)

    # Retrieve currency
    currency = _args['client']['character']['currency_gigas'] if type_data['type'] == 'gold' \
        else get_cash(_args)

    # Retrieve item price
    price = item['{0}_price'.format(type_data['type'])]

    # Check if we have enough currency to afford this item
    if currency < int(price):
        return sync_inventory(_args, 'purchase', 65)

    # If we are purchasing guild extend, we'll have to validate we own a guild and that the guild is not too large (30 max)
    if item['item_id'] in ID_GUILD_EXTEND:

        # Obtain our guild
        guild = Guild.FetchGuild(_args, _args['client']['character']['id'])

        # If the guild wasn't found or we are not the leader of it, send an error
        if guild is None or guild['is_leader'] == 0:
            return sync_inventory(_args, 'purchase', 125) # Only guild masters can purchase the item

        # If the guild member count is already equal or greater than 30, we can not increase it anymore
        elif guild['max_members'] >= 30:
            return sync_inventory(_args, 'purchase', 49)

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

    # Expand our guild if we are dealing with guild expansion
    if item['item_id'] in ID_GUILD_EXTEND:

        # Expand guild max member count by 5
        _args['mysql'].execute('''UPDATE `guilds` SET `max_members` = (`max_members` + 5) WHERE `leader_character_id` = %s''', [
            _args['client']['character']['id']
        ])

    else:

        # If there are no errors, proceed to create an instance of character_items and insert the item into our inventory
        Character.add_item(_args, item, available_slot)

    # Send packet to sync the inventory and currency state
    sync_inventory(_args, 'purchase' if type_data['type'] == 'gold' else 'purchase_cash')

'''
This method will allow users to sell their items
'''
def sell_item(**_args):

    # Read slot number from the packet
    slot = int(_args['packet'].ReadInteger(38, 1, 'little'))

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
    if item['item_id'] in ID_GOLD_BAR:
        _args['mysql'].execute("""UPDATE `users` SET `cash` = (`cash` + %s) WHERE `id` = %s""", [
            item['selling_price'] / 10,
            _args['client']['account_id']
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
        'fc2a': [25, [0xE4, 0x2E]],

        # Accessories
        '322b': [2, [0x19, 0x2F]],

        # Skills
        '342b': [2, [0x1B, 0x2F]]

    }

    # Retrieve type data
    type_data = types[_args['packet'].id]

    # Read slot number from packet
    slot = int(_args['packet'].ReadInteger(type_data[0], 1, 'little'))

    # Retrieve our inventory to obtain more information about the item
    wearing_items   = Character.get_items(_args, _args['client']['character']['id'], 'wearing')
    inventory       = Character.get_items(_args, _args['client']['character']['id'], 'inventory')

    # Construct the response packet
    result = PacketWrite()
    result.AddHeader(bytearray(type_data[1]))

    # Retrieve item from the inventory
    item = inventory[slot]

    # Retrieve item from the database
    _args['mysql'].execute('''SELECT `id`, `level`, `part_type`, `bot_type` FROM `game_items` WHERE `item_id` = %s''', [
        item['id']])
    game_item = _args['mysql'].fetchone()

    # Check if the item was found. If it wasn't, send the "This item does not exist" error
    # The part type is also validated here to ensure people do not wear parts they can't wear
    # Lastly, a check is done to see if the bot type is compatible with the part that is being worn.
    if game_item is None or game_item['part_type'] == 0 \
            or (game_item['part_type'] in [1, 2, 3] and game_item['bot_type'] != _args['client']['character']['type']):
        result.AppendBytes([0x00, 0x42])
        return _args['client']['socket'].send(result.packet)

    # Check if we have the minimum level required to wear the item. If we do not meet the requirement, send an error.
    if game_item['level'] > _args['client']['character']['level']:
        result.AppendBytes([0x00, 0x65])
        return _args['client']['socket'].send(result.packet)

    # If we have a wearing merc, change the item type to merc2 to allow for wearing multiple mercs at once
    if item['type'] == 'merc1':
        for wearing_idx in wearing_items['items']:
            if wearing_items['items'][wearing_idx]['type'] == 'merc1':
                item['type'] = 'merc2'

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

    result.AppendBytes([0x01, 0x00])
    result.AppendBytes(Character.construct_bot_data(_args, _args['client']['character']))
    _args['socket'].send(result.packet)

'''
This method allows users to unwear their items
'''
def unwear_item(**_args):

    types = {

        # Parts
        'fd2a': {"type_index": 25, "types": ['head', 'body', 'arms']},
        '332b': {"type_index": 2, "types": ['mini-bot', 'gun', 'ef', 'wing', 'shield', 'shoulder', 'flag1', 'flag2']},
        '352b': {"type_index": 2, "types": ['passive_skill', 'attack_skill', 'field_pack', 'trans_pack', 'merc1', 'merc2']}
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

'''
This method will check if the user has enough cash to purchase a new warehouse/stash and will create a new one.
However, if the user has 5 stashes already, we will not be creating one.
'''
def purchase_storage(**_args):

    # Retrieve storage from the database
    _args['mysql'].execute('SELECT `cash_price` FROM `game_items` WHERE `item_id` = 5010300')
    storage = _args['mysql'].fetchone()

    # Retrieve the amount of stashes we own
    storage_count = Character.get_storage_count(_args, _args['client']['account_id'])

    # If the item was not found, send an item not found error.
    # We should also send this if we already have 5 storages
    if storage is None or storage_count >= 5:
        return sync_inventory(_args, 'purchase', 66)

    # Check if we have enough cash. Send an error if we do not have enough.
    elif storage['cash_price'] > get_cash(_args):
        return sync_inventory(_args, 'purchase', 65)

    # Create new storage for our account
    _args['mysql'].execute("""INSERT INTO `stash` (`account_id`) VALUES (%s)""", [ _args['client']['account_id']])

    # Update the currency amount
    _args['mysql'].execute('''UPDATE `users` SET `cash` = (`cash` - %s) WHERE `id` = %s''', [
        storage['cash_price'],
        _args['client']['account_id']
    ])

    # Send storage created packet
    storage_created = PacketWrite()
    storage_created.AddHeader([0x4C, 0x2F])
    storage_created.AppendBytes([0x01, 0x00])
    storage_created.AppendInteger((storage_count + 1), 2, 'little')
    _args['socket'].send(storage_created.packet)

'''
This method will sync the server's storage(stash) state with the client so that the client is aware of which items
are in the stash.
'''
def sync_storage(_args, storage_number):

    # Construct packet
    storage = PacketWrite()
    storage.AddHeader([0x4D, 0x2F])
    storage.AppendBytes([0x01, 0x00, 0x00, 0x00, 0x00])

    # Send updated inventory to the client
    inventory = Character.get_items(_args, _args['client']['character']['id'], 'inventory')
    for item in inventory:
        storage.AppendInteger(inventory[item]['id'], 4, 'little')
        storage.AppendInteger(inventory[item]['duration'], 4, 'little')
        storage.AppendInteger(inventory[item]['duration_type'], 1, 'little')

    for _ in range(180):
        storage.AppendBytes([0x00])

    # Storage number we want to send the updated state for
    storage.AppendInteger(storage_number - 1, 1, 'little')

    # Retrieve the state by storage number and send the items in the storage to the client
    storage_items = Character.get_items(_args, _args['client']['character']['id'], 'stash', storage_number)
    for item in storage_items:
        storage.AppendInteger(storage_items[item]['id'], 4, 'little')
        storage.AppendInteger(storage_items[item]['duration'], 4, 'little')
        storage.AppendInteger(storage_items[item]['duration_type'], 1, 'little')

    # Send state to the client
    _args['socket'].send(storage.packet)

'''
This method will move an item from source to target
Depending on the packet header, there will be two seperate actions.

These actions are as follows
    1. Insert:  Move an item from the inventory to the storage/stash.
    2. Draw:    Move an item from the storage/stash to the inventory.
'''
def storage_action(**_args):

    # Read source slot and storage number from the packet
    source_slot     = int(_args['packet'].ReadInteger(25, 1, 'little'))
    storage_number  = int(_args['packet'].ReadInteger(26, 1, 'little')) + 1

    # Get storage count so we can check if we actually own the storage we are trying to move to or move from.
    storage_count = Character.get_storage_count(_args, _args['client']['account_id'])

    # Drop the packet if we do not own the storage we are trying to move to or from.
    if storage_number > storage_count:
        return

    # Construct result packet in case we need to send an error
    result = PacketWrite()
    result.AddHeader([0x4D, 0x2F])

    # Determine action type based on packet ID. There are two actions, insert (add) and draw (remove).
    action_type = 'insert' if _args['packet'].id == '682b' else 'draw'

    # Get the target and an available slot within it. If the type is insert, the target will be the stash and the source will be the inventory.
    # Else, the source is the stash and the target is the inventory.
    target          = Character.get_items(_args, _args['client']['character']['id'], 'stash' if action_type == 'insert' else 'inventory', storage_number)
    available_slot  = Character.get_available_inventory_slot(target)

    # If we do not have an available slot in our target, send a slot error. This means that there is no slot for the item we wish to be moving.
    if available_slot is None:
        result.AppendBytes([0x00, 0x44]) # No available slot
        return _args['socket'].send(result.packet)

    # Get source and check if the slot is present in it. The source will be the inventory if the type is insert, else the source will be the storage/stash.
    source = Character.get_items(_args, _args['client']['character']['id'], 'inventory' if action_type == 'insert' else 'stash', storage_number)
    if source_slot not in source:
        result.AppendBytes([0x00, 0x42]) # Item not found
        return _args['socket'].send(result.packet)

    # Retrieve target item from the source slot
    item = source[source_slot]

    # Move the item from the source to the target
    _args['mysql'].execute('''  UPDATE `stash` stash INNER JOIN `inventory` inventory ON (inventory.`character_id` = %s)
                                    SET stash.`item_{0}` = %s, inventory.`item_{1}` = %s
                                WHERE stash.`id` = (
                                    SELECT `id` FROM `stash` WHERE `account_id` = %s
                                        ORDER BY `id` ASC LIMIT 1 OFFSET {2}
                                )'''.format(

        # This parameter will determine which slot to change in the storage itself.
        # If the action type is insert, the target will be the storage/stash and the source will be the inventory.
        #   Which means, the slot used here will be the available target slot

        # Otherwise, the source is the storage/stash and the target will be the inventory.
        #   Which means, the slot used here will be the slot the item comes from.
        available_slot + 1 if action_type == 'insert' else source_slot + 1,

        # This parameter will determine which slot to change in the inventory.
        # If the action type is insert, the source will be inventory and the target will be the storage/stash
        #   Which means, the slot used here will be the slot where the item comes from.

        # Otherwise, the target will be the inventory
        #   Which means that the item will come from the stash/storage and will be saved to the inventory.
        (source_slot + 1) if action_type == 'insert' else available_slot + 1,


        (storage_number - 1)    # Calculate offset, should start at 0
    ), [
        _args['client']['character']['id'],

        # If the action type is insert, we must move the item to the stash. Otherwise, we must remove the item from
        # the storage/stash.
        item['character_item_id'] if action_type == 'insert' else 0,

        # If the action type is insert, we must remove the item from the inventory. Otherwise, we must move the item
        # to the inventory.
        item['character_item_id'] if action_type == 'draw' else 0,

        _args['client']['account_id']
    ])

    # Send the updated storage state to the client
    return sync_storage(_args, storage_number)

'''
This method will allow users to combine their body, arm and head parts.
'''
def union_parts(**_args):

    # Read coupon slot from packet
    coupon_slot = int(_args['packet'].ReadInteger(2, 1, 'little'))

    # Read item slots from packet
    item_1_slot = int(_args['packet'].ReadInteger(3, 1, 'little'))
    item_2_slot = int(_args['packet'].ReadInteger(4, 1, 'little'))
    item_3_slot = int(_args['packet'].ReadInteger(5, 1, 'little'))

    # Check against duplicates. It could be possible for a client to send the same slots for each item.
    if len(set([item_1_slot, item_2_slot, item_3_slot])) != len([item_1_slot, item_2_slot, item_3_slot]):
        return sync_inventory(_args, 'sell', 61)  # Request refused

    # Retrieve the inventory of our character so we can validate if everything's correct
    inventory = Character.get_items(_args, _args['client']['character']['id'], 'inventory')

    # Check if the slot number for the coupon actually contains the union coupon
    if coupon_slot not in inventory or inventory[coupon_slot]['id'] != 5041200:
        return sync_inventory(_args, 'sell', 66) # Item not found

    # Check if the first item is a valid item. It has to be either a body, arm or head (and must actually exist)
    if item_1_slot not in inventory or inventory[item_1_slot]['type'] not in ['head', 'body', 'arms']:
        return sync_inventory(_args, 'sell', 61) # Request refused

    # Validate the remaining items. Compare them against the first item
    for slot in [item_2_slot, item_3_slot]:

        # Check if the item is really in the inventory
        if slot not in inventory:
            return sync_inventory(_args, 'sell', 66)  # Item not found

        # Check if the item id is the same item id as the first item
        elif inventory[slot]['id'] != inventory[item_1_slot]['id']:
            return sync_inventory(_args, 'sell', 61)  # Request refused

    # If the first item is already +5, the items can not be upgraded any more. At this point we are sure they're all equal.
    if int(str(inventory[item_1_slot]['id'])[-1:]) >= 5:
        return sync_inventory(_args, 'sell', 72)  # Item can not be upgraded anymore

    # Find new item in the database. If the item does not exist, do not proceed.
    _args['mysql'].execute('''SELECT `id` FROM `game_items` WHERE `item_id` = (%s + 1)''', [
        inventory[item_1_slot]['id'],
    ])
    item = _args['mysql'].fetchone()

    # If the new item does not exist, do not proceed.
    if item is None:
        return sync_inventory(_args, 'sell', 66)  # Item not found

    # If the coupon has expired, remove it.
    if inventory[coupon_slot]['duration'] == 1:
        Character.remove_item(_args, inventory[coupon_slot]['character_item_id'], coupon_slot)
    else:

        # Otherwise, decrease remaining_times by one
        _args['mysql'].execute(
            '''UPDATE `character_items` SET `remaining_times` = (`remaining_times` - 1) WHERE `id` = %s''', [
                inventory[coupon_slot]['character_item_id']
            ]
        )

    # Delete secondary and third items
    for slot in [item_2_slot, item_3_slot]:
        Character.remove_item(_args, inventory[slot]['character_item_id'], slot)

    # Upgrade first item
    _args['mysql'].execute("""UPDATE `character_items` SET `game_item` = %s WHERE `id` = %s""", [
        item['id'], inventory[item_1_slot]['character_item_id']])

    # Send character information
    result = PacketWrite()
    result.AddHeader([0xE4, 0x2E])
    result.AppendBytes([0x01, 0x00])
    result.AppendBytes(Character.construct_bot_data(_args, _args['client']['character']))
    _args['socket'].send(result.packet)

'''
This method will allow users to change their Bot's Race if they own the transformation coupon
'''
def change_race(**_args):

    # Read new bot type from packet
    new_type = int(_args['packet'].ReadInteger(2, 1, 'little'))

    # Check if the new bot type is valid and check if the new bot type does not equal our own
    if new_type not in [TYPE_PATCH, TYPE_SURGE, TYPE_RAM] or new_type == _args['client']['character']['type']:
        return sync_inventory(_args, 'sell', 61)  # Request refused

    # Retrieve the user's inventory and wearing items
    inventory   = Character.get_items(_args, _args['client']['character']['id'], 'inventory')
    wearing     = Character.get_items(_args, _args['client']['character']['id'], 'wearing')

    # Attempt to find the first instance of the transformation coupon in the user's inventory
    item_coupon, coupon_slot = None, None
    for idx, item in enumerate(inventory):
        if inventory[item]['id'] == ID_CHANGE_RACE:
            item_coupon = inventory[item]
            coupon_slot = idx
            break

    # If the coupon hasn't been found, refuse to process the request.
    if item_coupon is None:
        return sync_inventory(_args, 'sell', 61)  # Request refused

    # Container with update statements to execute after part validation.
    # We wish to update the part's race type only after we've ensured that they are available for the other type
    part_updates = []

    for i in range(3):

        # Retrieve the item from the wearing array
        item = wearing['items'][i]

        # There is no need to validate the item if its id is equal to 0
        if item['id'] == 0:
            continue

        # Construct new item id with the new_type in mind
        new_id = int(str(item['id'])[:1] + str(new_type) + str(item['id'])[2:])

        # Retrieve new item from the database, check if it exists and fetch the new item
        _args['mysql'].execute('''SELECT `id` FROM `game_items` WHERE `item_id` = %s''', [new_id])
        new_item = _args['mysql'].fetchone()

        # If the new item does not exist, refuse the request
        if new_item is None:
            return sync_inventory(_args, 'sell', 61)  # Request refused

        # If the item was found, add it to the part update array
        part_updates.append({'character_item_id': item['character_item_id'], 'new_id': new_item['id']})

    # Perform the item updates so that they are compatible with the new bot type
    for update in part_updates:
        _args['mysql'].execute('''UPDATE `character_items` SET `game_item` = %s WHERE `id` = %s''', [
            update['new_id'],
            update['character_item_id']
        ])

    # Change our bot type to the new type
    _args['client']['character']['type'] = new_type
    _args['mysql'].execute('''UPDATE `characters` SET `type` = %s WHERE `id` = %s''', [
        new_type,
        _args['client']['character']['id']
    ])

    # If the coupon has expired, remove it.
    if item_coupon['duration'] == 1:
        Character.remove_item(_args, item_coupon['character_item_id'], coupon_slot)
    else:

        # Otherwise, decrease remaining_times by one
        _args['mysql'].execute(
            '''UPDATE `character_items` SET `remaining_times` = (`remaining_times` - 1) WHERE `id` = %s''', [
                item_coupon['character_item_id']
            ]
        )

    # Construct and send type changed packet
    type_changed = PacketWrite()
    type_changed.AddHeader([0x57, 0x2F])
    type_changed.AppendBytes([0x01, 0x00])
    type_changed.AppendInteger(new_type, 1, 'little')

    for _ in range(6):
        type_changed.AppendBytes([0x00])

    # Retrieve and send inventory
    inventory = Character.get_items(_args, _args['client']['character']['id'], 'inventory')
    for item in inventory:
        type_changed.AppendInteger(inventory[item]['id'], 4, 'little')
        type_changed.AppendInteger(inventory[item]['duration'], 4, 'little')
        type_changed.AppendInteger(inventory[item]['duration_type'], 1, 'little')

    # Padding between inventory and wearing items
    for _ in range(180):
        type_changed.AppendBytes([0x00])

    # Retrieve and send wearing head, body and arms
    wearing_items = Character.get_items(_args, _args['client']['character']['id'], 'wearing')
    for i in range(0, 3):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        type_changed.AppendInteger(item['id'], 4, 'little')
        type_changed.AppendInteger(item['duration'], 4, 'little')
        type_changed.AppendInteger(item['duration_type'], 1, 'little')

    # Send type changed packet to the client
    _args['socket'].send(type_changed.packet)

    # Send item equip packet so that the character's statistics will be synced
    sync_stats = PacketWrite()
    sync_stats.AddHeader([0xE4, 0x2E])
    sync_stats.AppendBytes([0x01, 0x00])
    sync_stats.AppendBytes(Character.construct_bot_data(_args, _args['client']['character']))
    _args['socket'].send(sync_stats.packet)