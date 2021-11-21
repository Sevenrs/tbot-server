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
    username    = _args['packet'].ReadString()[1:]
    password    = _args['packet'].ReadString()

    # Construct result packet
    result = PacketWrite()
    result.AddHeader([0xEC, 0x2C])
    result.AppendBytes([0x01, 0x00])

    # Read environment variables
    env = dotenv_values('.env')

    try:

        # Send credentials to the internal web API
        response = requests.post("{0}/login".format(env['INTERNAL_ROOT_URL']),
                                 json={
                                     "username":    username,
                                     "password":    password,
                                     "ip":          _args['client']['address'][0]
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
            error   = response['errors'][0]['msg']
            status  = STATUS_MAP[error] if error in STATUS_MAP else RESPONSE_ERROR

            # Append this status to the packet and send to the client
            result.AppendInteger(status, 1, 'little')
            result.AppendBytes(PACKET_FOOTER)
            _args['client']['socket'].send(result.packet)
            return _args['client']['socket'].close()

        # If we have successfully logged in, check if we have a user on record with the web ID provided by the service
        web_id = response.json()['web_id']

        # Create a new user if we have to
        connection  = MySQL.GetConnection()
        cursor      = connection.cursor(dictionary=True)
        cursor.execute('''INSERT IGNORE INTO `users` SET `external_id` = %s''', [
            web_id
        ])

        # Close MySQL connection
        connection.close()

        # Append success status to the packet and send to the client and close the connection
        result.AppendInteger(RESPONSE_SUCCESS, 1, 'little')

    except Exception:
        result.AppendInteger(RESPONSE_ERROR, 1, 'little')

    result.AppendBytes(PACKET_FOOTER)
    _args['client']['socket'].send(result.packet)
    return _args['client']['socket'].close()


def unknown(**_args):
    print("[{0}]: Unknown packet: <0x{1}[len={3}]::{2}>".format(_args['client']['server'].name, _args['packet'].id,
                                                                _args['packet'].data, len(_args['packet'].data)))