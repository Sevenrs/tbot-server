#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Lobby

"""
This file is responsible for handling all requests relating to guilds
"""

"""
Method:         AddMember
Description:    This method will add a member to a guild
Parameters:     1. The guild ID
                2. The character ID
"""
def AddMember(_args, character_id, guild_id, applying = 0):
    _args['mysql'].execute("""INSERT INTO `guild_members` (`character_id`, `guild_id`, `applying`)
        VALUES (%s, %s, %s)""", [
        character_id,
        guild_id,
        applying
    ])

def FetchGuild(_args, character_id):
    _args['mysql'].execute("""SELECT g.`id`, g.`name`, g.`created`, g.`notice`, g.`max_members`, c.`name` AS `guild_master`,
        (SELECT COUNT(*) FROM `guild_members` WHERE `guild_id` = g.`id`) AS `member_count`,
        (SELECT SUM(`points`) FROM `guild_members` WHERE `guild_id` = g.`id` AND `applying` = 0) AS `guild_points`,
        (g.`leader_character_id` = m.`character_id`) AS `is_leader`, m.`applying`
        
        FROM `guild_members` m
        JOIN `guilds` g ON g.`id` = m.`guild_id`
        JOIN `characters` c ON c.id = g.leader_character_id
        WHERE m.`character_id` = %s""", [character_id])

    return _args['mysql'].fetchone()

"""
Method:         GetGuild
Description:    This method will fetch the guild membership of a specific user.
                It is possible to send the state to a specific client using the first parameter.
Parameters:     1. The _args parameter that contains all variables given by the server acting as a global state.
                2. The target client which is to receive this packet
                3. If we should also get the guild notice or not, default is False
"""
def GetGuild(_args, client, get_notice=False):

    # Get guild membership
    guild = FetchGuild(_args, client['character']['id'])
    
    # Create the guild state packet
    GuildState = PacketWrite()
    GuildState.AddHeader(bytearray([0x46, 0x2F]))
    GuildState.AppendBytes(bytearray([0x01, 0x00, 0x86, 0x12, 0x01, 0x00]))
    
    # Append member role and guild name
    if guild is None:
        
        # If the member is not part of a guild, the status should be 0
        GuildState.AppendBytes(bytearray([0x00]))
        
        # If we are in no guild, append 17 null bytes.
        for i in range(17):
            GuildState.AppendBytes(bytearray([0x00]))
    else:
        
        # If the character is applying to be in the guild, the status should be 1
        if guild['applying'] == 1:
            GuildState.AppendInteger(1, 1, 'little')
            
        # If the character is actually a member of the guild, the status should be 2
        else:
            GuildState.AppendInteger(2, 1, 'little')
        
        # Send guild name to client
        GuildState.AppendString(guild['name'], 17)
        
    GuildState.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00]))
    
    # If we are not in a guild, our status should be 0 in all cases
    if guild is None:
         GuildState.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00]))
         
    # Append guild leader status to the packet, 1 if leader but 0 if not
    else:
        GuildState.AppendInteger(int(guild['is_leader']), 4, 'little')
    
    # Send the guild state packet to the client
    client['socket'].send(GuildState.packet)
    
    # If we are in a guild, and if we are not applying to a guild, it is time to send the guild information packet
    if guild is None or guild['applying'] == 1:
        return
    
    GuildInfo = PacketWrite()
    GuildInfo.AddHeader(bytearray([0x45, 0x2F]))
    GuildInfo.AppendBytes(bytearray([0x01, 0x00]))
    GuildInfo.AppendString(guild['name'], 17)
    GuildInfo.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00]))
    GuildInfo.AppendString(guild['guild_master'], 15)
    GuildInfo.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00, 0x00, 0x00]))
    GuildInfo.AppendString(guild['created'].strftime('%Y-%m-%d %H:%M:%S'), 19)
    GuildInfo.AppendBytes(bytearray([0x00]))
    GuildInfo.AppendInteger(int(guild['member_count']), 4, 'little')
    GuildInfo.AppendInteger(int(guild['max_members']), 4, 'little')
    GuildInfo.AppendInteger(int(guild['guild_points']), 4, 'little')
    GuildInfo.AppendBytes(bytearray([0x01, 0x00, 0x00, 0x00]))
    client['socket'].send(GuildInfo.packet)
    
    # Build and send guild member list
    GuildMembers = PacketWrite()
    GuildMembers.AddHeader(bytearray([0x48, 0x2F]))
    GuildMembers.AppendBytes(bytearray([0x01, 0x00]))
    
    # Get all members belonging to this guild
    _args['mysql'].execute("""SELECT c.`name`, m.`points` FROM `guild_members` m
        JOIN `characters` c ON c.`id` = m.`character_id`
        WHERE m.`guild_id` = %s AND m.`applying` = 0""", [guild['id']])
    members = _args['mysql'].fetchall()
    
    # Append the character name and guild points for every member in the guild
    for member in members:
        GuildMembers.AppendString(member['name'], 15)
        GuildMembers.AppendInteger(member['points'], 4, 'little')
        
    # Since the client can handle up to 101 members, we'll have to append null bytes for the empty slots
    for _ in range(101 - len(members)):
        for _ in range(19):
            GuildMembers.AppendBytes(bytearray([0x00]))

    GuildMembers.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00]))
    client['socket'].send(GuildMembers.packet)

    if get_notice and guild['notice'] is not None and len(guild['notice']) > 0:
        Lobby.ChatMessage(_args['client'], "[Guild Notice] {}".format(guild['notice']), 8)
    
"""
Method:         Create
Description:    This method will handle guild creation requests
"""
def Create(**_args):
    
    # Character name, compare and do nothing if the two do not match
    character_name = _args['packet'].ReadString(1)
    if character_name != _args['client']['character']['name']:
        return

    # Check if we are already in a guild. If that's the case, just drop the packet and do nothing
    elif FetchGuild(_args, _args['client']['character']['id']) is not None:
        return

    # Read the guild name from the incoming packet
    guild_name = _args['packet'].ReadString().strip()

    # Create the result packet which we send after the creation of our guild
    result = PacketWrite()
    result.AddHeader(bytearray([0x3A, 0x2F]))

    # Check if we have enough gold/gigas
    if _args['client']['character']['currency_gigas'] < 30000:
        result.AppendBytes(bytearray([0x00, 0x04]))
        _args['socket'].send(result.packet)
        return

    # Check if our character is at least level 30
    elif _args['client']['character']['level'] < 30:
        result.AppendBytes(bytearray([0x00, 0x05]))
        _args['socket'].send(result.packet)
        return

    # Attempt to find a guild with the same name in the database, if the guild with the same name exists, we should stop
    _args['mysql'].execute("SELECT `id` FROM `guilds` WHERE `name` = %s", [guild_name])

    # If a guild with the same name exists, we should send the packet saying so.
    if len(_args['mysql'].fetchall()) > 0:
        print('guild found')
        result.AppendBytes(bytearray([0x00, 0x02]))
    else:
        try:
            _args['mysql'].execute("""INSERT INTO `guilds` (`leader_character_id`, `name`, `created`)
                VALUES (%s, %s, UTC_TIMESTAMP())""", [
                _args['client']['character']['id'],
                guild_name
            ])

            # Read the new guild ID and add our self to it as a leader and re-fetch the guild state
            guild_id = _args['mysql'].lastrowid
            AddMember(_args, _args['client']['character']['id'], guild_id)
            GetGuild(_args, _args['client'])

            # Transaction was successful, append the success status to our packet
            result.AppendBytes(bytearray([0x01, 0x00]))
        except Exception as e:

            # Transaction has failed, append failure status to packet
            result.AppendBytes(bytearray([0x00, 0x02]))

    # Send result no matter what
    _args['socket'].send(result.packet)

def SendGuildApplication(**_args):

    # Get guild membership
    guild = FetchGuild(_args, _args['client']['character']['id'])

    # We must be certain that we are not already in a guild. If we are, do nothing
    if guild is not None:
        return

    # Skip the first string (which would've been the character name) and read the guild name
    _args['packet'].ReadString(1)
    guild_name = _args['packet'].ReadString()

    # Obtain guild information
    _args['mysql'].execute("""SELECT `id`, `name` FROM `guilds` WHERE `name` = %s""", [guild_name])
    guild = _args['mysql'].fetchone()

    # Create result message packet
    result = PacketWrite()
    result.AddHeader(bytearray([0x3B, 0x2F]))

    if guild is None:
        result.AppendBytes(bytearray([0x00, 0x03]))
    else:
        AddMember(_args, _args['client']['character']['id'], guild['id'], 1)
        GetGuild(_args, _args['client'])
        result.AppendBytes(bytearray([0x01, 0x00]))

    # Send result message packet
    _args['socket'].send(result.packet)

def CancelGuildApplication(**_args):

    # Get guild membership and check if we are in a guild and are applying.
    # Do nothing otherwise.
    guild = FetchGuild(_args, _args['client']['character']['id'])
    if guild is None or guild['applying'] == 0:
        return

    # Delete application(s) for our character
    _args['mysql'].execute("""DELETE FROM `guild_members` WHERE `character_id` = %s AND `applying` = 1""", [
        _args['client']['character']['id']
    ])

    # Send success message
    result = PacketWrite()
    result.AddHeader(bytearray([0x3C, 0x2F]))
    result.AppendBytes(bytearray([0x01, 0x00]))
    _args['socket'].send(result.packet)

    # Fetch guild status again
    GetGuild(_args, _args['client'])

def FetchGuildApplications(**_args):

    # Get guild membership
    guild = FetchGuild(_args, _args['client']['character']['id'])

    # If we are not in a guild, or are not the leader, we should do nothing
    if guild is None or guild['is_leader'] == 0:
        return

    # Create application list packet
    applications = PacketWrite()
    applications.AddHeader(bytearray([0x49, 0x2F]))
    applications.AppendBytes(bytearray([0x01, 0x00]))

    # Fetch application list from the database
    _args['mysql'].execute("""SELECT c.`name`, c.`level` FROM `guild_members` m
        JOIN `characters` c ON c.`id` = m.`character_id`
        WHERE m.`guild_id` = %s AND m.`applying` = 1 LIMIT 10""", [
        guild['id']
    ])

    members = _args['mysql'].fetchall()

    # Loop through members and append to packet
    for member in members:
        applications.AppendString(member['name'], 15)
        applications.AppendInteger(member['level'], 4, 'little')
        applications.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00]))

    # Write null bytes to fix weird listings
    for _ in range(23 * (10 - len(members))):
        applications.AppendBytes(bytearray([0x00]))

    # Send packet to our client
    _args['socket'].send(applications.packet)

def AcceptApplication(**_args):

    # Get guild membership
    guild = FetchGuild(_args, _args['client']['character']['id'])

    # If we are not in a guild, or are not the leader, we should do nothing
    if guild is None or guild['is_leader'] == 0:
        return

    # Read character name from packet
    character_name = _args['packet'].ReadString(17)
    if character_name == _args['client']['character']['name']:
        return

    # Update the member record and refresh guild state
    _args['mysql'].execute("""UPDATE `guild_members` SET `applying` = 0 WHERE `guild_id` = %s 
        AND `character_id` = (SELECT `id` FROM `characters` WHERE `name` = %s) AND `applying` = 1""", [guild['id'], character_name])
    GetGuild(_args, _args['client'])

    # Send a notification to the remote player as well
    if _args['mysql'].rowcount > 0:
        client = _args['connection_handler'].GetCharacterClient(character_name)
        if client is not None:
            GetGuild(_args, client)
            Lobby.ChatMessage(client, "[Server] You have been accepted into guild [{}]!"
                              .format(guild['name']), 3)

def RejectApplication(**_args):

    # Get guild membership
    guild = FetchGuild(_args, _args['client']['character']['id'])

    # If we are not in a guild, or are not the leader, we should do nothing
    if guild is None or guild['is_leader'] == 0:
        return

    # Read character name from packet
    character_name = _args['packet'].ReadString(17)
    if character_name == _args['client']['character']['name']:
        return

    # Delete member from member table and refresh guild state
    _args['mysql'].execute("""DELETE FROM `guild_members` WHERE `guild_id` = %s
        AND `character_id` = (SELECT `id` FROM `characters` WHERE `name` = %s) AND `applying` = 1""", [guild['id'], character_name])
    GetGuild(_args, _args['client'])

def LeaveGuild(**_args):

    # Get guild membership
    guild = FetchGuild(_args, _args['client']['character']['id'])

    # Don't do anything if we're not in a guild
    if guild is None:
        return

    # Remove our character from the guild
    _args['mysql'].execute("""DELETE FROM `guild_members` WHERE `guild_id` = %s AND `character_id` = %s""", [
        guild['id'],
        _args['client']['character']['id']
    ])

    # Get all members belonging to this guild
    _args['mysql'].execute("""SELECT c.`name`, m.`points` FROM `guild_members` m
                JOIN `characters` c ON c.`id` = m.`character_id`
                WHERE m.`guild_id` = %s AND m.`applying` = 0""", [guild['id']])
    members = _args['mysql'].fetchall()

    # If we're the guild leader, find another member to make a leader.
    # We'll make the next person that joined after the current leader the new leader
    if guild['is_leader'] == 1:
        _args['mysql'].execute("""SELECT m.`character_id`, c.name FROM `guild_members` m
            JOIN `characters` c ON c.`id` = m.`character_id`
            WHERE m.`guild_id` = %s ORDER BY m.`id` ASC LIMIT 1""", [
            guild['id']
        ])

        new_leader = _args['mysql'].fetchone()

        # If our new leader does not exist, we will delete the guild forever (no more members)
        if new_leader is None:
            _args['mysql'].execute("""DELETE FROM `guilds` WHERE `id` = %s""", [
                guild['id']
            ])
        else:

            # If there is a new member, use the character ID and make it a leader
            _args['mysql'].execute("""UPDATE `guilds` SET `leader_character_id` = %s WHERE `id` = %s""", [
                new_leader['character_id'],
                guild['id']
            ])

        # For each member, send a message to their client indicating that their previous leader has left
        if len(members) > 0:
            for member in members:
                client = _args['connection_handler'].GetCharacterClient(member['name'])
                if client is not None:
                    GetGuild(_args, client)
                    Lobby.ChatMessage(client, "[Server] Your guild leader [{}] has left the guild ({})! The new leader is [{}]"
                                      .format(_args['client']['character']['name'], guild['name'], new_leader['name']), 3)

    else:

        # Send the guild master a notification that a member has left
        client = _args['connection_handler'].GetCharacterClient(guild['guild_master'])
        if client is not None:
            Lobby.ChatMessage(client, "[Server] [{}] has left your guild"
                              .format(_args['client']['character']['name']), 3)

        # Send the guild information packet to all online guild members including the master
        if len(members) > 0:
            for member in members:
                client = _args['connection_handler'].GetCharacterClient(member['name'])
                if client is not None:
                    GetGuild(_args, client)

    # We should always obtain the latest guild state despite our guild membership
    GetGuild(_args, _args['client'])

def ExpelGuildMember(**_args):

    # Get guild membership
    guild = FetchGuild(_args, _args['client']['character']['id'])

    # If we are not in a guild, or are not the leader, we should do nothing
    if guild is None or guild['is_leader'] == 0:
        return

    # Get character name of player we are going to kick
    character_name = _args['packet'].ReadString(17)
    if character_name == _args['client']['character']['name']:
        return

    # Remove character from guild
    _args['mysql'].execute("""DELETE FROM `guild_members`
    WHERE `guild_id` = %s AND `character_id` = (SELECT `id` FROM `characters` WHERE `name` = %s)""", [
        guild['id'],
        character_name
    ])

    # Refresh guild state for us and the character who has been removed from the guild, if the player is online
    GetGuild(_args, _args['client'])

    # Get remote client from the connection class and sync the guild and send a message
    if _args['mysql'].rowcount > 0:
        remote_client = _args['connection_handler'].GetCharacterClient(character_name)
        if remote_client is not None:
            GetGuild(_args, remote_client)
            Lobby.ChatMessage(remote_client, "[Server] You have been expelled from guild [{}]!".format(guild['name']), 3)

def UpdateGuildNotice(**_args):

    # Get guild membership
    guild = FetchGuild(_args, _args['client']['character']['id'])

    # If we are not in a guild, or are not the leader, we should do nothing
    if guild is None or guild['is_leader'] == 0:
        return

    guild_notice = _args['packet'].ReadString(17).strip()
    if len(guild_notice) == 1 and ord(guild_notice) == 1:
        guild_notice = ""

    # Update the guild notice
    _args['mysql'].execute("""UPDATE `guilds` SET `notice` = %s WHERE `id` = %s""", [
        guild_notice,
        guild['id']
    ])

    # Send guild notice to our own client\
    if len(guild_notice) > 0:
        Lobby.ChatMessage(_args['client'], "[Guild Notice] {}".format(guild_notice), 8)

def GetGuildNotice(**_args):

    # Get guild membership
    guild = FetchGuild(_args, _args['client']['character']['id'])

    if guild is None:
        return

def Chat(_args, message):

    # Get guild membership
    guild = FetchGuild(_args, _args['client']['character']['id'])

    # Don't do anything if we're not in a guild
    if guild is None:
        return

    # Get guild members
    _args['mysql'].execute("""SELECT c.`name`, m.`points` FROM `guild_members` m
        JOIN `characters` c ON c.`id` = m.`character_id`
        WHERE m.`guild_id` = %s AND m.`applying` = 0""", [guild['id']])
    members = _args['mysql'].fetchall()

    if len(members) > 0:
        for member in members:
            client = _args['connection_handler'].GetCharacterClient(member['name'])
            if client is not None:
                Lobby.ChatMessage(client, message, 5)

'''
Method:         invite
Description:    This method allows guild masters to invite new members in their guild through the lobby
'''
def invite(**_args):

    # Fetch guild membership and check if we are its leader. If not, do not proceed.
    guild = FetchGuild(_args, _args['client']['character']['id'])
    if guild is None or guild['is_leader'] == 0:
        return

    # Construct error packet, in the event that the remote client is unavailable
    error = PacketWrite()
    error.AddHeader([0x47, 0x2F])
    error.AppendBytes([0x00, 0x00])

    # Get target character name and check if the name does not match our own
    character_name = _args['packet'].ReadString(17).strip()

    # Get remote client from the character name received from the packet
    remote_client = _args['connection_handler'].GetCharacterClient(character_name)

    ''' Check if the client:
        1. Has been found
        2. Is not in a room
        3. Is not our own '''
    # Otherwise, we'll send an error indicating that the player can not respond at the moment
    if remote_client is None or 'room' in remote_client or remote_client is _args['client']:
        return _args['socket'].send(error.packet)

    # Check if the remote client is already in a guild. If so, we'll have to send an error as well.
    remote_guild = FetchGuild(_args, remote_client['character']['id'])
    if remote_guild is not None:
        return _args['socket'].send(error.packet)

    '''
    Create guild invite request session that expires after 12 seconds after being created
    '''
    session = _args['session_handler'].create(
        type            = 'guild_invite_request',
        clients         = [ remote_client ],
        data            = {'requester': _args['client'], 'guild': guild['id']},
        expires_after   = 12
    )

    # Create guild invite request and send it to the remote client
    request = PacketWrite()
    request.AddHeader(bytes=[0x62, 0x2B])
    request.AppendBytes(bytes=[0x01, 0x00])
    request.AppendString(_args['client']['character']['name'])
    _args['session_handler'].broadcast(session, request.packet)

'''
Method:         invitation_response
Description:    This method allows users to accept or deny guild invitations
'''
def invitation_response(**_args):

    # Read response and remote character name
    response            = int(_args['packet'].GetByte(0))
    remote_character    = _args['packet'].ReadString(19).strip()

    # Attempt to find the invitation session
    invitation_session = None
    for session in _args['server'].sessions:

        if session['type'] == 'guild_invite_request' \
            and _args['client'] in session['clients'] \
                and session['data']['requester']['character']['name'] == remote_character:
            invitation_session = session
            break

    # Create result packet
    result = PacketWrite()
    result.AddHeader(bytes=[0x47, 0x2F])

    # If we did not find any session, drop the packet and send an error
    if invitation_session is None:
        result.AppendBytes(bytes=[0x00, 0x00])  # Not logged in
        _args['socket'].send(result.packet)
        return

    # If we did find the session, destroy it and process the request further
    _args['session_handler'].destroy(invitation_session)

    # If the invitation has been refused, send the refusal packet to the remote client
    if response == 0:
        result.AppendBytes(bytes=[0x00, 0x01])  # The player has refused the invitation

        # Send packet to remote client
        try:
            invitation_session['data']['requester']['socket'].send(result.packet)
        except Exception as e:
            print('Failed to send invitation declined packet to remote client because: ', str(e))
        return

    # If we accepted the request, add our client to the guild and send guild sync packet to our client
    AddMember(_args, _args['client']['character']['id'], invitation_session['data']['guild'], applying=0)
    GetGuild(_args, _args['client'])

    # Finally, attempt to send the sync guild packet to the remote client
    # Additionally, attempt to send the success packet as well
    try:

        # Sync guild state
        GetGuild(_args, invitation_session['data']['requester'])

        # Success status
        result.AppendBytes(bytes=[0x01, 0x00])
        invitation_session['data']['requester']['socket'].send(result.packet)

    except Exception as e:
        print('Failed to send guild sync packet to remote client because: ', str(e))