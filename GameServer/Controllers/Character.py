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

    # Get and return wearing items
    if mode == 'wearing':
        wearing = {}

        # Array with wearable item types
        types = ['head', 'body', 'arms', 'mini-bot', 'gun', 'ef', 'wing', 'shield', 'shoulder', 'flag1', 'flag2',
                 'passive_skill', 'attack_skill', 'field_pack', 'trans_pack', 'merc1', 'merc2', 'coin_head', 'coin_minibot']

        # Obtain wearing item for each possible type
        for item_type in types:
            _args['mysql'].execute("""SELECT IFNULL(gitem.`item_id`, 0) AS `item_id`,
                                                    TIMESTAMPDIFF(HOUR, UTC_TIMESTAMP(), citem.`expiration_date`) 
                                                        AS `remaining_hours`,
                                                    citem.`remaining_games`,
                                                    citem.`remaining_times`,
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
                                                    gitem.`effect_luck`
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
                "item_id": wearing[item_type]['item_id'],
                'remaining_hours': wearing[item_type]['remaining_hours'],
                'remaining_games': wearing[item_type]['remaining_games'],
                'remaining_times': wearing[item_type]['remaining_times']
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
                                                    AS `remaining_times`

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

        result[idx] = {
            "id": item['item_id'],
            "duration": duration,
            "duration_type": duration_type
        }

    if mode == 'wearing':
        return {
            "items": result,
            "specifications": specifications_sum
        }

    return result


def get_body_transformation(body_item_id):

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
