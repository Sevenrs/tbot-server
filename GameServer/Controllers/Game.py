#!/usr/bin/env python3
__author__      = 'Icseon'
__copyright__   = 'Copyright (C) 2021 Icseon'
__version__     = '1.0'

from Packet.Write import Write as PacketWrite
from GameServer.Controllers.data.drops import *
from GameServer.Controllers.data.exp import *
from GameServer.Controllers.data.planet import PLANET_MAP_TABLE
from GameServer.Controllers.Room import get_room, get_slot, get_list, get_list_page_by_room_id, reset
from GameServer.Controllers.Character import get_items
import MySQL.Interface as MySQL
import random
import time
import _thread

"""
This controller is responsible for handling all game related actions
"""

'''
This method will tell the room that the client has finished loading the map
If a client has not loaded the map, the ready packet will not be sent yet
'''
def load_finish(**_args):

    # Get room and check if we are in one
    room = get_room(_args)
    if not room:
        return

    # Get slot and update loading status
    room['slots'][str(get_slot(_args, room))]['loaded'] = True

    # Check if the other slots have loaded
    for slot in room['slots']:
        if not room['slots'][slot]['loaded']:
            return

    # If all clients are ready to play, send the ready packet
    ready = PacketWrite()
    ready.AddHeader(bytearray([0x24, 0x2F]))
    ready.AppendBytes(bytearray([0x00]))
    _args['connection_handler'].SendRoomAll(_args['client']['room'], ready.packet)

    # Start new countdown timer thread
    _thread.start_new_thread(countdown_timer, (_args, room,))

'''
This method will handle monster deaths and broadcasts an acknowledgement to the room
of the monster being killed.
'''
def monster_kill(**_args):

    # If the client is not in a room or is not its master, drop the packet
    room = get_room(_args)
    if not room:
        return

    # Read monster ID from the packet
    monster_id = _args['packet'].GetByte(0)

    # Construct canister drops and drop chances
    drops = [
        (CANISTER_HEALTH, 0.05),
        (CANISTER_REBIRTH, 0.02),
        (CANISTER_STUN, 0.01),
        (CANISTER_BOMB, 0.02),
        (CANISTER_TRANS_UP, 0.01),
        (CANISTER_AMMO, 0.01)
    ]

    # Calculate whether or not we should drop an item based on chance
    monster_drops = []
    for drop, chance in drops:
        if random.random() < chance and room['drop_index'] < 256:
            monster_drops.append(bytes([room['drop_index'], drop, 0, 0, 0]))
            room['drop_index'] += 1
    drop_bytes = b''.join(monster_drops)

    # Create death response
    death = PacketWrite()
    death.AddHeader(bytes=bytearray([0x25, 0x2F]))
    death.AppendBytes(bytes=bytearray([0x01, 0x00]))
    death.AppendInteger(integer=monster_id, length=2, byteorder='little')

    death.AppendBytes([0x01, 0x00])
    death.AppendInteger(len(monster_drops), length=2, byteorder='little')
    death.AppendBytes(drop_bytes)

    # Broadcast the response to all sockets in the room
    _args['connection_handler'].SendRoomAll(room['id'], death.packet)

'''
This method will handle picking up items which were dropped from monsters
'''
def use_item(**_args):

    # If the client is not in a room, drop the packet
    room = get_room(_args)
    if not room:
        return

    # Read item index and type from packet
    item_index  = _args['packet'].GetByte(2)
    item_type   = _args['packet'].GetByte(3)

    print("Index: {0}, Type: {1}".format(item_index, item_type))

    use_canister = PacketWrite()
    use_canister.AddHeader(bytearray([0x23, 0x2F]))
    use_canister.AppendInteger(get_slot(_args, room) - 1, 2, 'little')
    use_canister.AppendInteger(item_index, 1, 'little')
    use_canister.AppendInteger(item_type, 4, 'little')
    _args['connection_handler'].SendRoomAll(room['id'], use_canister.packet)

'''
This method will handle player deaths.
It works by reading the slot number and broadcasting that the player is dead to all room sockets
'''
def player_death(**_args):

    # If the client is not in a room, drop the packet
    room = get_room(_args)
    if not room:
        return

    # Get slot number from the room
    room_slot = get_slot(_args, room)

    # Update room object and classify the player as dead
    room['slots'][str(room_slot)]['dead'] = True

    # Let the room know about the death of this player
    death = PacketWrite()
    death.AddHeader(bytearray([0x54, 0x2F]))
    death.AppendBytes(bytes=bytearray([0x01, 0x00]))
    death.AppendInteger(integer=(int(room_slot) - 1), length=2, byteorder='little')
    _args['connection_handler'].SendRoomAll(room['id'], death.packet)


'''
This method will handle the game end RPC. This acts as a caller for game_end through a packet instead of being
called manually in the game code.
'''
def game_end_rpc(**_args):

    # If the client is not in a room or is not its master, drop the packet
    room = get_room(_args, True)
    if not room:
        return

    game_end(_args=_args, room=room, status=(0 if _args['packet'].id == '3b2b' else 1))

'''
This method will send the correct packed to indicate what the game end result is to the room or specified client.
After this, it will start a new thread that will run the post-game transaction and show the game stats to the clients.
'''
def game_end(_args, room, status=0):

    # If the game is already over, there is not anything to do.
    if room['game_over']:
        return

    # The game is over. This is to avoid multiple calls to this method and to stop polling threads.
    room['game_over'] = True

    # If the room mode is equal to Planet and if the map is not defined in our data, we must assume the game has been lost
    if room['level'] not in PLANET_EXP_TABLE.keys():
        status = 0

    # Create game result packet and send it to all the room clients
    result = PacketWrite()
    result.AddHeader(bytes=bytearray([0x2A, 0x27]))
    result.AppendInteger(status, 2, 'little')
    _args['connection_handler'].SendRoomAll(room['id'], result.packet)

    # Start new thread for the game statistics
    _thread.start_new_thread(game_stats, (_args, room, status,))

'''
This method will update all characters in the room with their new results (if applicable)
Additionally, this method will return the results of the transaction in the form of a dictionary
'''
def post_game_transaction(_args, room, status):

    """
    Because we are not in the main thread, the database connection is not available to this method.
    We'll have to connect again in order to perform a database transaction.
    ---
    What we'll do is overwrite the object that would have been our mysql object if we were in the main thread
    """
    mysql_connection    = MySQL.GetConnection()
    _args['mysql']      = mysql_connection.cursor(dictionary=True)

    information = {}

    # Calculate new experience, level, etc for all players in the room
    for key, slot in room['slots'].items():

        # Retrieve character object belonging to this player
        character = slot['client']['character']

        # Obtain value additions, but default to 0 if we have lost the game
        addition_experience = PLANET_MAP_TABLE[room['level']][0][room['difficulty']] \
            if room['level'] in PLANET_MAP_TABLE.keys() and status == 1 else 0
        print(addition_experience)
        addition_gigas = 420 if status == 1 else 0

        # Check if we have leveled up
        level_up = character['experience'] + addition_experience >= EXP_TABLE[character['level'] + 1]
        if level_up:

            # Update our level and experience
            character['level'] += 1
            character['experience'] = 0
        else:

            # Update only our experience
            character['experience'] = character['experience'] + addition_experience

        # Calculate new gigas currency
        character['currency_gigas'] = character['currency_gigas'] + addition_gigas

        information[key] = {
            'addition_experience': addition_experience,
            'addition_gigas': addition_gigas,
            'experience': character['experience'],
            'gold': character['currency_gigas'],
            'wearing_items': get_items(_args, character['id'], 'wearing'),
            'won': True,
            'leveled_up': level_up,
            'level': character['level']
        }

        # Update character with the new values
        _args['mysql'].execute(
            """UPDATE `characters` SET `experience` = %s, `currency_gigas` = %s, `level` = %s WHERE `id` = %s""",
            [
                character['experience'],
                character['currency_gigas'],
                character['level'],
                slot['client']['character']['id']
            ])

    # After doing updates to the character object, we should close the mysql connection and return the results
    mysql_connection.close()
    return information


'''
This method will show the game statistics and the result of the post game transaction which is also
invoked in this method
'''
def game_stats(_args, room, status):

    # To give players the chance to obtain items such as drops, we will be waiting six seconds.
    time.sleep(6)

    # Perform post game transaction and obtain its results
    information = post_game_transaction(_args, room, status)

    # Construct room-wide information
    room_results = PacketWrite()

    # 8 bytes that tell which player won
    for i in range(8):
        room_results.AppendInteger(0 if str(i + 1) not in information else (1 if information[str(i + 1)]['won'] else 0))

    # 8 bytes that will tell which player leveled up
    for i in range(8):
        room_results.AppendInteger(0 if str(i + 1) not in information else (1 if information[str(i + 1)]['leveled_up'] else 0))

    # another 8 bytes which contain the new levels of said players
    for i in range(8):
        room_results.AppendInteger(0 if str(i + 1) not in information else information[str(i + 1)]['level'], 1, 'little')

    # new experience points for all players
    for i in range(8):
        room_results.AppendInteger(0 if str(i + 1) not in information else information[str(i + 1)]['addition_experience'], 2, 'little')

    # new health amount for all players
    for _ in range(8):
        room_results.AppendInteger(3001, 2, 'little')

    # Attack points
    for _ in range(8):
        room_results.AppendInteger(4, 2, 'little')

    # unknown
    for _ in range(4):
        room_results.AppendInteger(0, 4, 'little')

    # Player kills
    for _ in range(8):
        room_results.AppendInteger(23, 2, 'little')

    # Monster kills
    for _ in range(8):
        room_results.AppendInteger(69, 2, 'little')

    # MVPs shown
    room_results.AppendInteger(0, 2, 'little')
    room_results.AppendInteger(0, 2, 'little')

    # Cash item experience
    for _ in range(8):
        room_results.AppendInteger(0, 2, 'little')

    # Party experience
    for _ in range(8):
        room_results.AppendInteger(0, 2, 'little')

    # Player ranking and ranking experience
    for _ in range(8):
        # Ranking
        room_results.AppendInteger(2, 4, 'little')
        room_results.AppendBytes(bytearray([0x00]))

        # Ranking experience
        room_results.AppendInteger(5, 4, 'little')


    for key, slot in room['slots'].items():

        # Retrieve information for this specific player
        result_information = information[key]

        # Create game result packet
        packet = PacketWrite()
        packet.AddHeader(bytearray([0x1F, 0x2F]))
        packet.AppendBytes(bytearray([0x01, 0x00, 0x00, 0x00]))

        # New gold amount
        packet.AppendInteger(result_information['gold'], 4, 'little')

        # New level
        packet.AppendInteger(70, 2, 'little')

        # New experience
        packet.AppendInteger(result_information['experience'], 4, 'little')

        # New oil amount
        packet.AppendInteger(0, 4, 'little')
        packet.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00]))

        # Remaining time for wearing items
        for idx in [17, 18, 11, 12, 13, 14, 15, 16, 3, 4, 5, 6, 7, 8, 9, 10]:
            packet.AppendInteger(result_information['wearing_items']['items'][idx]['duration'], 4, 'little')

        # New character statistics
        packet.AppendInteger(room['slots'][key]['client']['character']['att_min']
                             + result_information['wearing_items']['specifications']['effect_att_min'], 2, 'little')
        packet.AppendInteger(room['slots'][key]['client']['character']['att_max']
                             + result_information['wearing_items']['specifications']['effect_att_max'], 2, 'little')
        packet.AppendInteger(room['slots'][key]['client']['character']['att_trans_min']
                             + result_information['wearing_items']['specifications']['effect_att_trans_min'], 2, 'little')
        packet.AppendInteger(room['slots'][key]['client']['character']['att_trans_max']
                             + result_information['wearing_items']['specifications']['effect_att_trans_max'], 2, 'little')

        # Finally, append room-wide information and send to the client's socket
        packet.AppendBytes(room_results.data)
        room['slots'][key]['client']['socket'].send(packet.packet)

    # We must now send the packet to go back to room after 6 seconds
    time.sleep(6)

    # Reset room status and broadcast room status to lobby
    reset(room)
    room['status'] = 0
    get_list(_args, mode=0 if room['game_type'] in [0, 1] else room['game_type'] - 1,
             page=get_list_page_by_room_id(room['id'], room['game_type']), local=False)

    game_exit = PacketWrite()
    game_exit.AddHeader(bytearray([0x2A, 0x2F]))
    game_exit.AppendBytes(bytearray([0x00]))
    _args['connection_handler'].SendRoomAll(room['id'], game_exit.packet)

'''
This method is responsible for waiting for the time to be over in sessions.
It uses polling due to having no ability to mutate the thread's state once it has been started.
'''
def countdown_timer(_args, room):

    # Always wait for the game count down to conclude. That's when the timer starts on the client.
    time.sleep(2)

    # Wait a predefined amount of time and check whether the game ended every second
    # If the game ended, stop polling. If everyone left the room, also stop.
    for _ in range(int(PLANET_MAP_TABLE[room['level']][1] * 60)):
        if len(room['slots']) == 0 or room['game_over']: break
        time.sleep(1)

    # If polling stopped while the game is not over, the game has ran out of time.
    # Also check if there are actually any players in the room
    if len(room['slots']) > 0 and not room['game_over']:
        game_end(_args=_args, room=room, status=2)