 #!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Lobby

"""
This file is responsible for handling all requests relating to friends
"""

"""
Method:         GetFriends
Description:    This method will obtain all friends from the database based on the character ID
"""
def GetFriends(_args, character_id):
    _args['mysql'].execute("""SELECT `character`.`level`, `character`.`name` FROM `characters` `character`
        WHERE `character`.`id` IN (SELECT `character_id_1` FROM `friends` WHERE `character_id_2` = %s)
        UNION
        SELECT `character`.`level`, `character`.`name` FROM `characters` `character`
        WHERE `character`.`id` IN (SELECT `character_id_2` FROM `friends` WHERE `character_id_1` = %s)""", [
            character_id,
            character_id
        ])
        
    # Return the results
    return _args['mysql']

"""
Method:         RetrieveFriends
Description:    This method obtains all friends (which I do not have) and sends them back to the target client
"""
def RetrieveFriends(_args, client):
    
    """ Initialize packet for the friend list """
    friends = PacketWrite()
    friends.AddHeader(bytearray([0x0C, 0x2F]))
    friends.AppendBytes(bytearray([0x01, 0x00]))
    
    """ Find all friends for the character belonging to the given client """
    result = GetFriends(_args, client['character']['id'])
    
    """ For every friend in the resultset, append it to the packet """
    for friend in result:
        friends.AppendString(friend['name'], 15)
        friends.AppendInteger(friend['level'], 4, 'little')
        
        # Check if friend is online
        if _args['connection_handler'].GetCharacterClient(friend['name']) is None:
            friends.AppendInteger(0, 4, 'little')
        else:
            friends.AppendInteger(1, 4, 'little')
    
    """ Additional padding (240 bytes) """
    for i in range(240):
        friends.AppendBytes([0x00])
    
    """ Send target client the packet we just built """
    client['socket'].send(friends.packet)
    
"""
Method:         FriendRequest
Description:    This method will handle all incoming friend requests and ensure the packets are sent to the right client(s)
"""
def FriendRequest(**_args):
    
    """ Read the receiver and the sender character name(s) from the packet """
    sender      = _args['packet'].ReadString(1) # Local player character name
    receiver    = _args['packet'].ReadString()  # Remote player character name
    
    """ Contruct the friend request packet for the receiver to receive """
    request = PacketWrite()
    request.AddHeader(bytearray([0x0F, 0x2F]))
    request.AppendBytes(bytearray([0x01, 0x00]))
    request.AppendString(_args['client']['character']['name'], 15) # Since our local client is the sender, we need to append our character name to the packet
    
    """ Attempt to find the target client and send the request packet to the socket """
    _args['connection_handler'].GetCharacterClient(receiver, request.packet)
    
"""
Method:         FriendRequestResult
Description:    This method will handle the answer for the friend request sent by the receiver of the initial request
"""
def FriendRequestResult(**_args):
    result      = _args['packet'].GetByte(2)    # If the request had been accepted
    receiver    = _args['packet'].ReadString(5) # Our local player's character name
    sender      = _args['packet'].ReadString()  # Our remote player's character name
    
    # Get client instance of the sender of the request
    sender_client = _args['connection_handler'].GetCharacterClient(sender)
    
    # If the sender is not online, we should not proceed
    if sender_client is None:
        return
    
    # If the friend request was declined, send a message indicating such
    if result == 0:
        declined_msg = PacketWrite()
        declined_msg.AddHeader(bytearray([0x28, 0x2F]))
        declined_msg.AppendBytes(bytearray([0x00, 0x53]))
        sender_client['socket'].send(declined_msg.packet)
        
    # If the request was accepted, insert the friend in the database and send the friend packet to both clients
    else:
        _args['mysql'].execute("""
            INSERT INTO `friends` (`character_id_1`, `character_id_2`, `date`)
                VALUES(%s, %s, UTC_TIMESTAMP())
        """, [_args['client']['character']['id'], sender_client['character']['id']])
        
        # Send friend state packet to both parties
        RetrieveFriends(_args, _args['client'])
        RetrieveFriends(_args, sender_client)
        
"""
Method:         DeleteFriend
Description:    This method will handle friend deletions
"""
def DeleteFriend(**_args):
    initiator = _args['packet'].ReadString(1) # Our local player character name. We will not be using this though.
    target    = _args['packet'].ReadString()  # Remote player character name.
    
    # Remove friend relationship from the database
    _args['mysql'].execute("""
        DELETE FROM `friends`
            WHERE
                (`character_id_1` = %s AND `character_id_2` = (SELECT `id` FROM `characters` WHERE `name` = %s)) OR
                (`character_id_2` = %s AND `character_id_1` = (SELECT `id` FROM `characters` WHERE `name` = %s))
    """, [
        _args['client']['character']['id'],
        target,
        _args['client']['character']['id'],
        target
    ])
    
    # Send friend packet to our local client
    RetrieveFriends(_args, _args['client'])
    
    # Notify the target of the deletion, if the target is present
    target_client = _args['connection_handler'].GetCharacterClient(target)
    if target_client is not None:
        RetrieveFriends(_args, target_client)

"""
Method:         PresenceNotification
Description:    This method will notify a character's friend of their presence
"""
def PresenceNotification(_args):
    friends = GetFriends(_args, _args['client']['character']['id'])
    for friend in friends:
        client = _args['connection_handler'].GetCharacterClient(friend['name'])
        if client is not None:
            Lobby.ChatMessage(client, "[Server] Your friend {0} has just logged in!".format(_args['client']['character']['name']), 3)
