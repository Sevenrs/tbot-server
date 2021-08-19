#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Guild, Friend, Room
from GameServer.Controllers.Character import get_items
from GameServer.Controllers.data.lobby import LOBBY_MSG
import os
    
"""
This method will send a chat message to a specific target client
"""
def ChatMessage(target, message, color, return_packet=False):
    chat = PacketWrite()
    chat.AddHeader(bytearray([0x1A, 0x27]))
    chat.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00]))
    chat.AppendInteger(color, 1)
    chat.AppendBytes(bytearray([0x00]))
    chat.AppendString(message)
    chat.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00, 0x00]))

    # If we want to use the chat packet itself, return the packet to the stack
    if return_packet:
        return chat.packet

    # Otherwise, send the packet to the intended target
    try:
        raise Exception('test')
        target['socket'].send(chat.packet)
    except Exception as e:
        print(target['socket'])
        print(e)

        f = open("chat_errors.txt", "a")
        f.write(str(e) + "\n")
        f.write(str(target['socket']) + "\n")
        f.close()
"""
This method will handle chat requests
"""
def Chat(**_args):
    message = _args['packet'].ReadString(6)
    chat_message = "[{0}] {1}".format(_args['client']['character']['name'], message[message.find(']') + 2:])
    chat_type = _args['packet'].GetByte(4)

    command_msg = message[message.find(']') + 2:]
    if command_msg[0:11] == '@changeslot':

        # Drop invalid ranges
        if int(command_msg[12]) < 1 or int(command_msg[12]) > 3:
            return

        _args['mysql'].execute('UPDATE `users` SET `active_bot_slot` = (%s - 1) WHERE `username` = %s', [
            command_msg[12],
            _args['client']['account']
        ])

        # try to kick the user to the channel list, to make sure that works
        exit = PacketWrite()
        exit.AddHeader(bytearray([0x0A, 0x2F]))
        exit.AppendBytes(bytearray([0x01, 0x00]))
        _args['socket'].send(exit.packet)
        _args['connection_handler'].CloseConnection(_args['client'])
        return

    if int(chat_type) == 5:
        Guild.Chat(_args, message)
    else:

        # Retrieve all clients that are currently not in a room, but are connected.
        clients = _args['connection_handler'].get_lobby_clients()

        # Depending on the position of the player, we need a different scope of clients
        # If the player a staff member, retrieve all clients
        if _args['client']['character']['position'] != 0:
            clients = _args['connection_handler'].GetClients()

        # Send the message to the right clients
        for client in clients:
            ChatMessage(client, chat_message, _args['client']['character']['position'])

def Whisper(**_args):
    
    """
    Get the target username
    """
    target = _args['packet'].ReadString(1)
    
    """
    We should never trust the client (users can fake their username without the server ever knowing).
    And so, we should let the server reconstruct the message.
    This method will work, as long we keep the same structure the client expects.
    """
    client_message  = _args['packet'].ReadString()
    whisper_message = "[{0}]Whisper\r: {1}".format(_args['client']['character']['name'],
                                          client_message[client_message.find(':')+2:])
    
    # Attempt to obtain the user from the user dictionary. If we can not find the user, the user is offline.
    result = _args['connection_handler'].GetCharacterClient(target)
        
    # Contruct whisper packet
    whisper_packet = PacketWrite()
    whisper_packet.AddHeader([0x2B, 0x2F])
    
    # If the user was never found, send the player offline packet
    if result is None:
        whisper_packet.AppendBytes(bytearray([0x00, 0x6B, 0x00, 0x00]))
    else:
        
        """
        Send the whisper packet to the target client.
        We should also make sure to calculate the new length ourselves
        due to clients having the ability to exploit packet edits to crash people's clients.
        """
        whisper_packet.AppendBytes(bytearray([0x01, 0x00]))
        whisper_packet.AppendInteger(len(whisper_message), 2, 'little')
        whisper_packet.AppendString(whisper_message)
        whisper_packet.AppendBytes(bytearray([0x00]))
        result['socket'].send(whisper_packet.packet)
    
    # Always send the result to our client
    _args['socket'].send(whisper_packet.packet)

'''
This method allows players to examine others in the lobby.
It does not require the other player to be online.
'''
def examine_player(**_args):

    # Read username from the packet
    username = _args['packet'].ReadString()

    # Retrieve the character id from the database and proceed to get the wearing items
    _args['mysql'].execute('SELECT `id`, `level`, `type`, `name`, `experience` FROM `characters` WHERE `name` = %s', [username])
    character = _args['mysql'].fetchone()

    # If the character was not found send the user not found packet
    if character is None:
        return  _args['socket'].send(bytearray([0x2B, 0x2F, 0x02, 0x00, 0x00, 0x33]))

    # Attempt to retrieve the client by the username
    remote_client = _args['connection_handler'].GetCharacterClient(username)

    # Define room and room ID this character is in. Default to nothing.
    room, room_id = None, 0

    # If the remote client has been found and is in a room, retrieve room information
    if remote_client is not None and 'room' in remote_client:
        room = _args['server'].rooms[str(remote_client['room'])]
        room_id = (room['client_id'] + 1) - (1500 if room['game_type'] == 4 else 0)

    # Retrieve wearing items
    wearing_items = get_items(_args, character['id'], 'wearing')

    # Create examination packet
    examination = PacketWrite()
    examination.AddHeader(bytearray([0x27, 0x2F]))
    examination.AppendInteger(0 if character['name'] != _args['client']['character']['name']
                              else character['experience'], 4, 'little')

    examination.AppendInteger(character['level'], 2, 'little')  # Character level
    examination.AppendInteger(room_id, 2, 'little')             # Room ID

    # Send character parts and gear
    for i in range(0, 11):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        examination.AppendInteger(item['id'], 4, 'little')

    # Send coin parts
    for i in range(17, 19):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        examination.AppendInteger(item['id'], 4, 'little')

    examination.AppendInteger(0 if room is None else 1, 1, 'little')    # In-room status
    examination.AppendInteger(character['type'], 1, 'little')           # Character type
    examination.AppendBytes([0x01, 0x00])                               # Request status
    examination.AppendString(character['name'], 15)                     # Character name

    # Send examination packet to the client
    _args['socket'].send(examination.packet)


"""
This method will load the lobby
"""
def GetLobby(**_args):
    lobby_packet = PacketWrite()

    # Packet header
    lobby_packet.AddHeader(bytearray([0xF2, 0x2E]))
    lobby_packet.AppendBytes([0x01, 0x00])

    # Amount of players
    clients = _args['connection_handler'].GetClients()
    lobby_packet.AppendInteger(len(clients), 2, 'little')

    for client in clients:
        lobby_packet.AppendString(client['character']['name'], 15)
        lobby_packet.AppendInteger(client['character']['type'], 1)
        lobby_packet.AppendBytes([0x01])

    lobby_packet.AppendBytes([0x02, 0x01, 0x00, 0x00, 0x00, 0x00])
    _args['socket'].send(lobby_packet.packet)

    # For each player that is in a room, send an additional status packet
    for client in clients:

        # If the client is not in a room, do not send the additional status packet
        if 'room' not in client:
            continue

        # Construct status packet and send it to our own socket
        status = PacketWrite()
        status.AddHeader([0x27, 0x27])
        status.AppendBytes([0x01, 0x00])
        status.AppendString(client['character']['name'], 15)
        status.AppendInteger(3, 1, 'little')
        status.AppendInteger(0, 1, 'little')
        _args['socket'].send(status.packet)

    # Load friends
    Friend.RetrieveFriends(_args, _args['client'])

    # Get guild membership
    Guild.GetGuild(_args, _args['client'], True)

    # If this is the first time that this client has requested the lobby, notify all their friends
    if _args['client']['new']:

        # Notify all friends
        Friend.PresenceNotification(_args)

        # Send welcome message to our client
        ChatMessage(_args['client'], LOBBY_MSG[0], LOBBY_MSG[1])

        # Update client status
        _args['client']['new'] = False

def RoomList(**_args):

    # Read mode and page from packet
    page = _args['packet'].GetByte(2)
    mode = _args['packet'].GetByte(4)

    Room.get_list(_args, mode, page)