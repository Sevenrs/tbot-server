from Packet.Write                       import Write as PacketWrite
from GameServer.Controllers.data.game   import MODE_PLANET
from GameServer.Controllers             import Room, Lobby
import datetime

"""
This method will register this event, if the conditions in the method are met
"""
def register(room):
    for event in ['start_game', 'reset']:
        Room.register_callback(room, event, 'event_weekends')

def reset(_args, room):
    room['experience_modifier'] = 1.0

'''
This method will execute once the game is started
'''
def start_game(_args, room):

    # Determine whether or not we are awarding +50% experience
    awarding = (datetime.datetime.today().weekday() >= 5 or (datetime.datetime.now().month == 2 and (datetime.datetime.now().day == 1))) and room['game_type'] == MODE_PLANET

    # If we are awarding more experience, mutate the experience modifier
    if awarding:
        room['experience_modifier'] = 1.5

    # Send experience banner state to the room
    banner = PacketWrite()
    banner.AddHeader([0x28, 0x27])
    banner.AppendBytes([0x01 if awarding else 0x00, 0x00])
    _args['connection_handler'].SendRoomAll(room['id'], banner.packet)