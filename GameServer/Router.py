#!/usr/bin/env python3
__author__ = "Icseon"
__copyright__ = "Copyright (C) 2020 Icseon"
__version__ = "1.0"

# Import MySQL interface to communicate with the database
import MySQL.Interface as MySQL

# Import all packet handlers to use throughout the service
from GameServer.Controllers import BoutLogin, Lobby, Shop, Guild, Friend, Inbox, Room, Character, Game

"""
This method will link the incoming packet to the right controller
Similarly in backends seen in websites
"""

def route(socket, packet, server, client, connection_handler):

    """
    If our client has no connected character with it, it means that the client is attempting to communicate with the server without
    having sent a ID request first.

    We must check if the client exists in the global client container and check if the command ID is equal to the ID request
    and we must check if the client has a character, and if not we must only accept the character create packet
    """
    if client not in server.clients and packet.id != 'f82a' or 'character' not in client and client in server.clients and not (
            packet.id == 'fa2a'):
        raise Exception('Invalid packet received')

    # Create new MySQL connection
    mysql_connection = MySQL.GetConnection()
    mysql = mysql_connection.cursor(dictionary=True, buffered=True)

    # Define packet commands to handle as well as their methods
    packets = {

        # Controller: Bout Authentication
        '0200': BoutLogin.pong,
        'f82a': BoutLogin.id_request,
        'f92a': BoutLogin.get_character,
        'fa2a': BoutLogin.create_character,
        '222b': BoutLogin.exit_server,

        # Controller: Lobby
        '082b': Lobby.GetLobby,
        '1a27': Lobby.Chat,
        '412b': Lobby.examine_player,
        '442b': Lobby.Whisper,
        '0a2b': Lobby.RoomList,

        # Controller: Friends
        '272b': Friend.FriendRequest,
        '242b': Friend.FriendRequestResult,
        '252b': Friend.DeleteFriend,

        # Controller: Inbox
        '282b': Inbox.RequestInbox,
        '292b': Inbox.SendMessage,
        '2a2b': Inbox.RequestMessage,
        '2b2b': Inbox.DeleteMessage,

        # Controller: Shop
        '512b': Shop.sync_cash_rpc,
        '022b': Shop.purchase_item,     # Gold items
        '042b': Shop.purchase_item,     # Cash items
        '032b': Shop.sell_item,

        'fc2a': Shop.wear_item,         # Parts
        '322b': Shop.wear_item,         # Accessories
        '342b': Shop.wear_item,         # Packs

        'fd2a': Shop.unwear_item,       # Parts
        '332b': Shop.unwear_item,       # Accessories
        '352b': Shop.unwear_item,       # Packs

        # Controller: Guild
        '552b': Guild.Create,
        '562b': Guild.SendGuildApplication,
        '572b': Guild.CancelGuildApplication,
        '642b': Guild.FetchGuildApplications,
        '5a2b': Guild.AcceptApplication,
        '5b2b': Guild.RejectApplication,
        '5d2b': Guild.LeaveGuild,
        '592b': Guild.ExpelGuildMember,
        '732b': Guild.UpdateGuildNotice,

        # Controller: Room
        '062b': Room.join_room,
        '092b': Room.create,
        '0e2b': Room.quick_join,
        '0b2b': Room.start_game,
        '392b': Room.set_status,
        '402b': Room.kick_player,
        '422b': Room.exit_room,
        '652b': Room.set_level,
        '7a2b': Room.set_difficulty,
        '782b': Room.enter_shop,
        '792b': Room.exit_shop,

        # Controller: Game
        '6f2b': Game.player_death_rpc,
        '362b': Game.use_field_pack,
        '3a2b': Game.monster_kill,
        '3c2b': Game.use_item,
        '3e2b': Game.load_finish,
        '3b2b': Game.game_end_rpc,  # Game lost
        '462b': Game.game_end_rpc,  # Game won
        'a627': Game.chat_command,
        'a628': Game.set_score

    }.get(packet.id, unknown)(**locals())

    # Close MySQL connection after packet has been parsed
    mysql_connection.close()


"""
Handle unknown packets
"""

def unknown(**_args):
    print('Unknown packet: <0x{0}[len={2}]::{1}>'.format(_args['packet'].id, _args['packet'].data, len(_args['packet'].data)))
