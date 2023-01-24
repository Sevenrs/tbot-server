__author__ = 'Icseon'

import requests
from dotenv import dotenv_values

'''
This method will suspend a player from the game
'''


def suspend_player(_args, user_id, connection_handler=None, client=None):
    print('[moderation@suspend_player()] :: suspending player with user id: {0}'.format(web_id))

    # Suspend the user
    _args['mysql'].execute('''UPDATE `users` SET `suspended` = 1 WHERE `id` = ?''', [
        user_id
    ])

    # If the connection handler and client have both been provided, disconnect the client from the game server.
    if connection_handler is not None and client is not None:
        connection_handler.update_player_status(client, 2)
