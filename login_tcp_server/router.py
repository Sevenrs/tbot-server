#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2021 Icseon"
__version__ = "2.0"

'''
This file is responsible for handling all login packets
'''

from Packet.Write import Write as PacketWrite
import MySQL.Interface as MySQL
from login_tcp_server.data.authenticate import *
from ratelimit import LOGIN_RATE_LIMIT
from dotenv import dotenv_values
from pyrate_limiter import BucketFullException
import argon2


def route(client, packet):
    packets = {
        'f82a': login
    }.get(packet.id, unknown)(**locals())


'''
This method will validate the username and password and will return a status
'''


def authenticate(username, password, ip_address, mysql_cursor):

    # Attempt to find the user in the database
    mysql_cursor.execute('''SELECT * FROM `users` WHERE `username` = %s''', [username])
    user = mysql_cursor.fetchone()

    # Initialize a default state object
    state = {
        "status": None,
        "warnet": False
    }

    try:

        # If the user couldn't be found, we're going to return RESPONSE_USER_NOT_FOUND
        if user is None:
            state['status'] = RESPONSE_USER_NOT_FOUND
            return state

        # Verify user password
        argon2.PasswordHasher().verify(user['password'], password)

        # If the user hasn't verified their email yet, we'll return RESPONSE_EMAIL_UNVERIFIED
        if user['email_verified'] == 0:
            state['status'] = RESPONSE_EMAIL_UNVERIFIED
            return state

        # If the user has been suspended, we'll return RESPONSE_USER_SUSPENDED
        if user['suspended'] == 1:
            state['status'] = RESPONSE_USER_SUSPENDED
            return state

        # If we're still there, we've successfully authenticated. Update the last IP address
        mysql_cursor.execute('''UPDATE `users` SET `last_ip` = %s WHERE `username` = %s''', [
            ip_address,
            username
        ])

        # Update state accordingly and return the state
        state['status'] = RESPONSE_SUCCESS
        state['warnet'] = user['warnet_bonus'] == 1

    # Handle incorrect passwords
    except argon2.exceptions.VerifyMismatchError:
        LOGIN_RATE_LIMIT.try_acquire('LOGIN_{0}'.format(ip_address))
        state['status'] = RESPONSE_INCORRECT_PASSWORD

    # Handle rate limit
    except BucketFullException:
        state['status'] = RESPONSE_RATE_LIMIT

    return state


'''
This method will give users the possibility to authenticate
'''


def login(**_args):
    # Read username and password from the packet. We'll be skipping one character (H) with the username.
    username = _args['packet'].read_string()[1:]
    password = _args['packet'].read_string()

    # Create a new MySQL connection. We're going to require it to we can start finding the user of relevance.
    connection = MySQL.get_connection()
    cursor = connection.cursor(dictionary=True)

    # Let's see what the authentication result is
    authentication_result = authenticate(username=username,
                                         password=password,
                                         ip_address=_args['client']['address'][0],
                                         mysql_cursor=cursor)

    # Construct result packet
    result = PacketWrite()
    result.add_header([0xEC, 0x2C])
    result.append_bytes([0x01, 0x00])

    # Add result status to the packet
    result.append_integer(authentication_result['status'], 1, 'little')

    # Add warnet state to the packet
    result.append_bytes([0x00, authentication_result['warnet']])

    # Add the packet footer - skip first two bytes as we've just written them
    result.append_bytes(PACKET_FOOTER[2:])

    # Send the result packet and close the connection
    _args['client']['socket'].sendall(result.packet)
    return _args['client']['socket'].close()


def unknown(**_args):
    print("[{0}]: Unknown packet: <0x{1}[len={3}]::{2}>".format(_args['client']['server'].name, _args['packet'].id,
                                                                _args['packet'].data, len(_args['packet'].data)))
