import datetime
import random

from GameServer.Controllers import Room, Lobby
from GameServer.Controllers.data.game import MODE_PLANET
from Packet.Write import Write as PacketWrite


def register(room):
    for event in ['start_game', 'load_finish']:
        Room.register_callback(room, event, 'event_christmas')


def start_game(_args, room):
    # If it is not between december 18th and 31, do not proceed
    if not (datetime.datetime.now().month == 12 and (18 <= datetime.datetime.now().day <= 31)):
        return

    # Generate a random number
    chance = random.randint(0, 5)
    if chance in [4, 5] and room['game_type'] == MODE_PLANET:
        Room.add_callback_data(room, 'event_boss', 99)


def load_finish(_args, room):
    # If the event boss was assigned to callback data, dispatch the event boss packet to all clients
    if 'event_boss' in room['callback_data']:
        event_boss = PacketWrite()
        event_boss.add_header([0x20, 0x27])
        event_boss.append_bytes([0x01, 0x00])
        _args['connection_handler'].room_broadcast(room['id'], event_boss)

        messages = [
            'Disturbance! Something is not right. There is a foreign entity present on this planet',
            'Hm... We could not find the boss of this planet. Let\'s figure out what\'s going on',
            'The temperature has dropped near the end of this planet... could it be?',
            'These enemies seem to have lost track of their leader'
        ]

        message = Lobby.chat_message(target=None,
                                     message=messages[random.randint(0, len(messages) - 1)],
                                     color=3,
                                     return_packet=True)
        _args['connection_handler'].room_broadcast(room['id'], message)
