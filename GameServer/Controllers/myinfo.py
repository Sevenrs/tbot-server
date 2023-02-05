#!/usr/bin/env python3
__author__ = "Icseon"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Guild, Character, Friend

'''
This method will delete our client's character entirely
'''


def delete_character(**_args):
    # Construct result packet
    result = PacketWrite()
    result.add_header([0xE3, 0x2E])

    # If we are a staff member, we can not delete our bot.
    # We're also going to check if we are in a room. If we are, we can't proceed either.
    if _args['client']['character']['position'] > 0 or 'room' in _args['client']:
        result.append_bytes([0x00, 0xBF])
        return _args['socket'].sendall(result.packet)

    # If we are in a guild, we can not delete the bot (specific message for guilds)
    if Guild.fetch_guild(_args, _args['client']['character']['id']) is not None:
        result.append_bytes([0x00, 0xC4])
        return _args['socket'].sendall(result.packet)

    # Retrieve inventory and wearing items for this character
    inventory = Character.get_items(_args, _args['client']['character']['id'], 'inventory')
    wearing = Character.get_items(_args, _args['client']['character']['id'], 'wearing')

    # Check if we are wearing coin items (if type in field_pack coin_head coin_minibot or duration type = 1)
    for item in wearing['items']:
        if wearing['items'][item]['type'] in ['field_pack', 'coin_head', 'coin_minibot'] \
                or wearing['items'][item]['duration_type'] == 1:
            result.append_bytes([0x00, 0xC4])
            return _args['socket'].sendall(result.packet)

    # Append all inventory items to the item id array
    item_ids = []
    for item in inventory:
        if inventory[item]['character_item_id'] is not None:
            item_ids.append(inventory[item]['character_item_id'])

    # Append all wearing items to the item id array
    for item in wearing['items']:
        if wearing['items'][item]['character_item_id'] is not None:
            item_ids.append(wearing['items'][item]['character_item_id'])

    # Remove all IDs from character_items
    in_statement = ''
    for id in item_ids:
        in_statement += "{0}, ".format(str(id))

    # If the in statement has a length greater than 0, delete all of its IDs
    if len(in_statement) > 0:
        _args['mysql'].execute('''DELETE FROM `character_items` WHERE `id` IN ({0})'''.format(in_statement[:-2]))

    # Run deletion queries
    queries = [

        # Delete character inventory
        'DELETE FROM `inventory` WHERE `character_id` = %s',

        # Remove character's wearing items
        'DELETE FROM `character_wearing` WHERE `character_id` = %s',

        # Delete incoming gift items for this character
        'DELETE FROM `character_items` WHERE `id` IN (SELECT `item_1` FROM `gifts` WHERE `receiver` = %s AND `type` = 0)',

        # Delete incoming gifts for this character
        'DELETE FROM `gifts` WHERE `receiver` = %s',

        # Delete incoming messages for this character
        'DELETE FROM `inbox` WHERE `receiver_character_id` = %s',

        # Remove blocked users
        'DELETE FROM `blocked` WHERE `blocker` = %s',

        # Delete character
        'DELETE FROM `characters` WHERE `id` = %s'
    ]

    for query in queries:
        _args['mysql'].execute(query, [_args['client']['character']['id']])

    # Get our friends. We will have to notify them that we've deleted them as a friend.
    friends = Friend.get_friends(_args, character_id=_args['client']['character']['id']).fetchall()

    # Remove friendships. We are doing that separately because there are two possible WHERE conditions
    _args['mysql'].execute('''DELETE FROM `friends` WHERE (`character_id_1` = %s OR `character_id_2` = %s)''', [
        _args['client']['character']['id'],
        _args['client']['character']['id']
    ])

    # Refresh friend state on all of our friends' clients - if they exist
    for friend in friends:

        # Get friend's client and check if it was found. If so, we'll send the state
        friend_client = _args['connection_handler'].get_character_client(friend['name'])

        if friend_client:

            # Send their friend state to them
            Friend.retrieve_friends(_args, friend_client)

    # Finalize the result packet and send to the client
    result.append_bytes([0x01, 0x00])
    _args['socket'].sendall(result.packet)

    # Close connection
    _args['connection_handler'].update_player_status(_args['client'], 2)
