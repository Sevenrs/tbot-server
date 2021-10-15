#!/usr/bin/env python3
__author__      = 'Icseon'
__copyright__   = 'Copyright (C) 2021 Icseon'
__version__     = '1.0'

from Packet.Write import Write as PacketWrite
from GameServer.Controllers.data.drops import *
from GameServer.Controllers.data.exp import *
from GameServer.Controllers.data.planet import PLANET_MAP_TABLE, PLANET_BOXES, PLANET_BOX_MOBS, PLANET_DROPS,\
    PLANET_ASSISTS
from GameServer.Controllers.data.military import MILITARY_BASE
from GameServer.Controllers.data.client import CLIENT_FILE_HASHES
from GameServer.Controllers.data.game import *
from GameServer.Controllers.Character import get_items, add_item, get_available_inventory_slot, remove_expired_items
from GameServer.Controllers import Lobby, Room, Guild
import MySQL.Interface as MySQL
import random, time, datetime, _thread

"""
This controller is responsible for handling all game related actions
"""

'''
This method will tell the room that the client has finished loading the map
If all clients have finished loading, the game will be started.
'''
def load_finish_rpc(**_args):

    # Get room and check if we are in one
    room = Room.get_room(_args)
    if not room:
        return

    # Get slot
    slot = Room.get_slot(_args, room)

    # Check if file validation passed. If not, disconnect client now.
    if not room['slots'][str(slot)]['file_validation_passed']:
        return _args['connection_handler'].UpdatePlayerStatus(_args['client'], 2)

    # Get slot and update loading status
    room['slots'][str(slot)]['loaded'] = True

    # Check if the other slots have loaded
    for _slot in room['slots']:
        if not room['slots'][_slot]['loaded']:
            return

    # If all slots have loaded the level, call load_finish and let the clients play the game
    load_finish(_args, room)

'''
This method will be called once all players have finished loading
'''
def load_finish(_args, room):

    # If the game has already loaded, don't do anything
    if room['game_loaded']:
        return

    # Mark the room's game as loaded
    room['game_loaded'] = True

    # If all clients are ready to play, send the ready packet
    ready = PacketWrite()
    ready.AddHeader(bytearray([0x24, 0x2F]))
    ready.AppendBytes(bytearray([0x00]))
    _args['connection_handler'].SendRoomAll(room['id'], ready.packet)

    # Start new countdown timer thread, but only for Planet and DeathMatch modes
    if room['game_type'] in [MODE_PLANET, MODE_DEATHMATCH]:
        _thread.start_new_thread(countdown_timer, (_args, room,))

    # Start new incremental canister thread, but only for Battle and Team Battle mode
    if room['game_type'] in [MODE_BATTLE, MODE_TEAM_BATTLE]:
        _thread.start_new_thread(incremental_canister_drops, (_args, room,))

    # If the game is deathmatch, send a story message
    if room['game_type'] == MODE_DEATHMATCH:
        message = Lobby.ChatMessage(target=None,
                                    message='DeathMatch! The player with the most kills wins!',
                                    color=3,
                                    return_packet=True)
        _args['connection_handler'].SendRoomAll(room['id'], message)

'''
This method will handle monster deaths and broadcasts an acknowledgement to the room
of the monster being killed.
'''
def monster_kill(**_args):

    # If the client is not in a room or is not its master, drop the packet
    room = Room.get_room(_args)
    if not room:
        return

    # Read monster ID from the packet
    monster_id  = _args['packet'].GetByte(0)
    who         = _args['packet'].GetByte(4)
    pushed      = _args['packet'].GetByte(6)

    # Initialize assistant_multiplication variable that is used to increase drop chances
    # when planet mode is being played and an assistant is being killed.
    assistant_multiplication = 1.0

    # Construct base canister drop table and drop chances.
    drops = [
        (CANISTER_HEALTH,   0.02),
        (CANISTER_STUN,     0.01),
        (CANISTER_TRANS_UP, 0.01),
        (CANISTER_AMMO,     0.01),
    ]

    # If we are playing planet mode, add additional drops such as rebirth and bombs.
    # Additionally, we'll be adding box drops in case that possibility exists.
    if room['game_type'] == MODE_PLANET:
        drops+= [
            (CANISTER_REBIRTH,  0.02),
            (CANISTER_BOMB,     0.02),
            (CHEST_GOLD,        0.007)
        ]

        # If the monster is a mob from which to drop boxes from, append the boxes array
        if room['level'] in PLANET_BOXES and monster_id in PLANET_BOX_MOBS[room['level']]:
            drops += PLANET_BOXES[room['level']]

        # If the mob is an assistant, multiply the canister chance by a factor of 50
        if room['level'] in PLANET_ASSISTS and monster_id in PLANET_ASSISTS[room['level']]:
            assistant_multiplication = 50.0

    # If we are playing military mode, add gold to the drop table with no chance to drop.
    # We will only be making it a possible drop when a MILITARY_BASE has been killed.
    elif room['game_type'] == MODE_MILITARY:
        drops+= [
            (CHEST_GOLD, 0.00)
        ]

    # Randomly shuffle the drops to randomize drop order
    random.shuffle(drops)

    # Calculate whether or not we should drop an item based on chance
    # But only if the monster ID is not in the array of killed mobs and if the game is still going
    # Lastly, we shouldn't drop anything if the monster has been pushed
    monster_drops = []
    if monster_id not in room['killed_mobs'] and not room['game_over'] and pushed == 0:
        for drop, chance in drops:

            ''' If the monster ID is equal to the boss, we'll have to change the drop chances, but only if we are in planet mode '''
            if room['level'] in PLANET_BOXES and monster_id == PLANET_BOX_MOBS[room['level']][len(PLANET_BOX_MOBS[room['level']]) - 1] \
                    and room['game_type'] == MODE_PLANET:

                # If the drop is not a canister, increase chance by 5x
                if drop >= BOX_ARMS:
                    chance = chance * 5
                else:

                    # Otherwise, the chance should be 0. We do not want to drop canisters.
                    chance = 0.00

                    # Except if the drop is a rebirth then the chance should always be 100%
                    if drop == CANISTER_REBIRTH:
                        chance = 1.00

            # Ensure that a military base always drops gold
            elif room['game_type'] == MODE_MILITARY and monster_id in MILITARY_BASE and drop == CHEST_GOLD:
                chance = 1.00

            # If applicable, apply the assistant multiplication except if the drop type is greater or equal to CHEST_GOLD(18)
            if random.random() < (chance * (assistant_multiplication if drop < BOX_ARMS else 1.0)) and room['drop_index'] < 256:
                monster_drops.append(bytes([room['drop_index'], drop, 0, 0, 0]))
                room['drops'][room['drop_index']] = {'type': drop, 'used': False}
                room['drop_index'] += 1
    drop_bytes = b''.join(monster_drops)

    # Randomly generate drop direction
    direction = random.randrange(0, 6)

    # Create monster death response
    death = PacketWrite()
    death.AddHeader(bytes=bytearray([0x25, 0x2F]))
    death.AppendBytes(bytes=bytearray([0x01, 0x00]))
    death.AppendInteger(integer=monster_id, length=2, byteorder='little')
    death.AppendInteger(direction, 2, 'little')
    death.AppendInteger(len(monster_drops), length=2, byteorder='little')
    death.AppendBytes(drop_bytes)

    # Broadcast the response to all sockets in the room
    _args['connection_handler'].SendRoomAll(room['id'], death.packet)

    # Count up the amount of mobs the slot has killed, but only if the slot is in the room and the mob isn't already registered as dead
    if str(who +1) in room['slots'] and who != 65535 \
            and monster_id not in room['killed_mobs'] and room['game_over'] == False:
        room['slots'][str(who + 1)]['monster_kills'] += 1

    # Add the monster to the killed mob array, but only if we're in planet or military mode
    if room['game_type'] == MODE_PLANET or (room['game_type'] == MODE_MILITARY and monster_id != MILITARY_BASE):
        room['killed_mobs'].append(monster_id)

'''
This method will handle picking up items which were dropped from monsters
'''
def use_item(**_args):

    # If the client is not in a room, drop the packet
    room = Room.get_room(_args)
    if not room:
        return

    # Read item index and type from packet
    item_index  = _args['packet'].GetByte(2)
    item_type   = _args['packet'].GetByte(3)

    # Check if the drop is valid. If it is not, change the item type to 0 so nothing happens.
    if item_index not in room['drops'] or room['drops'][item_index]['used'] == True \
             or room['drops'][item_index]['type'] != item_type:
        item_type = 0

    # Mark the drop as used before further processing of the packet
    # but only if the item index is actually registered
    if item_index in room['drops']:
        room['drops'][item_index]['used'] = True

    # Broadcast the use canister packet to the room
    use_canister = PacketWrite()
    use_canister.AddHeader(bytearray([0x23, 0x2F]))
    use_canister.AppendInteger(Room.get_slot(_args, room) - 1, 2, 'little')
    use_canister.AppendInteger(item_index, 1, 'little')
    use_canister.AppendInteger(item_type, 4, 'little')
    _args['connection_handler'].SendRoomAll(room['id'], use_canister.packet)

    # If the item is a rebirth pack, make all players alive
    if item_type == CANISTER_REBIRTH:
        for key, slot in room['slots'].items():
            slot['dead'] = False

    # If the item is OIL, process oil pickup
    if item_type in [OIL_YELLOW, OIL_ORANGE, OIL_BLUE, OIL_PINK]:

        # Container for the amount of oil a player receives per type
        OIL_AWARDS = {
            OIL_YELLOW: 5,
            OIL_ORANGE: 15,
            OIL_BLUE: 20,
            OIL_PINK: 30
        }

        # Retrieve award amount and update the character
        award = OIL_AWARDS[item_type]
        _args['client']['character']['currency_botstract'] += award
        _args['mysql'].execute("""UPDATE `characters` SET `currency_botstract` = (`currency_botstract` + %s) WHERE `id` = %s""", [
            award,
            _args['client']['character']['id']
        ])

    # If the item type is equal or exceeds 18, process a box pickup
    if item_type >= 18:

        # Find available slot
        inventory = get_items(_args, _args['client']['character']['id'], 'inventory')
        available_slot = get_available_inventory_slot(inventory)

        # Construct pickup packet
        pickup = PacketWrite()
        pickup.AddHeader(bytes=[0x2C, 0x2F])

        # Send inventory full packet if we do not have an available slot
        if available_slot is None:
            pickup.AppendBytes(bytes=[0x00, 0x44])
            return _args['socket'].send(pickup.packet)

        # If the item is gold, calculate what gold bar to award
        if item_type == CHEST_GOLD:
            item_id = [
                6000001,
                6000002,
                6000003
            ][random.randint(0, 2)]
        else:

            # If we do not have this item type in the drop table, do nothing
            if item_type not in PLANET_DROPS[room['level']]:
                return

            # Retrieve random drop and calculate the chance
            drops = PLANET_DROPS[room['level']][item_type]

            # Calculate the chance
            sc = random.random()
            last_chance = 0.0

            # Based on the randomized chance, retrieve the item we are going to award
            item_id = 0
            for iid, chance in drops:
                if sc <= (chance + last_chance):
                    item_id = iid
                    break
                else:

                    # No match? Try again with a higher chance
                    last_chance += chance

        # Mutate the item ID to be of our bot type if the item type is either a HEAD, BODY or ARM
        if item_type in [BOX_HEAD, BOX_BODY, BOX_ARMS]:

            # Create a list of the item ID and append the character type to it
            new_item_id = list(str(item_id))
            new_item_id[1] = str(_args['client']['character']['type'])

            # Convert the item ID back to an integer
            item_id = int("".join(new_item_id))

        # Find item in the database
        _args['mysql'].execute(
            '''SELECT `id`, `item_id`, `buyable`, `gold_price`, `cash_price`, `part_type`, `duration` FROM `game_items` WHERE `item_id` = %s''',
            [item_id])
        item = _args['mysql'].fetchone()

        # If the item hasn't been found, return an error
        if item is None:
            pickup.AppendBytes(bytes=[0x00, 0x00])
            return _args['socket'].send(pickup.packet)

        # Add item to inventory of the user
        add_item(_args, item, available_slot)

        # Send pickup packet to the player
        pickup.AppendBytes(bytes=[0x01, 0x00])
        pickup.AppendInteger(item_id, 4, 'little')
        pickup.AppendInteger(0, 4, 'little')
        pickup.AppendInteger(Room.get_slot(_args, room) - 1, 2, 'little')
        _args['socket'].send(pickup.packet)

'''
This method allows players to use their field packs
'''
def use_field_pack(**_args):

    # Get room and check if we are in a room
    room = Room.get_room(_args)
    if not room:
        return

    # Get our slot number
    room_slot = Room.get_slot(_args, room)

    # Get wearing field pack
    wearing = get_items(_args, _args['client']['character']['id'], 'wearing')
    for idx in wearing['items']:
        if wearing['items'][idx]['type'] == 'field_pack':

            # Check if the item ID is a field pack. If not, drop the packet
            field_packs = [
                4030100,
                4030101,
                4030102,
                4030103,
                4030200,
                4030201,
                4030202,
                4030203,
                4030204,
                4030301,
                4030302,
                4030303,
                4030401
            ]

            if wearing['items'][idx]['id'] not in field_packs:
                return

            # Check if we are dealing with a rebirth pack
            if wearing['items'][idx]['id'] in [4030100, 4030101, 4030102, 4030103]:

                # Mark all players as alive
                for key, slot in room['slots'].items():
                    slot['dead'] = False

                # Construct rebirth packet and broadcast it to the room
                rebirth = PacketWrite()
                rebirth.AddHeader([0x3A, 0x27])
                rebirth.AppendInteger(room_slot - 1, 1, 'little')
                rebirth.AppendBytes([0x00, 0x01, 0x00])
                _args['connection_handler'].SendRoomAll(room['id'], rebirth.packet)

                # Construct an acknowledge message that indicates that the rebirth pack was used
                message = Lobby.ChatMessage(target=None,
                                            message='{0} has used their revival pack'.format(_args['client']['character']['name']),
                                            color=2,
                                            return_packet=True)
                _args['connection_handler'].SendRoomAll(room['id'], message)

            # Subtract one from the duration. Ensure that the number never becomes lower than 0.
            wearing['items'][idx]['duration'] = wearing['items'][idx]['duration'] - 1
            if wearing['items'][idx]['duration'] < 0:
                wearing['items'][idx]['duration'] = 0

            # Construct and send health packet
            update_pack_times = PacketWrite()
            update_pack_times.AddHeader([0x1D, 0x2F])
            update_pack_times.AppendBytes([0x01, 0x00])

            # Append item duration to the packet
            for i in range(11, 17):
                item = wearing['items'][list(wearing['items'].keys())[i]]
                update_pack_times.AppendInteger(item['id'], 4, 'little')
                update_pack_times.AppendInteger(item['duration'], 4, 'little')
                update_pack_times.AppendInteger(item['duration_type'], 1, 'little')

            _args['socket'].send(update_pack_times.packet)

            # Subtract one from the remaining_times column for the item
            _args['mysql'].execute("""UPDATE `character_items` SET `remaining_times` = (`remaining_times` - 1) 
                WHERE `id` = %s AND `remaining_times` > 0""", [wearing['items'][idx]['character_item_id']])
            break


'''
This method will handle player deaths.
'''
def player_death_rpc(**_args):

    # If the client is not in a room, drop the packet
    room = Room.get_room(_args)
    if not room:
        return

    # If the game mode is not equal to 2, drop the packet and send a message to the client
    if room['game_type'] != MODE_PLANET:
        Lobby.ChatMessage(_args['client'], 'You can only use the suicide button in planet mode', 2)
        return

    # Kill player
    player_death(_args, room)

'''
This method will kill a player
It works by reading the slot number and broadcasting that the player is dead to all room sockets
'''
def player_death(_args, room):

    # Get slot number from the room
    room_slot = Room.get_slot(_args, room)

    # Do not kill the player if the player is already dead
    if room['slots'][str(room_slot)]['dead']:
        return False

    # Update room object and classify the player as dead
    room['slots'][str(room_slot)]['dead'] = True

    # Let the room know about the death of this player
    death = PacketWrite()
    death.AddHeader(bytearray([0x54, 0x2F]))
    death.AppendBytes(bytes=bytearray([0x01, 0x00]))
    death.AppendInteger(integer=(int(room_slot) - 1), length=2, byteorder='little')
    _args['connection_handler'].SendRoomAll(room['id'], death.packet)

'''
This method will update the score with the score sent from the client
'''
def set_score(**_args):

    # Check if we are in a room and get our room slot
    room = Room.get_room(_args)
    if not room:
        return

    room_slot = Room.get_slot(_args, room)

    # Retrieve score from the packet and set the score
    score = int(_args['packet'].ReadInteger(0, 2, 'big'))
    room['slots'][str(room_slot)]['points'] = score

'''
This method will receive the file hashes of every important file of the game and compare its hashes against what
we have. If any hash is not matching, we disconnect the client.
'''
def file_validation(**_args):

    # Check if we are in a room and obtain our slot
    room = Room.get_room(_args)
    if not room:
        return

    room_slot = Room.get_slot(_args, room)

    for hash in CLIENT_FILE_HASHES:

        # Read hash received from the client
        client_hash = _args['packet'].ReadString()

        # Compare hash. If they don't match, we disconnect the client.
        if client_hash != hash:
            print("Invalid file hash. Expected: {0}, Got: {1}".format(hash, client_hash))
            return _args['connection_handler'].UpdatePlayerStatus(_args['client'], 2)

    # If we have passed validation, update our validation state to True (passed)
    room['slots'][str(room_slot)]['file_validation_passed'] = True

'''
This method will link clients through relay when the clients indicate that they are not connected with each-other.
It works by adding an array of clients to a container and looping through that array to figure out who to connect to who.
'''
def network_state(**_args):

    # Get the room we are currently in and check if we are in a room at all.
    room = Room.get_room(_args)
    if not room:
        return

    # Read request ID from the packet. The request ID is the aforementioned container's unique identifier.
    request_id = int(_args['packet'].ReadInteger(7, 2, 'little'))

    # Create the container of unlinked clients if such container was not previously created.
    # These containers will be cleaned up once the room is reset
    if request_id not in room['network_state_requests']:
        room['network_state_requests'][request_id] = []

    # Insert our own client in the container.
    if _args['client'] not in room['network_state_requests'][request_id]:
        room['network_state_requests'][request_id].append(_args['client'])

        # Loop through every client in the container and link them.
        for client in room['network_state_requests'][request_id]:

            ''' Find the room instance for the client we are processing.
            # Even though we have obtained the room before, we need to do this again because the state could
            # have changed since the creation of the container. '''
            client_room = Room.get_room({'client': client, 'server': _args['server']})

            # Check if the current client is actually in a room to begin with
            # If not, skip the iteration and remove the client from the container.
            if not client_room:
                room['network_state_requests'][request_id].remove(client)
                continue

            # Retrieve the slot number and slot instance for the client
            slot_number = Room.get_slot({'client': client}, client_room)
            slot = room['slots'][str(slot_number)]

            try:

                # Retrieve all clients inside of the request container
                for remote_client in room['network_state_requests'][request_id]:

                    '''
                        Make sure the following cases are true:
                        1.  The client is actually remote and not the client we are processing.
                        2.  The remote client is connected to the relay server
                        3.  The remote client is in the same room of the client we are processing

                        If any of these cases are false, skip the iteration.
                    '''
                    if remote_client is client \
                            or 'relay_client' not in remote_client \
                            or Room.get_room({'client': remote_client, 'server': _args['server']}) is not client_room:
                        continue

                    # Add the remote client's relay ID to the relay container of the client we are processing.
                    if remote_client['relay_client']['id'] not in slot['relay_ids']:
                        slot['relay_ids'].append(remote_client['relay_client']['id'])

            except Exception as e:
                print('Failed to link connections because {0}'.format(str(e)))

'''
This method will handle the game end RPC. This acts as a caller for game_end through a packet instead of being
called manually in the game code.
'''
def game_end_rpc(**_args):

    # If the client is not in a room, drop the packet
    room = Room.get_room(_args)
    if not room:
        return

    # Get our slot number from the room
    room_slot = Room.get_slot(_args, room)

    # Determine the status of the end result
    status = 0 if _args['packet'].id == '3b2b' else 1

    # Death handler for Battle, team Battle, DeathMatch and Military
    if room['game_type'] != MODE_PLANET:

        # Update death status (unless we're playing DeathMatch or Military)
        if room['game_type'] not in [MODE_DEATHMATCH, MODE_MILITARY]:
            slot = room['slots'][str(room_slot)]
            slot['dead'] = True

        # Increment death kill, but only if the game hasn't ended
        if not room['game_over']:
            room['slots'][str(room_slot)]['deaths'] += 1

        # Retrieve who killed the player
        who = int(_args['packet'].ReadInteger(5, 2, 'little'))

        # If the player is in the room and the game hasn't ended, increment their kill count by one
        if str(who + 1) in room['slots'] and who != 65535 and not room['game_over']:
            room['slots'][str(who + 1)]['player_kills'] += 1

        # Tell the room about the death of the player for the Battle modes and Military mode
        if room['game_type'] in [MODE_BATTLE, MODE_TEAM_BATTLE, MODE_MILITARY]:

            # Default drop result and drop bytes used for player drops.
            drop_result, drop_bytes = [], b''

            # We only want to have drops for the Battle modes. Military shouldn't drop anything
            if room['game_type'] != MODE_MILITARY:

                # Array with possible drops from players
                drops = [
                    OIL_BLUE,
                    OIL_PINK,
                    OIL_ORANGE,
                    OIL_YELLOW
                ]

                # Since we want the possibility for drops to occur more than once, we'll need to randomly generate
                # the amount we want
                _drops = []
                for drop in drops:
                    for _ in range(random.randrange(0, 3)):
                        _drops.append(drop)

                # If the chance exceeds the randomized value, add a gold drop
                if random.random() < 0.35:
                    _drops.append(CHEST_GOLD)

                # Randomly shuffle the drop order
                random.shuffle(_drops)

                # Add drops to the drop result list
                for idx, drop in enumerate(_drops):
                    if room['drop_index'] < 256:

                        # Create and append drop data to the result and modify room state to register the drop
                        drop_result.append(bytes([room['drop_index'], drop, 0, 0, 0]))
                        room['drops'][room['drop_index']] = {'type': drop, 'used': False}
                        room['drop_index'] += 1

                # Create drop bytes for the drop packet
                drop_bytes = b''.join(drop_result)

            # Randomly generate drop direction
            direction = random.randrange(0, 6)

            # Construct player death response to include aforementioned drops
            death = PacketWrite()
            death.AddHeader([0x22, 0x2F])
            death.AppendBytes(bytes=bytearray([0x01, 0x00]))
            death.AppendInteger(integer=(int(room_slot) - 1), length=2, byteorder='little')
            death.AppendInteger(direction, 2, 'little')
            death.AppendInteger(len(drop_result), length=2, byteorder='little')
            death.AppendBytes(drop_bytes)
            _args['connection_handler'].SendRoomAll(room['id'], death.packet)

        # Kill the player and update the score board if we are playing DeathMatch
        elif room['game_type'] == MODE_DEATHMATCH and (str(who + 1) in room['slots'] or who == 65535):

            # Update the score board
            update = PacketWrite()
            update.AddHeader([0x5B, 0x2F])
            update.AppendBytes(bytes=bytearray([0x01, 0x00]))
            update.AppendInteger(integer=(int(room_slot) - 1), length=2, byteorder='little')    # Victim
            update.AppendInteger(integer=who, length=2, byteorder='little')                     # Killer
            _args['connection_handler'].SendRoomAll(room['id'], update.packet)

        # Death check for Battle
        if room['game_type'] == MODE_BATTLE:

            # Check if there is at least one player still alive. The player that is alive, wins the game.
            alive = []
            for slot in room['slots']:
                if not room['slots'][slot]['dead']:
                    alive.append(slot)

            # Check if the length of the alive array is equal to or less than 1. If so, the game has ended.
            # The player in the alive array (if any) should be the winner.
            if len(alive) < 2:

                # It is possible for this length to be equal to 0. If so, nobody has won the game.
                # If the length is equal to 1, the last alive player will be the winner
                if len(alive) == 1:
                    room['slots'][alive[0]]['won'] = True

                # End the game
                game_end(_args=_args, room=room)

        # Death check for team Battle
        elif room['game_type'] == MODE_TEAM_BATTLE:

            # Object containing the amount of alive players per team
            teams = {
                TEAM_RED:   {'alive': 0},
                TEAM_BLUE:  {'alive': 0}
            }

            # Retrieve amount of alive players per team
            for slot in room['slots']:
                if not room['slots'][slot]['dead']:
                    teams[room['slots'][slot]['team']]['alive'] +=1

            # Check if any team has no alive players, make opposite team win
            for team in teams:
                if teams[team]['alive'] == 0:

                    # Retrieve the opposite team
                    opposite_team = TEAM_RED if team == TEAM_BLUE else TEAM_BLUE

                    # Make all players in the opposite team win
                    for slot in room['slots']:
                        if room['slots'][slot]['team'] == opposite_team:
                            room['slots'][slot]['won'] = True

                    # End the game
                    game_end(_args=_args, room=room)
                    break

        # Death check for Military
        elif room['game_type'] == MODE_MILITARY:

            # If at least one player hasn't died 5 (or more) times, then there's no need to do anything
            for slot in room['slots']:
                if room['slots'][slot]['deaths'] < 5:
                    return

            # If all players are really dead, end the game. There's no way to finish the game without at least one person.
            game_end(_args=_args, room=room, status=0)


    # Planet Mode
    elif room['game_type'] == MODE_PLANET:

        # Check if all players are actually dead. If not, drop the packet
        if status == 0:
            for slot in room['slots']:
                if not room['slots'][slot]['dead']:
                    return

        # If the room level is not in the map table we must change the status to 0 (lost)
        if room['level'] not in room['maps']:
            status = 0

        # End the game
        game_end(_args=_args, room=room, status=status)

'''
This method will listen to the client to tell which team has won the match.
Everyone in the winning team will be marked as a winner and the game will end.
'''
def military_win(**_args):

    # If the client is not in a room, drop the packet
    room = Room.get_room(_args)
    if not room:
        return

    # Verify if the room is a Military room. If not, drop the packet.
    if room['game_type'] is not MODE_MILITARY:
        return

    # Read winning team
    winning_team = int(_args['packet'].ReadInteger(3, 2, 'little'))

    # If the winning team from the client is not valid, drop the packet
    if winning_team not in [TEAM_RED, TEAM_BLUE]:
        return

    # Ensure that everyone in the winning team is marked as a winner
    for slot in room['slots']:
        if room['slots'][slot]['team'] == winning_team:
            room['slots'][slot]['won'] = True

    # End the game
    game_end(_args=_args, room=room)

'''
This method will send the correct packet to indicate what the game end result is to the room or specified client.
After this, it will start a new thread that will run the post-game transaction and show the game stats to the clients.
'''
def game_end(_args, room, status=None):

    # If the game is already over, there is not anything to do.
    if room['game_over']:
        return

    # The game is over. This is to avoid multiple calls to this method and to stop polling threads.
    room['game_over'] = True

    # If we already know the status for all players beforehand, we can send the packet based on that
    if status is not None:

        # Create game result packet and send it to all the room clients
        result = PacketWrite()
        result.AddHeader(bytes=bytearray([0x2A, 0x27]))
        result.AppendInteger(status, 2, 'little')
        _args['connection_handler'].SendRoomAll(room['id'], result.packet)

        # If the status is equal to 1, then everyone has won. Set the won status of every player in the room to True
        if status == 1:
            for slot in room['slots']:
                room['slots'][slot]['won'] = True

    # Otherwise we must loop through every player in the game to determine their status
    else:

        for slot in room['slots']:
            status = 1 if room['slots'][slot]['won'] else 0

            # Create result packet and send to this player
            result = PacketWrite()
            result.AddHeader([0x2A, 0x27])
            result.AppendInteger(status, 2, 'little')
            try:
                room['slots'][slot]['client']['socket'].send(result.packet)
            except Exception:
                pass

    # Start new thread for the game statistics
    _thread.start_new_thread(game_stats, (_args, room,))

'''
This method will update all characters in the room with their new results (if applicable)
Additionally, this method will return the results of the transaction in the form of a dictionary
'''
def post_game_transaction(_args, room):

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

        # Default experience addition and giga addition values
        addition_experience, addition_gigas, addition_rank_experience = 0, 0, 0

        ''' Calculate experience and giga gains for planet mode'''
        if room['game_type'] == MODE_PLANET:

            ''' Calculate the amount of experience to award to the player. If the player's level has a difference of at least 10,
                the experience is divided by four. Otherwise, the experience is not mutated. 
                
                If there is an experience modifier present, it will be applied on top of the base experience.
                Finally, if the player has lost the game, no experience will be awarded at all. '''
            addition_experience = int(PLANET_MAP_TABLE[room['level']][0][room['difficulty']] * room['experience_modifier'] \
                                  / (1.00 if abs(PLANET_MAP_TABLE[room['level']][2] - character['level']) < 10 else 4.00)) \
                                        if room['level'] in PLANET_MAP_TABLE.keys() and slot['won'] else 0

            ''' Calculate the amount of gigas to award to the player. If the level difference is too large, the amount is reduced.
                The base reward is equal to 1250 which a rate is applied on top of.'''
            mv      = (PLANET_MAP_TABLE[room['level']][2] + 1) * 2
            rate    = min(15.0, max(0.1, 1.0 + (float(mv - character['level']) / 10.0)))
            reward  = int(1250 * rate / (1.00 if abs(PLANET_MAP_TABLE[room['level']][2] - character['level']) < 10 else 4.00))
            addition_gigas = reward if slot['won'] else 0

        # If the game mode is DeathMatch, calculate the rank addition
        elif room['game_type'] == MODE_DEATHMATCH:
            addition_rank_experience = int(slot['player_kills'] * 2.5)

        # If the game mode is Battle, team Battle or Military, calculate the experience and currency gains
        elif room['game_type'] in [MODE_BATTLE, MODE_TEAM_BATTLE, MODE_MILITARY]:

            ''' Calculate multiplier for the experience (and also gigas, eventually) based on the room's start time.
                The maximum multiplayer should be 60 (1 minute)'''
            experience_multiplier = max(1, min((datetime.datetime.now() - room['start_time']).total_seconds(), 60))

            ''' Calculate the amount of experience to award based on both the experience multiplier and the amount 
                of players that this player has killed. Eventually, base gigas off of that as well.
                
                We'll also want to randomize the experience multiplier with another multiplier (uniform)
                to randomize the outcome as well. '''
            addition_experience = int(slot['player_kills'] * (experience_multiplier * random.uniform(1.0, 1.3)))
            addition_gigas      = addition_experience * random.randrange(13, 16)

            ''' Calculate additional experience for Military mode'''
            if room['game_type'] == MODE_MILITARY:
                addition_experience += int(slot['monster_kills'] * (experience_multiplier * random.uniform(1.0, 1.3)))

        # Check if we have leveled up
        level_up = character['experience'] + addition_experience >= EXP_TABLE[character['level'] + 1]
        if level_up:

            # Update our level and experience
            character['level'] += 1
            character['experience'] = 0
        else:

            # Update only our experience
            character['experience'] = character['experience'] + addition_experience

        # Increase the rank experience and then check if we can rank up
        character['rank_exp'] += addition_rank_experience

        # Find our next rank based on the amount of experience we have.
        # Do not change the rank if the rank is greater than 43 (max rank)
        new_rank = 0
        for rank in RANK_EXP_TABLE:
            if character['rank_exp'] >= RANK_EXP_TABLE[rank] and rank <= 43:
                new_rank = rank

        # Change our current rank to the new rank if it's greater than our current rank
        rank_up = new_rank > character['rank']
        if rank_up:
            character['rank'] = new_rank

        # Calculate new gigas currency
        character['currency_gigas'] = character['currency_gigas'] + addition_gigas

        # Decrease the amount of games left for the items the current character is wearing
        wearing = get_items(_args, character['id'], 'wearing')
        in_statement = ''

        # Construct IN statement
        for idx in wearing['items']:
            if wearing['items'][idx]['character_item_id'] is not None:
                in_statement+= '{}, '.format(wearing['items'][idx]['character_item_id'])

        # Remove one remaining game from the total amount of remaining games, if applicable.
        if len(in_statement) > 0:
            _args['mysql'].execute("""UPDATE `character_items` SET `remaining_games` = (`remaining_games` - 1) WHERE `id`
                                   IN ({0}) AND `remaining_games` IS NOT NULL""".format(in_statement[:-2]))

        # Remove expired items from our character and the game itself
        remove_expired_items(_args, character['id'])

        information[key] = {
            'addition_experience': addition_experience,
            'addition_rank_experience': addition_rank_experience,
            'addition_gigas': addition_gigas,
            'experience': character['experience'],
            'gold': character['currency_gigas'],
            'oil': character['currency_botstract'],
            'wearing_items': get_items(_args, character['id'], 'wearing'),
            'won': slot['won'],
            'leveled_up': level_up,
            'level': character['level'],
            'points': slot['points']
        }

        # Calculate and award guild points if character is in a guild
        if Guild.FetchGuild(_args, character['id']) is not None:

            # Calculate guild points based on the amount of experience and rank experience
            guild_points = int((addition_experience * .70) + (addition_rank_experience * 1.25))

            # Update guild points for this member
            _args['mysql'].execute('''UPDATE `guild_members` SET `points` = (`points` + %s) WHERE `character_id` = %s''', [
                guild_points,
                character['id']
            ])

        # In case the room game type is either Battle or Team Battle, we'll have to display experience as rank experience
        # This is because the client uses the rank experience result screen for Battle too, instead of the traditional one.
        if room['game_type'] in [MODE_BATTLE, MODE_TEAM_BATTLE]:
            information[key]['addition_rank_experience'] = information[key]['addition_experience']

        # Update character with the new values
        _args['mysql'].execute(
            """UPDATE `characters` SET
                                        `experience` = %s,
                                        `currency_gigas` = %s,
                                        `level` = %s,
                                        `rank` = %s,
                                        `rank_exp` = %s
                                    WHERE `id` = %s""",
            [
                character['experience'],
                character['currency_gigas'],
                character['level'],
                character['rank'],
                character['rank_exp'],
                slot['client']['character']['id']
            ])

    # After doing updates to the character object, we should close the mysql connection and return the results
    mysql_connection.close()
    return information


'''
This method will show the game statistics and the result of the post game transaction which is also
invoked in this method
'''
def game_stats(_args, room):

    # To give players the chance to obtain items such as drops, we will be waiting a few seconds.
    time.sleep(6.5)

    # If the room ID no longer represents our room, stop.
    if str(room['id']) not in _args['server'].rooms or room is not _args['server'].rooms[str(room['id'])]:
        return

    # Perform post game transaction and obtain its results
    information = post_game_transaction(_args, room)

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
    for i in range(8):
        room_results.AppendInteger(0 if str(i + 1) not in information else room['slots'][str(i + 1)]['client']['character']['health']
                             + information[str(i + 1)]['wearing_items']['specifications']['effect_health'], 2, 'little')

    # Attack points
    for i in range(8):
        room_results.AppendInteger(0 if str(i + 1) not in information else int(room['slots'][str(i + 1)]['points'] / 1.5), 2, 'little')

    # unknown
    for _ in range(8):
        room_results.AppendInteger(0, 2, 'little')

    # Player kills
    for _ in range(8):
        room_results.AppendInteger(0, 2, 'little')

    # Monster kills
    for i in range(8):
        room_results.AppendInteger(0 if str(i + 1) not in information else room['slots'][str(i + 1)]['monster_kills'], 2, 'little')

    # MVPs
    room_results.AppendInteger(1 if len(room['slots']) >= 2 else 0, 2, 'little')    # MVP
    room_results.AppendInteger(1 if len(room['slots']) >= 3 else 0, 2, 'little')    # Boss/Base killer number 1

    # Cash item experience
    for _ in range(8):
        room_results.AppendInteger(0, 2, 'little')

    # Party experience
    for _ in range(8):
        room_results.AppendInteger(0, 2, 'little')

    room_results.AppendBytes(bytearray([0x00, 0x00, 0x00, 0x00, 0x00])) # Unknown

    # Player ranking and ranking experience
    for i in range(0, 8):
        room_results.AppendInteger(0 if str(i + 1) not in information else room['slots'][str(i + 1)]['client']['character']['rank_exp'], 4, 'little')
        room_results.AppendInteger(0 if str(i + 1) not in information else room['slots'][str(i + 1)]['client']['character']['rank'], 4, 'little')

        # Rank points
        room_results.AppendInteger(0 if str(i + 1) not in information else information[str(i + 1)]['addition_rank_experience'], 4, 'little')

        # Kill points
        room_results.AppendInteger(0, 4, 'little')

        # Experience bonus
        room_results.AppendInteger(0, 4, 'little')

        # Unknown
        room_results.AppendInteger(0, 4, 'little')

        # Cash point
        room_results.AppendInteger(0, 4, 'little')

        # Rank experience points
        room_results.AppendInteger(0 if str(i + 1) not in information else information[str(i + 1)]['addition_rank_experience'], 4, 'little')

        # Kills
        room_results.AppendInteger(0 if str(i + 1) not in information else room['slots'][str(i + 1)]['player_kills'], 4, 'little')

        # Deaths
        room_results.AppendInteger(0 if str(i + 1) not in information else room['slots'][str(i + 1)]['deaths'], 4, 'little')

        # Attack points
        room_results.AppendInteger(0 if str(i + 1) not in information else room['slots'][str(i + 1)]['points'], 4, 'little')

        # Leveled up
        room_results.AppendBytes(bytearray([0x00]))


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
        packet.AppendInteger(result_information['level'], 2, 'little')

        # New experience
        packet.AppendInteger(result_information['experience'], 4, 'little')

        # New oil amount
        packet.AppendInteger(result_information['oil'], 4, 'little')
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
    time.sleep(6.5)

    # If the room ID no longer represents our room, stop.
    if str(room['id']) not in _args['server'].rooms or room is not _args['server'].rooms[str(room['id'])]:
        return

    # Reset room status and broadcast room status to lobby
    Room.reset(room)
    room['status'] = 0
    Room.get_list(_args, mode=0 if room['game_type'] in [MODE_BATTLE, MODE_TEAM_BATTLE] else room['game_type'] - 1,
             page=Room.get_list_page_by_room_id(room['id'], room['game_type']), local=False)

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

    # Retrieve the amount of minutes from the room setting
    minutes = 3 if room['time'] == 0 else 5

    # For planet gameplay, retrieve the amount of minutes from the map
    if room['game_type'] == MODE_PLANET:
        minutes = PLANET_MAP_TABLE[room['level']][1]

    # Wait a predefined amount of time and check whether the game ended every second
    # If the game ended, stop polling. If everyone left the room, also stop.
    for _ in range(int(minutes * 60)):
        if len(room['slots']) == 0 or room['game_over']: break
        time.sleep(1)

    # If polling stopped while the game is not over, the game has ran out of time.
    # Also check if there are actually any players in the room
    if len(room['slots']) > 0 and not room['game_over']:
        game_end(_args=_args, room=room, status=2 if room['game_type'] != MODE_DEATHMATCH else 3)

'''
This method is responsible for dropping canisters per set interval to give players canisters
in DeathMatch and Battle mode. This method uses long polling due to having no ability to mutate the thread's state
once it has been started.
'''
def incremental_canister_drops(_args, room):
    while True:

        # Wait a predefined amount of time and check if the game has ended every second
        for _ in range(30):
            if len(room['slots']) == 0 or room['game_over']:
                return
            time.sleep(1)

        # Valid drops with their respective chances
        possible_drops = [
            CANISTER_HEALTH,
            CANISTER_STUN,
            CANISTER_TRANS_UP,
            CANISTER_AMMO
        ]

        # Construct the drop result
        drops = []
        for drop in possible_drops:
            random_count = random.randrange(1, 3)
            for _ in range(random_count):
                drops.append(drop)

        # Do a shuffle to this drop result
        random.shuffle(drops)

        canisters = []
        for idx, drop in enumerate(drops):
            if room['drop_index'] < 256:

                # Construct drop data
                data = bytearray()
                data.extend(idx.to_bytes(2, 'little'))
                data.extend([room['drop_index'], drop])

                # Append drop data to the canisters
                canisters.append(data)
                room['drops'][room['drop_index']] = {'type': drop, 'used': False}
                room['drop_index'] += 1

        # Create drop bytes for the drop packet
        drop_bytes = b''.join(canisters)

        # Construct drop packet and send it to the room
        drop = PacketWrite()
        drop.AddHeader([0x2B, 0x27])
        drop.AppendInteger(len(canisters), length=2, byteorder='little')
        drop.AppendBytes(drop_bytes)
        _args['connection_handler'].SendRoomAll(room['id'], drop.packet)

'''
This thread will check clients' loading status in the background every second as a failsafe.
Once all clients have loaded, the game will be started.
'''
def load_finish_thread(_args, room):

    # Keep checking while the game hasn't loaded yet
    while not room['game_loaded'] and len(room['slots']) > 0:

        # Try every second
        time.sleep(1)

        # Loading check result, default to True.
        # Set to False if one client hasn't finished loading.
        loaded = True

        # Check if all clients have finished loading
        for slot in room['slots']:
            if not room['slots'][slot]['loaded']:
                loaded = False

        # Skip current iteration if at least once client hasn't loaded
        if not loaded:
            continue

        # Has everyone loaded the game? Start the game by calling load_finish
        load_finish(_args, room)

'''
This method will parse chat commands
'''
def chat_command(**_args):

    # Check if we are in a room, if not drop the packet
    room = Room.get_room(_args)
    if not room:
        return

    # Read message
    message = _args['packet'].ReadString()

    if message[0] == '@':
        command = message[1:]

        # Handle exit requests
        if command == 'exit':
            Room.remove_slot(_args, _args['client']['room'], _args['client'])

        # Force win command, only available to staff members
        elif command == 'win' and _args['client']['character']['position'] == 1:
            game_end(_args=_args, room=room, status=1)

        # Force lose command, only available to staff members
        elif command == 'lose' and _args['client']['character']['position'] == 1:
            game_end(_args=_args, room=room, status=0)

        # Force time over command, only available to staff members
        elif command == 'timeout' and _args['client']['character']['position'] == 1:
            game_end(_args=_args, room=room, status=2)

        # Force time over command (deathmatch variant), only available to staff members
        elif command == 'timeoutdm' and _args['client']['character']['position'] == 1:
            game_end(_args=_args, room=room, status=3)

        # Handle suicide requests
        elif command == 'suicide':

            # Drop packet if the game has not started
            if room['status'] != 3:
                return

            # This command is only supposed to work in planet mode
            if room['game_type'] == MODE_PLANET:
                result = player_death(_args, room)
                if result is not False:
                    Lobby.ChatMessage(_args['client'], 'You have just killed your player', 2)
            else:
                Lobby.ChatMessage(_args['client'], 'This command only works in planet mode', 2)

        # Handle kick requests
        elif command[:4] == 'kick':

            # Check message length
            if len(message) < 6:
                return

            # Check if we are the room master
            if room['master'] != _args['client']:
                return Lobby.ChatMessage(_args['client'], 'Only room masters can kick players from their rooms', 2)

            # Retrieve the character name of the new room master and attempt to find the user in the room
            who     = message[6:]
            slots   = room['slots'].items()

            # If we are trying to kick ourselves, stop.
            if who == _args['client']['character']['name']:
                return Lobby.ChatMessage(_args['client'], 'You can not kick yourself', 2)

            # Attempt to find the player we are trying to kick from the room
            for key, slot in slots:
                if slot['client']['character']['name'] == who:
                    Room.remove_slot(_args, room['id'], slot['client'], 2)
                    return

            # If we have passed the loop with no result, the player was not found
            Lobby.ChatMessage(_args['client'], 'Player {0} not found'.format(who), 2)

        elif command == 'help':

            # List of commands
            commands = [

                {
                    "command": "@help",
                    "description": "Show a list of available commands"
                },

                {
                    "command": "@exit",
                    "description": "Leaves the current room you are in"
                },

                {
                    "command": "@suicide",
                    "description": "Kills your player"
                },

                {
                    "command": "@kick <name>",
                    "description": "Kicks a player from your room"
                }
            ]

            for command in commands:
                Lobby.ChatMessage(_args['client'], '{0} -- {1}'.format(command['command'], command['description']), 2)

        else:
            Lobby.ChatMessage(_args['client'], 'Unknown command. Type @help for a list of commands', 2)