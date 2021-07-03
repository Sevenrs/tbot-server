#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from enum import Enum

def get_items(_args, character_id, mode = 'wearing'):

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
                                                    LEFT JOIN `character_items` citem 
                                                        ON citem.`id` = cwear.`{0}`
                                                            AND (citem.`expiration_date` IS NULL 
                                                                OR TIMESTAMPDIFF(MINUTE, UTC_TIMESTAMP(),
                                                                    citem.`expiration_date`) > 0)
                                                            AND (citem.`remaining_games` IS NULL 
                                                                OR citem.`remaining_games` > 0)
                                                            AND (citem.`remaining_times` IS NULL 
                                                                OR citem.`remaining_times` > 0)
                                                    LEFT JOIN `game_items` gitem ON gitem.`id` = citem.`game_item`
                                                    WHERE cwear.`character_id` = %s""".format(item_type),
                                                        [character_id])
            wearing[item_type] = _args['mysql'].fetchone()

            # For the body part, we may need to obtain the correct transformation pack
            if item_type == 'trans_pack' and wearing['trans_pack']['item_id'] == 0 and wearing['body']['item_id'] != 0:
                wearing['trans_pack']['item_id'] = get_body_transformation(int(str(wearing['body']['item_id'])[:-1]))

            item = {
                "item_id":              wearing[item_type]['item_id'],
                'remaining_hours':      wearing[item_type]['remaining_hours'],
                'remaining_games':      wearing[item_type]['remaining_games'],
                'remaining_times':      wearing[item_type]['remaining_times'],
                'used':                 wearing[item_type]['used'],
                'part_type':            wearing[item_type]['part_type'],
                'character_item_id':    wearing[item_type]['character_item_id']
            }

            # Modify specification summary
            if wearing[item_type]['item_id'] != 0:
                for key, value in specifications_sum.items():
                    if wearing[item_type][key] is not None:
                        specifications_sum[key] = (value + wearing[item_type][key])

            items.append(item)

    # Get and return inventory items
    elif mode == 'inventory':
        for i in range(1, 21):
            _args['mysql'].execute("""SELECT    IFNULL(gitem.`item_id`, 0)                                      
                                                    AS `item_id`,
                                                TIMESTAMPDIFF(HOUR, UTC_TIMESTAMP(), citem.`expiration_date`)
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

                                                FROM `inventory` inventory
                                                LEFT JOIN `character_items` citem   
                                                    ON  citem.`id` = inventory.`item_{0}`
                                                LEFT JOIN `game_items`      gitem  
                                                    ON  gitem.`id` = citem.`game_item`
                                                WHERE `character_id` = %s""".format(i), [
                                                    _args['client']['character']['id']])

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

        # If the item has not been used, and the duration type is higher than 1, update the duration type to be unused
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
'''
def get_available_inventory_slot(inventory):
    for item in inventory:
        if inventory[item]['id'] == 0:
            return item

    return None

'''
This method inserts a new item into character_items and puts it in our inventory
'''
def add_item(_args, item, slot, item_type):

    # Standard values
    remaining_games, remaining_times, used = None, None, (0 if item_type == 'cash' else None)

    # If the part is a pack or a special part, add the amount of times they can be used
    if item['part_type'] in (0, 14):
        remaining_times, used = item['duration'], 1

    # If the item type is either gun or passive/active skill, add remaining games
    if (item['part_type'] == 5 and item_type != 'gold') or item['part_type'] in (12, 13):
        remaining_games, used = item['duration'], 1

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
    _args['mysql'].execute("""UPDATE `inventory` SET `item_{0}` = %s WHERE `character_id` = %s""".format(str(slot + 1)), [
        character_item_id,
        _args['client']['character']['id']
    ])

'''
This method removes an item from character_items and removes it from our inventory
'''
def remove_item(_args, character_item_id, slot):

    # Remove item from the inventory of our character, but only if the item id actually matches the slot index
    _args['mysql'].execute("""UPDATE `inventory` SET `item_{0}` = 0 WHERE `character_id` = %s AND `item_{0}` = %s""".format(str(slot + 1)), [
        _args['client']['character']['id'],
        character_item_id
    ])

    # Remove item from character_items
    _args['mysql'].execute("""DELETE FROM `character_items` WHERE `id` = %s""", [character_item_id])


'''
This method constructs the bot data which can then be appended to a packet to send the character information sheet
'''
def construct_bot_data(_args, character):

    bot = PacketWrite()

    # Obtain wearing items
    wearing_items = get_items(_args, character['id'], 'wearing')

    # Append general character information to packet
    bot.AppendString(character['name'], 15)
    bot.AppendInteger(character['type'], 2, 'little')
    bot.AppendInteger(character['experience'], 4, 'little')
    bot.AppendInteger(character['level'], 2, 'little')
    bot.AppendInteger(character['health']
                                        + wearing_items['specifications']['effect_health'], 2, 'little')
    bot.AppendInteger(character['att_min']
                                        + wearing_items['specifications']['effect_att_min'], 2, 'little')
    bot.AppendInteger(character['att_max']
                                        + wearing_items['specifications']['effect_att_max'], 2, 'little')
    bot.AppendInteger(character['att_trans_min']
                                        + wearing_items['specifications']['effect_att_trans_min'], 2, 'little')
    bot.AppendInteger(character['att_trans_max']
                                        + wearing_items['specifications']['effect_att_trans_max'], 2, 'little')

    bot.AppendBytes([0x00, 0x00])

    # Append character effects to the packet
    bot.AppendInteger(character['trans_guage']
                                        + wearing_items['specifications']['effect_trans_guage'], 2, 'little')
    bot.AppendInteger(character['att_critical']
                                        + wearing_items['specifications']['effect_critical'], 2, 'little')
    bot.AppendInteger(character['att_evade']
                                        + wearing_items['specifications']['effect_critical'], 2, 'little')
    bot.AppendInteger(character['trans_special']
                                        + wearing_items['specifications']['effect_special_trans'], 2, 'little')
    bot.AppendInteger(character['speed']
                                        + wearing_items['specifications']['effect_speed'], 2, 'little')
    bot.AppendInteger(character['trans_def']
                                        + wearing_items['specifications']['effect_trans_bot_defense'], 2, 'little')
    bot.AppendInteger(character['trans_att']
                                        + wearing_items['specifications']['effect_trans_bot_attack'], 2, 'little')
    bot.AppendInteger(character['trans_speed']
                                        + wearing_items['specifications']['effect_trans_speed'], 2, 'little')
    bot.AppendInteger(character['att_ranged']
                                        + wearing_items['specifications']['effect_ranged_attack'], 2, 'little')
    bot.AppendInteger(character['luck']
                                        + wearing_items['specifications']['effect_luck'], 2, 'little')

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

    for i in range(200):
        bot.AppendBytes([0x00])

    for i in range(17, 19):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        bot.AppendInteger(item['id'], 4, 'little')
        bot.AppendInteger(item['duration'], 4, 'little')
        bot.AppendInteger(item['duration_type'], 1, 'little')

    for _ in range(30):
        bot.AppendBytes([0x00])

    bot.AppendInteger(2, 1, 'little')

    for _ in range(50):
        bot.AppendInteger(0, 4, 'little')
        bot.AppendInteger(0, 4, 'little')
        bot.AppendInteger(0, 1, 'little')

    for _ in range(27):
        bot.AppendBytes([0x00, 0x00, 0x00, 0x00])

    bot.AppendInteger(character['rank_exp'], 4, 'little')
    bot.AppendInteger(character['rank'], 4, 'little')

    return bot.data


def get_body_transformation(body_item_id):

    return 0

    # body 0 should have trans 0e
    if body_item_id == 0:
        return 0

    transformation_map = {

        # Patch Items
        112010: 870,
        112020: 880,
        112030: 890,
        112040: 900,
        112050: 910,
        112060: 920,
        112070: 930,
        112080: 940,
        112090: 950,
        112100: 960,
        112110: 970,
        112140: 980,

        # Surge Items
        122010: 990,
        122020: 220,
        122030: 230,
        122040: 240,
        122050: 250,
        122060: 260,
        122070: 270,
        122080: 280,
        122090: 290,
        122100: 300,
        122110: 310,
        122140: 320,

        # Ram Items
        132010: 330,
        132020: 340,
        132030: 350,
        132040: 360,
        132050: 370,
        132060: 380,
        132070: 390,
        132080: 400,
        132090: 410,
        132100: 420,
        132110: 430,
        132130: 440,
        132140: 450
    }

    return int("144{}0".format(str(transformation_map[body_item_id])))
