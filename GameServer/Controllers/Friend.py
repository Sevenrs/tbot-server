 #!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 - 2021 Icseon"
__version__ = "1.1"

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
    _args['mysql'].execute("""SELECT `character`.`level`, `character`.`name`, `character`.`id` FROM `characters` `character`
        WHERE `character`.`id` IN (SELECT `character_id_1` FROM `friends` WHERE `character_id_2` = %s)
        UNION
        SELECT `character`.`level`, `character`.`name`, `character`.`id` FROM `characters` `character`
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
    for _ in range(240):
        friends.AppendBytes([0x00])
    
    """ Attempt to send the packet we built to the target client """
    try:
        client['socket'].send(friends.packet)
    except Exception as e:
        print('Failed to send friend list packet to client because: ', str(e))
    
"""
Method:         friend_request
Description:    This method will handle all incoming friend requests and ensure the packets are sent to the right client(s)
"""
def friend_request(**_args):

    # Read remote character name from packet
    receiver = _args['packet'].ReadString(16)

    # Construct error packet in the event we need it
    error = PacketWrite()
    error.AddHeader([0x28, 0x2F])

    # Check if we have reached the maximum amount of friends (10)
    friends = GetFriends(_args, _args['client']['character']['id']).fetchall()
    if len(friends) >= 10:
        error.AppendBytes([0x00, 0x55]) # Max friend list capacity reached (10)
        return _args['socket'].send(error.packet)

    # Retrieve remote character's client handle
    remote_client = _args['connection_handler'].GetCharacterClient(receiver)

    # Check if the client exists, is not in a room and is not our own client
    if remote_client is None or 'room' in remote_client or remote_client is _args['client']:
        error.AppendBytes([0x00, 0x53]) # Request denied or player can not accept at the moment
        return _args['socket'].send(error.packet)

    # Check if the remote player still has any available slots for friends
    # If they do not, send an error to our own client
    remote_friends = GetFriends(_args, remote_client['character']['id']).fetchall()
    if len(remote_friends) >= 10:
        error.AppendBytes([0x00, 0x53]) # Request denied or player can not accept at the moment
        return _args['socket'].send(error.packet)

    # Check if the remote player is already in our friends list. Refuse the packet if this is the case.
    for friend in friends:
        if friend['id'] == remote_client['character']['id']:
            error.AppendBytes([0x00, 0x3D]) # Request refused
            return _args['socket'].send(error.packet)

    # Create friend request session that expires 20 seconds after being created
    session = _args['session_handler'].create(
        type            =   'friend_request',
        clients         =   [ remote_client ],
        data            =   {'requester': _args['client']},
        expires_after   = 20 # Expire after 20 seconds
    )
    
    # Construct the friend request packet for the receiver to receive
    # After construction, broadcast it to the remote client
    request = PacketWrite()
    request.AddHeader(bytearray([0x0F, 0x2F]))
    request.AppendBytes(bytearray([0x01, 0x00]))
    request.AppendString(_args['client']['character']['name'], 15) # Sender
    _args['session_handler'].broadcast(session, request.packet)
    
"""
Method:         FriendRequestResult
Description:    This method will handle the answer for the friend request sent by the receiver of the initial request
"""
def friend_request_result(**_args):

    # Read relevant data from packet
    response    = _args['packet'].GetByte(2)        # Acceptance
    sender      = _args['packet'].ReadString(20)    # Sender of request

    # Attempt to find the friend request session
    request_session = None
    for session in _args['server'].sessions:
        if session['type'] == 'friend_request' \
            and _args['client'] in session['clients'] \
                and session['data']['requester']['character']['name'] == sender:
            request_session = session
            break

    # Construct result packet that we will be sending to our own client
    result = PacketWrite()
    result.AddHeader([0x28, 0x2F])

    # If the request session was not found, drop the packet and send an error
    if request_session is None:
        result.AppendBytes([0x00, 0x3D]) # Request refused
        return _args['socket'].send(result.packet)

    # Destroy session and proceed with the request
    _args['session_handler'].destroy(request_session)

    # Obtain our friends so we can check if we still have capacity at this moment
    # We should also perform this check for the remote client
    friends         = GetFriends(_args, _args['client']['character']['id']).fetchall()
    remote_friends  = GetFriends(_args, request_session['data']['requester']['character']['id']).fetchall()
    
    # If the friend request was denied, or if we have hit the maximum capacity of our friend list
    # send the declination message to the remote client. If we have hit the maximum capacity, send that message
    # to our own client as well.
    if response == 0 or len(friends) >= 10 or len(remote_friends) >= 10:

        # Construct declination message and attempt to send to the requester
        declined = PacketWrite()
        declined.AddHeader([0x28, 0x2F])
        declined.AppendBytes([0x00, 0x53])
        try:
            request_session['data']['requester']['socket'].send(declined.packet)
        except Exception as e:
            print('Failed to send friend request declined packet to remote client because: ', str(e))

        # In case our friend list has reached its maximum capacity, send an error to our client as well
        if len(friends) >= 10:
            result.AppendBytes([0x00, 0x55])
            _args['socket'].send(result.packet)

        # Do not proceed with the request
        return

    # Otherwise, we can proceed to create the relationship between the two players
    _args['mysql'].execute("""
                INSERT INTO `friends` (`character_id_1`, `character_id_2`, `date`)
                    VALUES(%s, %s, UTC_TIMESTAMP())
            """, [_args['client']['character']['id'], request_session['data']['requester']['character']['id']])

    # Send friend state packet to both clients
    RetrieveFriends(_args, _args['client'])
    RetrieveFriends(_args, request_session['data']['requester'])
        
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

    # Get our friends
    friends = GetFriends(_args, _args['client']['character']['id'])

    for friend in friends:

        # Get remote client of friend and attempt to send a message
        client = _args['connection_handler'].GetCharacterClient(friend['name'])
        if client is not None:
            try:
                Lobby.ChatMessage(client, "[*Server*] Your friend {0} has just logged in!".format(_args['client']['character']['name']), 1)
            except Exception as e:
                print('Could not send PresenceNotification to remote client because: ', str(e))
