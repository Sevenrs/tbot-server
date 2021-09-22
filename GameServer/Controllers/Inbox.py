#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0" 

from Packet.Write import Write as PacketWrite
from GameServer.Controllers import Lobby

"""
This file is responsible for handling all requests relating to the inbox functionality.
"""

"""
Method:         RequestInbox
Description:    This will handle the inbox request sent by the client
"""
def RequestInbox(**_args):
    GetInbox(_args)

"""
Method:         GetInbox
Description:    This method will get the user's inbox and send it back to our client.
                Since this method needs to be called multiple times throughout different commands, we need to ensure we can do that
"""
def GetInbox(_args):
    
    # Retrieve all messages where the receiver is our character ID
    _args['mysql'].execute("""SELECT IFNULL(c.`name`, '( deleted )') AS `sender`, i.`date` FROM inbox i
        LEFT JOIN `characters` c ON c.`id` = i.`sender_character_id`
        WHERE i.`receiver_character_id` = %s ORDER BY i.`id` DESC LIMIT 20""", [
             _args['client']['character']['id']
    ])
    
    # Fetch all messages
    messages = _args['mysql'].fetchall()
        
    # Create new packet
    message_packet = PacketWrite()
    message_packet.AddHeader(bytearray([0x10, 0x2F]))
    message_packet.AppendBytes(bytearray([0x01, 0x00]))
    
    # Append number of messages to packet
    message_packet.AppendInteger(len(messages), 2, 'little')
    
    # Append all messages
    for index, message in enumerate(messages):
        message_packet.AppendInteger((index + 1), 4, 'little')
        message_packet.AppendString(message['sender'], 15)
        message_packet.AppendString(message['date'].strftime('%Y-%m-%d %H:%M'), 17)
    
    # Send packet to our client
    _args['client']['socket'].send(message_packet.packet)
    
"""
Method:         SendMessage
Description:    This method will send messages to a target character
"""
def SendMessage(**_args):
    
    # Read sender (our local username)
    sender      = _args['packet'].ReadString(1)
    receiver    = _args['packet'].ReadString().strip()
    message     = _args['packet'].ReadString()
    
    # Create the result packet that contains the status within a message
    result = PacketWrite()
    result.AddHeader(bytearray([0x11, 0x2F]))
    
    # Attempt to send the message
    try:
        
        # Do not send the message if the receiver is equal to our own username
        if receiver.lower() == _args['client']['character']['name'].lower():
            raise Exception('User tried sending message to themselves')
        
        # Insert the message in the database, if there is an error then the character does not exist
        _args['mysql'].execute("""INSERT INTO `inbox` (`sender_character_id`, `receiver_character_id`, `message`, `date`)
            VALUES (%s, (SELECT `id` FROM `characters` WHERE `name` = %s), %s, UTC_TIMESTAMP())""", [
                _args['client']['character']['id'],
                receiver,
                message
            ])

        # If the remote player is online, send a notification to them
        remote_client = _args['connection_handler'].GetCharacterClient(receiver)
        if remote_client is not None:
            try:

                # Construct text notification and send to remote client
                Lobby.ChatMessage(target=remote_client,
                                  message='[Server] {0} has sent you a message'.format(
                                      _args['client']['character']['name']),
                                  color=1)

                # Construct and send notification packet
                notification = PacketWrite()
                notification.AddHeader([0x14, 0x2F])
                notification.AppendBytes([0x01, 0x00])
                remote_client['socket'].send(notification.packet)

            except Exception as e:
                print('[InboxController] Could not send message notification to remote client because: ', str(e))
            
        result.AppendBytes(bytearray([0x01, 0x00, 0x01, 0x00, 0x00]))
    except Exception as e:
        result.AppendBytes(bytearray([0x00, 0x33, 0x00, 0x00, 0x00]))
        
    _args['socket'].send(result.packet)

"""
Method:         RequestMessage
Description:    This method will obtain a specific message and send it to the client
"""
def RequestMessage(**_args):
    
    # Read message index
    message_index = int(_args['packet'].GetByte(17))
    
    # Find the message in the database
    _args['mysql'].execute("""SELECT IFNULL(c.`name`, '( deleted )') AS `sender`, i.`message`, i.`id` FROM inbox i
        LEFT JOIN `characters` c ON c.`id` = i.`sender_character_id`
        WHERE i.`receiver_character_id` = %s ORDER BY i.`id` DESC LIMIT 1 OFFSET %s""", [
            _args['client']['character']['id'],
            (message_index - 1)
    ])
    
    # Fetch the result, do nothing if nothing has been found
    result = _args['mysql'].fetchone()
    if result is None:
        return
    
    # Create new packet and send to the client
    message = PacketWrite()
    message.AddHeader(bytearray([0x12, 0x2F]))
    message.AppendBytes(bytearray([0x01, 0x00]))
    message.AppendString(result['sender'], 15)
    message.AppendString(result['message'], 98)
    _args['socket'].send(message.packet)

    # Mark message as read
    _args['mysql'].execute('''UPDATE `inbox` SET `read` = 1 WHERE `id` = %s''', [result['id']])

    # Run the unread notification function to see if we need to show a notification for unread messages
    unread_message_notification(_args)

"""
Method:         DeleteMessage
Description:    This method will delete a specific message from the user's inbox
"""
def DeleteMessage(**_args):
    
    # Get message index from client
    message_index = _args['packet'].GetByte(17)
    
    # Remove message from the database
    _args['mysql'].execute("""DELETE FROM `inbox` WHERE `id` = (SELECT `id` FROM `inbox` WHERE `receiver_character_id` = %s
                           ORDER BY `id` ASC LIMIT 1 OFFSET %s) AND `receiver_character_id` = %s""", [
        _args['client']['character']['id'],
        (message_index - 1),
        _args['client']['character']['id']
    ])
    
    # Reload inbox
    GetInbox(_args)

'''
Method:         unread_message_notification
Description:    If our client has at least one unread message, a flashing inbox icon will be shown for the client.
                This method returns the number of unread messages to the stack.
'''
def unread_message_notification(_args):

    # Get number of unread messages
    _args['mysql'].execute('''SELECT `id` FROM `inbox` WHERE `receiver_character_id` = %s AND `read` = 0''', [
        _args['client']['character']['id']
    ])

    # Retrieve amount of unread messages
    unread_messages = _args['mysql'].rowcount

    # Create notification packet
    notification = PacketWrite()
    notification.AddHeader([0x14, 0x2F])
    notification.AppendBytes([0x01, 0x00] if unread_messages > 0 else [0x00, 0x00, 0x00, 0x00, 0x00, 0x00])
    _args['socket'].send(notification.packet)

    return unread_messages