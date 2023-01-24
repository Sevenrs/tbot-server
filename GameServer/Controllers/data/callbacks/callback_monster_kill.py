from GameServer.Controllers import Room, Lobby, Game
import _thread

"""
Callback event registration method
"""


def register(room):
    Room.register_callback(room, 'monster_kill', 'callback_monster_kill')


'''
This method will run once a monster has been killed
'''


def monster_kill(_args, room):
    # Do nothing if the room level is not in the map scripts array
    if room['level'] not in [
        13  # Acurin Ruins 2
    ]: return

    # Read monster ID from the packet
    monster_id = _args['packet'].get_byte(0)

    # Determine what method to execute based on the room's current map
    level_scripts = {
        13: lv33_acurin_ruins_2
    }.get(room['level'])(**locals())


'''
Custom script logic for level 33 (Acurin Ruins 2)
'''


def lv33_acurin_ruins_2(_args, room, monster_id):
    """
    Energy ball handler
    """

    # Array containing monster ID and text of the energy balls
    energy_balls = {
        70: 'Left energy ball destroyed!',
        78: 'Right energy ball destroyed!',
    }

    ''' Check if the monster ID is an energy ball. If it is,
        we'll send yellow text to the client as story '''
    if monster_id in energy_balls.keys():

        # Create a message for the ball we just destroyed
        message = Lobby.chat_message(target=None,
                                     message=energy_balls[monster_id],
                                     color=3,
                                     return_packet=True)
        _args['connection_handler'].room_broadcast(room['id'], message)

        # Check if both energy balls have been destroyed. If so, we send another message
        if all(elem in room['killed_mobs'] for elem in energy_balls.keys()):
            # Construct final story message
            message = Lobby.chat_message(target=None,
                                         message='Both energy balls have been destroyed. Well done!',
                                         color=3,
                                         return_packet=True
                                         )
            _args['connection_handler'].room_broadcast(room['id'], message)

    """
    Countdown timer handler
    """

    # Monsters that need to be killed before we start the timer
    previous_block = [54, 55, 56, 57, 58]

    # Check if the monster ID is in the previous block and check if all the monsters in the previous block have been
    # killed.
    if monster_id in previous_block and all(elem in room['killed_mobs'] for elem in previous_block):
        _thread.start_new_thread(Game.countdown_timer, (_args, room, 3,))
