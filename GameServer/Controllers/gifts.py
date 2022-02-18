#!/usr/bin/env python3
__author__      = 'Icseon'
__copyright__   = 'Copyright (C) 2021 Icseon'
__version__     = '1.0'

from Packet.Write import Write as PacketWrite
from GameServer.Controllers.Character import get_items, get_available_inventory_slot, add_item
from GameServer.Controllers.Shop import get_cash, sync_cash, sync_inventory
from GameServer.Controllers.data.gifts import TYPE_ITEM, TYPE_GOLD, TYPE_OIL

'''
This handler is responsible for handling the gift functionality
'''

'''
Method:         sync_state
Description:    This method will send the latest currency and inventory data to the client
'''
def sync_state(_args):

    # Create sync result packet and send it to the client
    result = PacketWrite()
    result.AddHeader([0x16, 0x2F])
    result.AppendBytes([0x01, 0x00])

    # Send current currency values
    result.AppendInteger(_args['client']['character']['currency_gigas'], 4, 'little')
    result.AppendInteger(_args['client']['character']['currency_botstract'], 4, 'little')

    for _ in range(15):
        result.AppendBytes([0x00])

    # Send inventory
    inventory = get_items(_args, _args['client']['character']['id'], 'inventory')
    for item in inventory:
        result.AppendInteger(inventory[item]['id'], 4, 'little')
        result.AppendInteger(inventory[item]['duration'], 4, 'little')
        result.AppendInteger(inventory[item]['duration_type'], 1, 'little')

    _args['socket'].send(result.packet)

'''
Method:         get_gifts_rpc
Description:    This method will handle the request sent by the client
Debug symbol:   CGiftManagement::RequestPostList()
'''
def get_gifts_rpc(**_args):
    get_gifts(_args)

'''
Method:         get_gifts
Description:    This method will retrieve all gifts from the database and send a response to the client
'''
def get_gifts(_args):

    # Obtain all gifts that our character has received
    _args['mysql'].execute('''SELECT g.`id`, IFNULL(c.`name`, '( deleted )') AS `sender`, g.`date`, g.`message`, g.`type`,
        g.`item_1` AS `contents` FROM `gifts` g
            LEFT JOIN `characters` c ON c.`id` = g.`sender`
        WHERE g.`receiver` = %s ORDER BY g.`id` DESC LIMIT 20''', [
        _args['client']['character']['id']
    ])

    # Fetch gifts into a usable object
    gifts = _args['mysql'].fetchall()

    # Construct response packet
    result = PacketWrite()
    result.AddHeader([0x15, 0x2F])
    result.AppendBytes([0x01, 0x00])

    for index, gift in enumerate(gifts):
        result.AppendString(gift['sender'], 15)
        result.AppendString(gift['message'], 31)

        # Is the gift type gold/gigas? Append the contents at the bytes reserved for gold/gigas.
        if gift['type'] == TYPE_GOLD:
            result.AppendInteger(gift['contents'], 4, 'little')
        else:
            for _ in range(4): result.AppendBytes([0x00])

        # Is this gift an item? Append the item ID, duration and duration type
        if gift['type'] == TYPE_ITEM:

            # Retrieve item and add it to the packet
            item = get_items(_args, _args['client']['character']['id'], 'gifts', gift['id'])[0]

            result.AppendInteger(item['id'], 4, 'little')
            result.AppendInteger(item['duration'], 4, 'little')
            result.AppendInteger(item['duration_type'], 1, 'little')
        else:
            for _ in range(9): result.AppendBytes([0x00])

        # In case the gift is oil, append the amount of oil to the packet in this offset
        if gift['type'] == TYPE_OIL:
            result.AppendInteger(gift['contents'], 4, 'little')
        else:
            for _ in range(4): result.AppendBytes([0x00])

        # Padding bytes
        for _ in range(12):
            result.AppendBytes([0x00])

        # Gift date and padding byte
        result.AppendString(gift['date'].strftime('%Y%m%d%H%M'), 12)
        result.AppendBytes([0x00])

    # If we do not have 20 gifts, we'll have to add null bytes for those we do not have
    for _ in range(0, (20 - len(gifts))):
        for _ in range(88):
            result.AppendBytes([0x00])

    # Send list to client
    _args['socket'].send(result.packet)

'''
Method:         receive_gift
Description:    This method will receive gifts. For items, it would move the item from the gift to the inventory and for the rest, the currency would be updated.
'''
def receive_gift(**_args):

    # Read gift offset from packet
    gift_offset = int(_args['packet'].ReadInteger(4, 1, 'little'))

    # Find gift and select id, type and item_1 (contents)
    _args['mysql'].execute('''SELECT `id`, `type`, `item_1` AS `contents` FROM `gifts` WHERE `receiver` = %s ORDER BY `id` DESC LIMIT 1 OFFSET %s''', [
        _args['client']['character']['id'],
        gift_offset
    ])

    # Fetch gift
    gift = _args['mysql'].fetchone()

    # Construct response packet for errors
    error = PacketWrite()
    error.AddHeader([0x15, 0x2F])
    error.AppendBytes([0x00])

    # If the gift wasn't found, send an error
    if gift is None:
        error.AppendBytes([0x42]) # Item does not exist
        return _args['socket'].send(error.packet)

    # Handle item gifts
    if gift['type'] == TYPE_ITEM:

        # Retrieve inventory and available slot
        inventory       = get_items(_args, _args['client']['character']['id'], 'inventory')
        available_slot  = get_available_inventory_slot(inventory)

        # If we do not have an available inventory slot, send an error indicating that it is full
        if available_slot is None:
            error.AppendBytes([0x44]) # No available slot
            return _args['socket'].send(error.packet)

        # Move item to inventory
        _args['mysql'].execute('''UPDATE `inventory` SET `item_{0}` = %s WHERE `character_id` = %s'''.format(str(available_slot + 1)), [
            gift['contents'],
            _args['client']['character']['id']
        ])

    # Handle gold and oil gifts
    elif gift['type'] in [TYPE_GOLD, TYPE_OIL]:

        # Determine what column we need to update based on the gift type
        currency = 'currency_gigas' if gift['type'] == TYPE_GOLD else 'currency_botstract'

        # Update character to have the new currency amount
        _args['mysql'].execute('''UPDATE `characters` SET `{0}` = ({0} + %s) WHERE `id` = %s'''.format(currency), [
            int(gift['contents']),
            _args['client']['character']['id']
        ])

        # Update local state with the new currency amount
        _args['client']['character'][currency] += int(gift['contents'])

    # Delete gift as it has been received
    _args['mysql'].execute('''DELETE FROM `gifts` WHERE `id` = %s''', [
        gift['id']
    ])

    # Send updated list to client
    get_gifts(_args)
    sync_state(_args)

'''
Method:         send_gift
Description:    This method allows users to send gifts through the lobby
'''
def send_gift(**_args):

    # Read sender and receiver from the packet
    sender      = _args['packet'].ReadString(4) # This will not be used in practice, we are already aware of who we are.
    receiver    = _args['packet'].ReadString(3).strip()

    # Create result packet
    result = PacketWrite()
    result.AddHeader([0x16, 0x2F])

    # Attempt to find the receiver's character ID
    _args['mysql'].execute('SELECT `id` FROM `characters` WHERE `name` = %s', [
        receiver
    ])

    # Fetch the receiver's character
    receiver_character = _args['mysql'].fetchone()

    ''' If the character does not exist or the ID equals our own or the client is trying to send a gift to themselves
        send back a bot name error. '''
    if receiver_character is None or receiver_character['id'] == _args['client']['character']['id'] \
        or receiver.lower() == _args['client']['character']['name'].lower():
            result.AppendBytes([0x00, 0x33])
            return _args['socket'].send(result.packet)

    # Read gift message, type and contents
    message     = _args['packet'].ReadString()
    gift_type   =  int(_args['packet'].ReadInteger(2, 1, 'little'))

    # Each gift type has a different content position in the packet.
    # We'll have to retrieve the content number based on the offset given in the list below.
    gift_data = {
        TYPE_ITEM:  {'content_offset': 64},
        TYPE_GOLD:  {'content_offset': 68},
        TYPE_OIL:   {'content_offset': 72}
    }

    # Check if the gift type is valid
    if gift_type not in gift_data.keys():
        result.AppendBytes([0x00, 0x05])
        return _args['socket'].send(result.packet)

    # Default gift content variable. This variable should be overwritten.
    # Will be stored in the database.
    content = 0

    # Read gift content
    gift_content = int(_args['packet'].ReadInteger(gift_data[gift_type]['content_offset'], 4, 'little'))

    # Handle item gifts
    if gift_type == TYPE_ITEM:

        # Retrieve inventory
        inventory = get_items(_args, _args['client']['character']['id'], 'inventory')

        # Check if there is an item in the inventory slot we received
        if gift_content not in inventory:
            result.AppendBytes([0x00, 0x42]) # Item not found
            return _args['socket'].send(result.packet)

        # Fetch item and set content value
        item    = inventory[gift_content]
        content = item['character_item_id']

        # Remove item from our inventory
        _args['mysql'].execute('''UPDATE `inventory` SET `item_{0}` = 0 WHERE `character_id` = %s'''.format(str(gift_content + 1)), [
            _args['client']['character']['id']
        ])

    # Handle gold and oil gifts
    elif gift_type in [TYPE_GOLD, TYPE_OIL]:

        # Determine currency type based on the gift type
        currency = 'currency_gigas' if gift_type == TYPE_GOLD else 'currency_botstract'

        # Check if we have enough currency for this operation
        if int(gift_content) > _args['client']['character'][currency]:
            result.AppendBytes([0x00, 0x41])
            return _args['socket'].send(result.packet)

        # Set gift content value
        content = int(gift_content)

         # Update character to have the new currency amount
        _args['mysql'].execute('''UPDATE `characters` SET `{0}` = ({0} - %s) WHERE `id` = %s'''.format(currency), [
            int(gift_content),
            _args['client']['character']['id']
        ])

        # Update local state with the new currency amount
        _args['client']['character'][currency] -= int(gift_content)

    # Save gift for the receiver to use
    _args['mysql'].execute('''INSERT INTO `gifts` (`sender`, `receiver`, `date`, `message`, `type`, `item_1`)
        VALUES (%s, %s, UTC_TIMESTAMP(), %s, %s, %s)''', [
        _args['client']['character']['id'],
        receiver_character['id'],
        message,
        gift_type,
        content
    ])

    # Send success packet to the client
    sync_state(_args)

'''
Method:         purchase_gift
Description:    This method allows users to send gifts through the shop
                The user will directly purchase an item and gift it without it ever reaching their inventory
'''
def purchase_gift(**_args):

    # Read information from incoming packet
    sender      = _args['packet'].ReadString(3)  # This will not be used in practice, we are already aware of who we are.
    receiver    = _args['packet'].ReadString().strip()
    message     = _args['packet'].ReadString()
    item_id     = int(_args['packet'].ReadInteger(70, 3, 'little'))

    # Construct result packet
    result = PacketWrite()
    result.AddHeader([0xEC, 0x2E])

    # Attempt to get the receiver's character ID
    _args['mysql'].execute('SELECT `id` FROM `characters` WHERE `name` = %s', [receiver])
    receiver_character = _args['mysql'].fetchone()

    ''' If the character doesn't exist, or the client is trying to gift its current character, send back an error '''
    if receiver_character is None or receiver_character['id'] == _args['client']['character']['id'] \
            or receiver.lower() == _args['client']['character']['name'].lower():
                result.AppendBytes([0x00, 0x33])  # Bot name error
                return _args['socket'].send(result.packet)

    # Attempt to find the item in the database
    _args['mysql'].execute('''SELECT `id`, `item_id`, `gold_price`, `cash_price`, `part_type`, `duration` FROM `game_items`
        WHERE `item_id` = %s AND `buyable` = 1''', [item_id])
    item = _args['mysql'].fetchone()

    # Check if the item was found
    if item is None:
        result.AppendBytes([0x00, 0x42]) # Item not found
        return _args['socket'].send(result.packet)

    # Check if we have enough currency to purchase the item
    if item['gold_price'] > _args['client']['character']['currency_gigas'] \
            or item['cash_price'] > get_cash(_args):
        result.AppendBytes([0x00, 0x41]) # Not enough game points
        return _args['socket'].send(result.packet)

    # If the item's gold price is greater than 0, mutate the character's currency_gigas variable
    if item['gold_price'] > 0:
        _args['mysql'].execute('''UPDATE `characters` SET `currency_gigas` = (currency_gigas - %s) WHERE `id` = %s''', [
            item['gold_price'],
            _args['client']['character']['id']
        ])

        # Update local state with the new currency amount
        _args['client']['character']['currency_gigas'] -= item['gold_price']

    # Since an item could theoretically have two currency types attached to it, we'll also check if there's a cash amount.
    # I would otherwise use elif for this.
    if item['cash_price'] > 0:
        _args['mysql'].execute('''UPDATE `users` SET `cash` = (`cash` - %s) WHERE `id` = %s''', [
            item['cash_price'],
            _args['client']['account_id']
        ])

    # Create the item and send a gift to the receiver
    character_item_id = add_item(_args=_args, item=item, slot=None, inventory_insert=False)
    _args['mysql'].execute('''INSERT INTO `gifts` (`sender`, `receiver`, `date`, `message`, `type`, `item_1`)
            VALUES (%s, %s, UTC_TIMESTAMP(), %s, 0, %s)''', [
        _args['client']['character']['id'],
        receiver_character['id'],
        message,
        character_item_id
    ])

    # Sync cash and inventory
    sync_cash(_args)
    sync_inventory(_args)

'''
Method:         gift_count()
Description:    This method returns the amount of gifts our client has and returns it to the stack
'''
def gift_count(_args):

    # Get number of gifts
    _args['mysql'].execute('''SELECT `id` FROM `gifts` WHERE `receiver` = %s''', [
        _args['client']['character']['id']
    ])

    return _args['mysql'].rowcount