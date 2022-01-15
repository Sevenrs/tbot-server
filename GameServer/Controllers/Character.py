#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from enum import Enum
from GameServer.Controllers.data.bot import *

'''
This method is responsible for obtaining items connected to an account or character.
The supported modes are:

    1. Wearing      - this will retrieve all items the character is currently wearing.
    2. Inventory    - this will retrieve all items in a characters' inventory.
    3. Stash        - this will retrieve all items in a specific stash number (1 to 5).
    
This will return an easy to use object where items can be easily read and managed.
'''
def get_items(_args, character_id, mode = 'wearing', external_id=None):

    # List with the obtained items from the database
    items = []

    # List with the formatted representation of the items
    result = {}

    # List with the character specification adjustments caused by the wearing items
    specifications_sum = {
        'effect_health': 0,
        'effect_att_min': 0,
        'effect_att_max': 0,
        'effect_att_trans_min': 0,
        'effect_att_trans_max': 0,
        'effect_trans_guage': 0,
        'effect_critical': 0,
        'effect_evade': 0,
        'effect_special_trans': 0,
        'effect_speed': 0,
        'effect_trans_bot_defense': 0,
        'effect_trans_bot_attack': 0,
        'effect_trans_speed': 0,
        'effect_ranged_attack': 0,
        'effect_luck': 0
    }

    # Array with item types
    types = ['head', 'body', 'arms', 'mini-bot', 'gun', 'ef', 'wing', 'shield', 'shoulder', 'flag1', 'flag2',
             'passive_skill', 'attack_skill', 'field_pack', 'trans_pack', 'merc1', 'merc2', 'coin_head', 'coin_minibot']

    # Get and return wearing items
    if mode == 'wearing':
        wearing = {}

        # Obtain wearing item for each possible type
        for item_type in types:
            _args['mysql'].execute("""SELECT IFNULL(gitem.`item_id`, 0) AS `item_id`,
                                                    TIMESTAMPDIFF(HOUR, UTC_TIMESTAMP(), citem.`expiration_date`) 
                                                        AS `remaining_hours`,
                                                    citem.`remaining_games`,
                                                    citem.`remaining_times`,
                                                    citem.`used`,
                                                    gitem.`effect_health`,
                                                    gitem.`effect_att_min`,
                                                    gitem.`effect_att_max`,
                                                    gitem.`effect_att_trans_min`,
                                                    gitem.`effect_att_trans_max`,
                                                    gitem.`effect_trans_guage`,
                                                    gitem.`effect_critical`,
                                                    gitem.`effect_evade`,
                                                    gitem.`effect_special_trans`,
                                                    gitem.`effect_speed`,
                                                    gitem.`effect_trans_bot_defense`,
                                                    gitem.`effect_trans_bot_attack`,
                                                    gitem.`effect_trans_speed`,
                                                    gitem.`effect_ranged_attack`,
                                                    gitem.`effect_luck`,
                                                    gitem.`part_type`,
                                                    citem.`id` AS `character_item_id`
                                                    FROM `character_wearing` cwear
                                                    LEFT JOIN `character_items` citem   ON citem.`id` = cwear.`{0}`
                                                    LEFT JOIN `game_items` gitem        ON gitem.`id` = citem.`game_item`
                                                    WHERE cwear.`character_id` = %s""".format(item_type),
                                                        [character_id])
            wearing[item_type] = _args['mysql'].fetchone()

            item = {
                "item_id":              wearing[item_type]['item_id'],
                'remaining_hours':      wearing[item_type]['remaining_hours'],
                'remaining_games':      wearing[item_type]['remaining_games'],
                'remaining_times':      wearing[item_type]['remaining_times'],
                'used':                 wearing[item_type]['used'],
                'part_type':            17 if item_type == 'merc2' else wearing[item_type]['part_type'],
                'character_item_id':    wearing[item_type]['character_item_id']
            }

            # Modify specification summary
            if wearing[item_type]['item_id'] != 0:
                for key, value in specifications_sum.items():
                    if wearing[item_type][key] is not None:
                        specifications_sum[key] = (value + wearing[item_type][key])

            items.append(item)

    # Get and return inventory or stash items
    elif mode in ['inventory', 'stash', 'gifts']:

        # Default item range, where statement and SQL parameter to retrieve all items in the character's inventory.
        item_range, where_statement, sql_parameter = 21, '`character_id` = %s', character_id

        # If we are trying to obtain a stash, overwrite the item range and where statement
        # We want to obtain the stash ordered by ID with an offset, because an account can have multiple stashes.
        if mode == 'stash':
            item_range      = 11
            where_statement = '`account_id` = %s ORDER BY `model`.`id` ASC LIMIT 1 OFFSET {0}'.format(external_id - 1)
            sql_parameter   = _args['client']['account_id']

        elif mode == 'gifts':
            item_range      = 2
            where_statement = 'model.`id` = %s'
            sql_parameter   = external_id

        for i in range(1, item_range):
            _args['mysql'].execute("""SELECT    IFNULL(gitem.`item_id`, 0)                                      
                                                    AS `item_id`,
                                                TIMESTAMPDIFF(HOUR, UTC_TIMESTAMP(), DATE_ADD(UTC_TIMESTAMP(), INTERVAL `remaining_seconds` SECOND))
                                                    AS `remaining_hours`,
                                                citem.`remaining_games`                                        
                                                    AS `remaining_games`,
                                                citem.`remaining_times`                                         
                                                    AS `remaining_times`,
                                                citem.`used`
                                                    AS `used`,    
                                                gitem.`part_type`
                                                    AS `part_type`,
                                                citem.`id`
                                                    AS `character_item_id`

                                                FROM `{0}` model
                                                LEFT JOIN `character_items` citem   
                                                    ON  citem.`id` = model.`item_{1}`
                                                LEFT JOIN `game_items`      gitem  
                                                    ON  gitem.`id` = citem.`game_item`
                                                WHERE {2}""".format(mode, i, where_statement), [
                                                    sql_parameter])

            items.append(_args['mysql'].fetchone())

    # Determine duration and duration type and format the result properly
    for idx, item in enumerate(items):

        # Standard values
        duration = 0
        duration_type = 0

        if item['remaining_hours'] is not None:
            duration = item['remaining_hours']
            duration_type = 1

        elif item['remaining_times'] is not None:
            duration = item['remaining_times']
            duration_type = 2

        elif item['remaining_games'] is not None:
            duration = item['remaining_games']
            duration_type = 3

        # If the item has not been used, update the duration type to be unused
        if item['used'] == 0:
            duration_type = 4

        result[idx] = {
            "id":                   item['item_id'],
            "duration":             duration,
            "duration_type":        duration_type,
            "type":                 types[int(item['part_type']) - 1] if item['part_type'] is not None else None,
            'character_item_id':    item['character_item_id']
        }

    if mode == 'wearing':
        return {
            "items": result,
            "specifications": specifications_sum
        }

    return result

'''
This method gets the first available inventory slot number
This method also works for stashes/storages
'''
def get_available_inventory_slot(inventory):
    for item in inventory:
        if inventory[item]['id'] == 0:
            return item

    return None

'''
This method inserts a new item into character_items and puts it in our inventory
'''
def add_item(_args, item, slot, inventory_insert=True):

    # Standard values. The used parameter is set only if the duration of the item is greater than 0
    remaining_games, remaining_times, used = None, None, (0 if item['duration'] > 0 else None)

    '''
    If the part is a pack or a special part, add the amount of times they can be used
    Additionally, the item should have its used state removed
    '''
    if item['part_type'] in (0, 14) and item['duration'] > 0:
        remaining_times, used = item['duration'], None

    '''
    If the item type is a gun, passive or active skill, add the remaining games
    Remove the used state from the item because there is no need to track that
    '''
    if item['part_type'] in (5, 12, 13) and item['duration'] > 0:
        remaining_games, used = item['duration'], None

    # Insert into character items
    _args['mysql'].execute("""INSERT INTO `character_items` (`game_item`, `remaining_games`, `remaining_times`, `used`)
     VALUES (%s, %s, %s, %s)""", [
        item['id'],
        remaining_games,
        remaining_times,
        used
    ])

    # Retrieve character item id from the last row identifier
    character_item_id = _args['mysql'].lastrowid

    # Insert item into the inventory of our character
    if inventory_insert:
        _args['mysql'].execute("""UPDATE `inventory` SET `item_{0}` = %s WHERE `character_id` = %s""".format(str(slot + 1)), [
            character_item_id,
            _args['client']['character']['id']
        ])

    return character_item_id

'''
This method removes an item from character_items and removes it from our inventory
'''
def remove_item(_args, character_item_id, slot=None):

    # Remove item from the inventory of our character, but only if the item id actually matches the slot index
    if slot is not None:
        _args['mysql'].execute("""UPDATE `inventory` SET `item_{0}` = 0 WHERE `character_id` = %s AND `item_{0}` = %s""".format(str(slot + 1)), [
            _args['client']['character']['id'],
            character_item_id
        ])

    # Remove item from character_items
    _args['mysql'].execute("""DELETE FROM `character_items` WHERE `id` = %s""", [character_item_id])


'''
This method will remove expired items which we are wearing
'''
def remove_expired_items(_args, character_id):

    # Retrieve currently wearing items
    wearing_items = get_items(_args, character_id, 'wearing')['items']

    # Construct wearing table
    wearing_table   = {}

    for item in wearing_items:

        # Skip iteration if the character_item_id is equal to None
        if wearing_items[item]['character_item_id'] is None:
            continue

        # Append item to the wearing table and item id array
        wearing_table[wearing_items[item]['character_item_id']] = wearing_items[item]['type']

    # There is nothing to do if we are not wearing anything
    if len(wearing_table) == 0:
        return

    # Construct IN statement for the query
    in_statement = ''
    for id in wearing_table.keys():
        in_statement+="{0}, ".format(str(id))

    # Retrieve expired items dynamically
    _args['mysql'].execute("""SELECT `id` FROM `character_items` WHERE (
            (UTC_TIMESTAMP() >= `expiration_date` AND `expiration_date` IS NOT NULL)    OR
                (`remaining_games` < 1 AND `remaining_games` IS NOT NULL)               OR
                    (`remaining_times` < 1 AND `remaining_times` IS NOT NULL)
    ) AND `id` IN ({})""".format(in_statement[:-2]))
    expired_items = _args['mysql'].fetchall()

    # Remove the expired items from our character and from the game entirely
    for item in expired_items:

        # Remove item from our character and from the game
        _args['mysql'].execute("""UPDATE `character_wearing` SET `{0}` = 0 WHERE `character_id` = %s"""
                               .format(wearing_table[item['id']]), [character_id])
        remove_item(_args, item['id'])

'''
This method will get the amount of storages/stashes an account has
'''
def get_storage_count(_args, account_id):
    _args['mysql'].execute('SELECT `id` FROM `stash` WHERE `account_id` = %s', [account_id])
    return _args['mysql'].rowcount

'''
This method will return the requested statistic value and apply the statistic override where applicable
'''
def get_statistic_value(
        character,
        wearing_items,
        statistic,
        stat_override={}
):

    # Calculate the value by adding the default value as well as the value from the specification object
    value = character[ statistic[STAT_KEY] ] + wearing_items['specifications'][ statistic[STAT_EFFECT_KEY] ]

    # If the stat is defined in the stat override object, overwrite the stat with the value there
    if statistic[STAT_KEY] in stat_override:
        value = stat_override[ statistic[STAT_KEY] ]

    # Return the value to the stack
    return value

'''
This method constructs the bot data which can then be appended to a packet to send the character information sheet
'''
def construct_bot_data(_args, character, stat_override={}):

    # Prepare bot packet
    bot = PacketWrite()

    # Before we obtain wearing items, remove any expired items that we may have
    remove_expired_items(_args, character['id'])

    # Obtain wearing items
    wearing_items = get_items(_args, character['id'], 'wearing')

    # Append general character information to packet
    bot.AppendString    (character['name'], 15)
    bot.AppendInteger   (character['type'], 2, 'little')
    bot.AppendInteger   (character['experience'], 4, 'little')
    bot.AppendInteger   (character['level'], 2, 'little')

    # Append health, att_min, att_max, att_trans_min and att_trans_max to the packet
    for statistic in [
        STAT_HEALTH,
        STAT_ATT_MIN,
        STAT_ATT_MAX,
        STAT_ATT_TRANS_MIN,
        STAT_ATT_TRANS_MAX
    ]: bot.AppendInteger(get_statistic_value(
        character=character, wearing_items=wearing_items, statistic=statistic, stat_override=stat_override
    ), 2, 'little')

    # Defense statistic, 51.2% of incoming damage
    bot.AppendInteger(512, 2, 'little')

    # Append character effects to the packet
    for statistic in [
        STAT_ATT_TRANS_GAUGE,
        STAT_ATT_CRITICAL,
        STAT_ATT_EVADE,
        STAT_ATT_SPECIAL_TRANS,
        STAT_SPEED,
        STAT_TRANS_DEF,
        STAT_TRANS_ATT,
        STAT_TRANS_SPEED,
        STAT_ATT_RANGED,
        STAT_LUCK
    ]: bot.AppendInteger(get_statistic_value(
        character=character, wearing_items=wearing_items, statistic=statistic, stat_override=stat_override
    ), 2, 'little')

    # Append the amount of botstract to the packet
    bot.AppendInteger(character['currency_botstract'], 4, 'little')

    for _ in range(4):
        bot.AppendBytes([0x00, 0x00, 0x00, 0x00])

    for i in range(0, 3):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        bot.AppendInteger(item['id'], 4, 'little')
        bot.AppendInteger(item['duration'], 4, 'little')
        bot.AppendInteger(item['duration_type'], 1, 'little')

    bot.AppendBytes([0x01, 0x00, 0x00])

    inventory = get_items(_args, character['id'], 'inventory')
    for item in inventory:
        bot.AppendInteger(inventory[item]['id'], 4, 'little')
        bot.AppendInteger(inventory[item]['duration'], 4, 'little')
        bot.AppendInteger(inventory[item]['duration_type'], 1, 'little')

    for _ in range(904):
        bot.AppendBytes([0x00])

    # Gigas
    bot.AppendInteger(character['currency_gigas'], 4, 'little')

    for _ in range(242):
        bot.AppendBytes([0x00])

    for i in range(3, 17):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        bot.AppendInteger(item['id'], 4, 'little')
        bot.AppendInteger(item['duration'], 4, 'little')
        bot.AppendInteger(item['duration_type'], 1, 'little')

    for _ in range(200):
        bot.AppendBytes([0x00])

    for i in range(17, 19):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        bot.AppendInteger(item['id'], 4, 'little')
        bot.AppendInteger(item['duration'], 4, 'little')
        bot.AppendInteger(item['duration_type'], 1, 'little')

    for _ in range(30):
        bot.AppendBytes([0x00])

    # Retrieve the amount of stashes we own and use that count to retrieve stash items
    stash_count = get_storage_count(_args, _args['client']['account_id'])
    bot.AppendInteger(stash_count, 1, 'little')

    # For every stash, send its items over the network
    for i in range(0, stash_count):

        # Get stash items with the stash number supplied.
        stash = get_items(_args, character['id'], 'stash', (i + 1))
        for item in stash:
            bot.AppendInteger(stash[item]['id'], 4, 'little')
            bot.AppendInteger(stash[item]['duration'], 4, 'little')
            bot.AppendInteger(stash[item]['duration_type'], 1, 'little')

    # For the stashes we do not have, we'll want to send null items.
    for _ in range((5 - stash_count) * 10):
        bot.AppendInteger(0, 4, 'little')
        bot.AppendInteger(0, 4, 'little')
        bot.AppendInteger(0, 1, 'little')

    for _ in range(27):
        bot.AppendBytes([0x00, 0x00, 0x00, 0x00])

    bot.AppendInteger(character['rank_exp'], 4, 'little')
    bot.AppendInteger(character['rank'], 4, 'little')

    return bot.data