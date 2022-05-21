#!/usr/bin/env python3
__author__      = 'Icseon'
__copyright__   = 'Copyright (C) 2021 Icseon'
__version__     = '1.0'

from Packet.Write import Write as PacketWrite

"""
This handler is responsible for handling user blocks
"""

'''
Method:         block_user
Description:    This method will handle user blocks
Debug symbol:   COption::RequestBlockAdd()
'''
def block_user(**_args):

    # Read the username our client is attempting to block
    username = _args['packet'].ReadString(2).strip()

    # Create result packet
    result = PacketWrite()
    result.AddHeader([0x50, 0x2F]) # COption::ReplyBlockAdd

    # Check if we have exceeded the limit of blocked users (20)
    _args['mysql'].execute('''SELECT `id` FROM `blocked` WHERE `blocker` = %s''', [ _args['client']['character']['id']])
    blocks = _args['mysql'].fetchall()
    if len(blocks) >= 20:
        result.AppendBytes([0x00, 0xC0]) # You cannot add anymore BOTS to your Block list. (Limit 20)
        return _args['socket'].sendall(result.packet)

    # Attempt to find the target's character ID. We should exclude staff members from the scope of blockable users.
    _args['mysql'].execute('''SELECT `id`, `name` FROM `characters` WHERE `name` = %s AND `position` = 0''', [ username ])
    target_character = _args['mysql'].fetchone()

    # Check if the target character exists and is not our own by checking the ID
    if target_character is None or target_character['id'] == _args['client']['character']['id']:
        result.AppendBytes([0x00, 0x33])
        return _args['socket'].sendall(result.packet)

    # Create the block between the two users by adding it to the database, but only if the block does not exist
    # Additionally, do not allow to block anymore users if the amount of users this user has blocked is equal or greater than 20
    _args['mysql'].execute('''INSERT INTO `blocked` (`blocker`, `blocked`)
                                SELECT %s, %s FROM DUAL
                                    WHERE
                                        NOT EXISTS (SELECT * FROM `blocked` WHERE (`blocker` = %s AND `blocked` = %s) LIMIT 1)
                                        AND (SELECT COUNT(*) FROM `blocked` WHERE (`blocker` = %s)) < 20''', [
        _args['client']['character']['id'],
        target_character['id'],
        _args['client']['character']['id'],
        target_character['id'],
        _args['client']['character']['id']
    ])

    # If the affected row count is 0, the user was already blocked
    if _args['mysql'].rowcount == 0:
        result.AppendBytes([0x00, 0xBE]) # This bot is already on the list!
        return _args['socket'].sendall(result.packet)

    # If the affected rows were higher than 0, the user has been blocked successfully. Send result packet.
    result.AppendBytes([0x01, 0x00])
    result.AppendString(target_character['name'], 15)
    _args['socket'].sendall(result.packet)

'''
Method:         unblock_user
Description:    This method will handle user unblocks
Debug symbol:   COption::RequestBlockDelete()
'''
def unblock_user(**_args):

    # Read the username our client is attempting to unblock
    username = _args['packet'].ReadString(2).strip()

    # Remove the block between the two users
    _args['mysql'].execute('''DELETE FROM `blocked` WHERE (`blocker` = %s AND `blocked` = (
        SELECT `id` FROM `characters` WHERE `name` = %s))''', [
        _args['client']['character']['id'],
        username
    ])

    # Construct result packet
    result = PacketWrite()
    result.AddHeader([0x51, 0x2F]) # COption::ReplyBlockDelete

    # If the affected row count is 0, the user was not unblocked. Send bot name error.
    if _args['mysql'].rowcount == 0:
        result.AppendBytes([0x00, 0x33])
        return _args['socket'].sendall(result.packet)

    # If the affected rows were higher than 0, the user has been unblocked successfully. Send result packet.
    result.AppendBytes([0x01, 0x00])
    result.AppendString(username, 15)
    _args['socket'].sendall(result.packet)


'''
Method:         get_blocks()
Description:    This method will retrieve all users that we have blocked and send it to the client
'''
def get_blocks(_args):

    # Retrieve all blocked users
    _args['mysql'].execute('''SELECT c.`name` FROM `blocked` b
        JOIN `characters` c ON c.`id` = b.`blocked` WHERE b.`blocker` = %s''', [
        _args['client']['character']['id']
    ])

    # Fetch the blocked users
    blocked_users = _args['mysql'].fetchall()

    # Construct result packet and send to the client
    result = PacketWrite()
    result.AddHeader([0x4F, 0x2F])
    result.AppendBytes([0x01, 0x00, 0x00, 0x00])
    result.AppendInteger(len(blocked_users), 2, 'little')

    for user in blocked_users:
        result.AppendString(user['name'], 15)

    # Send result to client
    _args['socket'].sendall(result.packet)