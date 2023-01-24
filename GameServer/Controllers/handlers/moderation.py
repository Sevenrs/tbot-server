__author__ = 'Icseon'

import requests
from dotenv import dotenv_values

'''
This method will suspend a player from the game
'''


def suspend_player(web_id, connection_handler=None, client=None):
    print('[moderation@suspend_player()] :: suspending player with web_id: {0}'.format(web_id))

    # Read environment variables
    env = dotenv_values('.env')

    # Attempt to send a PUT request that suspends the player in question
    requests.put('{0}/moderation/suspend-user'.format(env['INTERNAL_ROOT_URL']),
                 json={'web_id': web_id},
                 headers={
                     'Content-Type': 'application/json',
                     'Authorization': env['INTERNAL_ACCESS_TOKEN']
                 })

    # If the connection handler and client have both been provided, disconnect the client from the game server.
    if connection_handler is not None and client is not None:
        connection_handler.update_player_status(client, 2)
