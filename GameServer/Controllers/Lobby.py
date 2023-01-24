#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Guild, Friend, Room, block
from GameServer.Controllers.Character import get_items
from GameServer.Controllers.data.lobby import LOBBY_MSG
from GameServer.Controllers.Inbox import unread_message_notification
from GameServer.Controllers.gifts import gift_count
from ratelimit import CHAT_RATE_LIMIT
from pyrate_limiter import BucketFullException
import os

"""
This method will send a chat message to a specific target client
If the return_packet boolean is True, the packet is not sent but returned to the stack
"""


def chat_message(target, message, color, return_packet=False):
    # Construct chat packet
    result = PacketWrite()
    result.add_header(bytearray([0x1A, 0x27]))
    result.append_bytes(bytearray([0x00, 0x00, 0x00, 0x00]))
    result.append_integer(color, 1)
    result.append_bytes(bytearray([0x00]))
    result.append_string(message)
    result.append_bytes(bytearray([0x00, 0x00, 0x00, 0x00, 0x00]))

    # If we want to use the chat packet itself, return the packet to the stack
    if return_packet:
        return result.packet

    # Otherwise, send the packet to the intended target
    try:
        target['socket'].sendall(result.packet)
    except Exception:
        pass


"""
This method will handle chat requests
"""


def chat(**_args):
    # Read incoming message from the client
    message_type = _args['packet'].get_byte(4)
    message = _args['packet'].read_string(6)
    message_username = _args['client']['character']['name']

    # If the message is a guild chat, send the message to all members in the user's guild
    if int(message_type) == 5:
        return Guild.chat(_args, message)

    # Consume chat rate limit point
    try:
        CHAT_RATE_LIMIT.try_acquire('CHAT_{0}'.format(_args['client']['account_id']))

        # Determine the scope of the message we are about to send
        clients = _args['connection_handler'].get_lobby_clients() if _args['client']['character']['position'] == 0 \
            else _args['connection_handler'].get_clients()

        # Broadcast message to all clients in the scope
        for client in clients:
            chat_message(target=client,
                         message="[{0}] {1}".format(message_username, message[message.find(']') + 2:]),
                         color=_args['client']['character']['position'])
    except BucketFullException:

        # Send warning message to the client
        chat_message(target=_args['client'], message="[Warning] You are sending messages too fast.", color=2)


def whisper(**_args):
    """
    Get the target username
    """
    target = _args['packet'].read_string(1)

    """
    We should never trust the client (users can fake their username without the server ever knowing).
    And so, we should let the server reconstruct the message.
    This method will work, as long we keep the same structure the client expects.
    """
    client_message = _args['packet'].read_string()
    whisper_message = "[{0}]Whisper\r: {1}".format(_args['client']['character']['name'],
                                                   client_message[client_message.find(':') + 2:])

    # Attempt to obtain the user from the user dictionary. If we can not find the user, the user is offline.
    result = _args['connection_handler'].get_character_client(target)

    # Construct whisper packet
    whisper_packet = PacketWrite()
    whisper_packet.add_header([0x2B, 0x2F])

    # If the user was never found, send the player offline packet
    if result is None:
        whisper_packet.append_bytes(bytearray([0x00, 0x6B, 0x00, 0x00]))
    else:

        """
        Send the whisper packet to the target client.
        We should also make sure to calculate the new length ourselves
        due to clients having the ability to exploit packet edits to crash people's clients.
        """
        whisper_packet.append_bytes(bytearray([0x01, 0x00]))
        whisper_packet.append_integer(len(whisper_message), 2, 'little')
        whisper_packet.append_string(whisper_message)
        whisper_packet.append_bytes(bytearray([0x00]))
        result['socket'].sendall(whisper_packet.packet)

    # Always send the result to our client
    _args['socket'].sendall(whisper_packet.packet)


'''
This method allows players to examine others in the lobby.
It does not require the other player to be online.
'''


def examine_player(**_args):

    # Read username from the packet
    username = _args['packet'].read_string()

    # Retrieve the character id from the database and proceed to get the wearing items
    _args['mysql'].execute('SELECT `id`, `level`, `type`, `name`, `experience` FROM `characters` WHERE `name` = %s',
                           [username])
    character = _args['mysql'].fetchone()

    # If the character was not found send the user not found packet
    if character is None:
        return _args['socket'].sendall(bytearray([0x2B, 0x2F, 0x02, 0x00, 0x00, 0x33]))

    # Attempt to retrieve the client by the username
    remote_client = _args['connection_handler'].get_character_client(username)

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
    examination.add_header(bytearray([0x27, 0x2F]))
    examination.append_integer(0 if character['name'] != _args['client']['character']['name']
                               else character['experience'], 4, 'little')

    examination.append_integer(character['level'], 2, 'little')  # Character level
    examination.append_integer(room_id, 2, 'little')  # Room ID

    # Send character parts and gear
    for i in range(0, 11):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        examination.append_integer(item['id'], 4, 'little')

    # Send coin parts
    for i in range(17, 19):
        item = wearing_items['items'][list(wearing_items['items'].keys())[i]]
        examination.append_integer(item['id'], 4, 'little')

    examination.append_integer(0 if room is None else 1, 1, 'little')  # In-room status
    examination.append_integer(character['type'], 1, 'little')  # Character type
    examination.append_bytes([0x01, 0x00])  # Request status
    examination.append_string(character['name'], 15)  # Character name

    # Send examination packet to the client
    _args['socket'].sendall(examination.packet)


"""
This method will load the lobby
"""


def get_lobby(**_args):
    lobby_packet = PacketWrite()

    # Packet header
    lobby_packet.add_header(bytearray([0xF2, 0x2E]))
    lobby_packet.append_bytes([0x01, 0x00])

    # Amount of players
    clients = _args['connection_handler'].get_clients()
    lobby_packet.append_integer(len(clients), 2, 'little')

    for client in clients:
        lobby_packet.append_string(client['character']['name'], 15)
        lobby_packet.append_integer(client['character']['type'], 1)
        lobby_packet.append_bytes([0x01])

    lobby_packet.append_bytes([0x02, 0x01, 0x00, 0x00, 0x00, 0x00])
    _args['socket'].sendall(lobby_packet.packet)

    # For each player that is in a room, send an additional status packet
    for client in clients:

        # If the client is not in a room, do not send the additional status packet
        if 'room' not in client:
            continue

        # Construct status packet and send it to our own socket
        status = PacketWrite()
        status.add_header([0x27, 0x27])
        status.append_bytes([0x01, 0x00])
        status.append_string(client['character']['name'], 15)
        status.append_integer(client['character']['type'], 1, 'little')
        status.append_integer(0, 1, 'little')
        _args['socket'].sendall(status.packet)

    # If this is the first time that this client has requested the lobby, notify all their friends and retrieve the
    # block list
    if _args['client']['new']:

        # Retrieve block list
        block.get_blocks(_args)

        # Notify all friends
        Friend.presence_notification(_args)

        # Send welcome message to our client
        chat_message(_args['client'], LOBBY_MSG[0], LOBBY_MSG[1])

        # Update client status
        _args['client']['new'] = False

    # Get amount of unread messages and gift count. Also send a message notification packet if we have to.
    unread_messages, gifts = unread_message_notification(_args), gift_count(_args)
    chat_message(_args['client'],
                 "[Server] You have {0} unread message(s) and {1} gift(s)".format(unread_messages, gifts), 1)

    # Get guild membership
    Guild.get_guild(_args, _args['client'], True)

    # Load friends
    Friend.retrieve_friends(_args, _args['client'])


def room_list(**_args):

    # Read mode and page from packet
    page = _args['packet'].get_byte(2)
    mode = _args['packet'].get_byte(4)

    Room.get_list(_args, mode, page)
