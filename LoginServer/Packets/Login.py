#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

from enum import IntEnum
import MySQL.Interface as MySQL
import bcrypt

"""
This file is responsible for handling authentication requests
"""

"""
Possible authentication results
"""
class AUTH_RESULT(IntEnum):
    ERROR               = 0xA6  # Sent when something goes wrong on our end.
    LIMIT               = 0x05  # Sent when the user has failed to login too many times.
    USER_BANNED         = 0x03  # Sent when the user has been banned.
    USER_NOT_FOUND      = 0x02  # Sent when the user was not found in the database.
    INCORRECT_PASS      = 0x01  # Sent when the password is incorrect.
    SUCCESS             = 0x00  # Sent when everything is OK.

"""
This method will authenticate a user
"""
def Authenticate(socket, packet):

    # Get username and password from request
    username = packet.ReadString()[1:]
    password = packet.ReadString()
    
    # Check crendentials
    try:
        
        # Create MySQL connection and get cursor
        connection = MySQL.GetConnection()
        cursor = connection.cursor(dictionary=True)
        
        # Find user by username
        cursor.execute('SELECT `id`, `password`, `banned` FROM `users` WHERE `username` = %s', [username])
        user = cursor.fetchone()
        
        # Check if the user exists
        if user is None:
            RESULT = AUTH_RESULT.USER_NOT_FOUND
            
        # Check user password
        elif not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            RESULT = AUTH_RESULT.INCORRECT_PASS
            
        # Check if the user has been banned
        elif user["banned"] == 1:
            RESULT = AUTH_RESULT.USER_BANNED
            
        # If all checks have been passed without error, send a success status
        else:
            RESULT = AUTH_RESULT.SUCCESS
        
        # Close the database connection at this point
        connection.close()
        
    except Exception as e:
        
        # If any error occurs, send an authentication error message back to the client
        RESULT = AUTH_RESULT.ERROR
        print(e)
        
    # Send reply to consuming client
    socket.send(bytearray([
        0xEC, 0x2C, 0x4A, 0x00, 0x01, 0x00, RESULT, 0x00, 0x00, 0x01, 0x00, 0x0F, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00,
        0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00
    ]))
    socket.close()
