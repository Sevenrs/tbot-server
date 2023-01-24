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
import requests


def route(client, packet):
    packets = {
        'f82a': authenticate
    }.get(packet.id, unknown)(**locals())


'''
This method will give users the possibility to authenticate
'''


def authenticate(**_args):
    # Read username and password from the packet
    username = _args['packet'].read_string()[1:]
    password = _args['packet'].read_string()

    # Construct result packet
    result = PacketWrite()
    result.add_header([0xEC, 0x2C])
    result.append_bytes([0x01, 0x00])

    # Read environment variables
    env = dotenv_values('.env')

    try:

        # Consume login rate limit point
        LOGIN_RATE_LIMIT.try_acquire('LOGIN_{0}'.format(_args['client']['address'][0]))

        # Send credentials to the internal web API
        response = requests.post("{0}/login".format(env['INTERNAL_ROOT_URL']),
                                 json={
                                     "username": username,
                                     "password": password,
                                     "ip": _args['client']['address'][0]
                                 },

                                 headers={
                                     "Content-Type": "application/json",
                                     "Authorization": env['INTERNAL_ACCESS_TOKEN']
                                 })

        # If the status code is not 200 OK, there's an error. Send the right error depending on said status code.
        if response.status_code != 200:

            # Deserialize the response
            response = response.json()

            # Check if the response contains errors. If not, throw an exception
            if len(response['errors']) <= 0:
                raise Exception('Invalid response from API')

            # Read last error from response, retrieve the status code from the status map and send result to the client
            error = response['errors'][0]['msg']
            status = STATUS_MAP[error] if error in STATUS_MAP else RESPONSE_ERROR

            # Append this status to the packet and send to the client
            result.append_integer(status, 1, 'little')
            result.append_bytes(PACKET_FOOTER)
            _args['client']['socket'].sendall(result.packet)
            return _args['client']['socket'].close()

        # If we have successfully logged in, check if we have a user on record with the web ID provided by the service
        web_id = response.json()['web_id']

        # Create a new user if we have to
        connection = MySQL.get_connection()
        cursor = connection.cursor(dictionary=True)
        cursor.execute(
            '''INSERT INTO `users` (`external_id`) SELECT %s FROM DUAL WHERE NOT EXISTS (SELECT * FROM `users` WHERE 
            `external_id`= %s LIMIT 1) ''',
            [
                web_id,
                web_id
            ])

        # Close MySQL connection
        connection.close()

        result.append_integer(RESPONSE_SUCCESS, 1, 'little')  # Add success status to the packet and send to the client

        # Append war-net bonus status to the packet. It's 1 if there's a bonus,
        result.append_bytes([0x00, (0x01 if response.json()['warnet_bonus'] else 0x00)])
        result.append_bytes(PACKET_FOOTER[2:])  # Skip the first two bytes because we've manually written those above

    except Exception:

        # In case of an error, send the RESPONSE_ERROR status to the client
        result.append_integer(RESPONSE_ERROR, 1, 'little')
        result.append_bytes(PACKET_FOOTER)

    _args['client']['socket'].sendall(result.packet)
    return _args['client']['socket'].close()


def unknown(**_args):
    print("[{0}]: Unknown packet: <0x{1}[len={3}]::{2}>".format(_args['client']['server'].name, _args['packet'].id,
                                                                _args['packet'].data, len(_args['packet'].data)))
