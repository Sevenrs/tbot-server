from GameServer.Controllers import BoutLogin, Lobby, Shop, Guild, Friend, Inbox, Room, Character, Game

PACKET_NAME             = 0
PACKET_HANDLER          = 1
PACKET_MYSQL_REQUIRED   = 2

PACKET_READ = {
    '0200': ('PACKET_PONG',                     BoutLogin.pong,             False),
    'f82a': ('PACKET_ID_REQUEST',               BoutLogin.id_request,       True),
    'f92a': ('PACKET_GET_CHARACTER',            BoutLogin.get_character,    True),
    'fa2a': ('PACKET_CREATE_CHARACTER',         BoutLogin.create_character, True),
    '222b': ('PACKET_EXIT_SERVER',              BoutLogin.exit_server,      False),

    '082b': ('PACKET_LOBBY_REQUEST',            Lobby.GetLobby,             True),
    '1a27': ('PACKET_LOBBY_CHAT',               Lobby.Chat,                 True),
    '412b': ('PACKET_LOBBY_EXAMINE_PLAYER',     Lobby.examine_player,       True),
    '442b': ('PACKET_LOBBY_WHISPER',            Lobby.Whisper,              False),
    '0a2b': ('PACKET_LOBBY_ROOMS',              Lobby.RoomList,             False),

    '272b': ('PACKET_FRIEND_REQUEST',           Friend.FriendRequest,       False),
    '242b': ('PACKET_FRIEND_REQUEST_RESULT',    Friend.FriendRequestResult, True),
    '252b': ('PACKET_FRIEND_DELETE',            Friend.DeleteFriend,        True),

    '282b': ('PACKET_INBOX_REQUEST',            Inbox.RequestInbox,         True),
    '292b': ('PACKET_INBOX_SEND',               Inbox.SendMessage,          True),
    '2a2b': ('PACKET_INBOX_VIEW',               Inbox.RequestMessage,       True),
    '2b2b': ('PACKET_INBOX_DELETE',             Inbox.DeleteMessage,        True),

    '512b': ('PACKET_SHOP_SYNC_CASH',           Shop.sync_cash_rpc,         True),
    '022b': ('PACKET_SHOP_PURCHASE_GOLD',       Shop.purchase_item,         True),
    '042b': ('PACKET_SHOP_PURCHASE_CASH',       Shop.purchase_item,         True),
    '032b': ('PACKET_SHOP_SELL',                Shop.sell_item,             True),
    'fc2a': ('PACKET_SHOP_EQUIP_PART',          Shop.wear_item,             True),
    '322b': ('PACKET_SHOP_EQUIP_ACCESSORY',     Shop.wear_item,             True),
    '342b': ('PACKET_SHOP_EQUIP_PACK',          Shop.wear_item,             True),
    'fd2a': ('PACKET_SHOP_REMOVE_PART',         Shop.unwear_item,           True),
    '332b': ('PACKET_SHOP_REMOVE_ACCESSORY',    Shop.unwear_item,           True),
    '352b': ('PACKET_SHOP_REMOVE_PACK',         Shop.unwear_item,           True),

    '552b': ('PACKET_GUILD_CREATE',             Guild.Create,                   True),
    '562b': ('PACKET_GUILD_APPLY',              Guild.SendGuildApplication,     True),
    '572b': ('PACKET_GUILD_CANCEL_APPLICATION', Guild.CancelGuildApplication,   True),
    '642b': ('PACKET_GUILD_GET_APPLICATIONS',   Guild.FetchGuildApplications,   True),
    '5a2b': ('PACKET_GUILD_ACCEPT_APPLICATION', Guild.AcceptApplication,        True),
    '5b2b': ('PACKET_GUILD_REFUSE_APPLICATION', Guild.RejectApplication,        True),
    '5d2b': ('PACKET_GUILD_LEAVE',              Guild.LeaveGuild,               True),
    '592b': ('PACKET_GUILD_EXPEL_MEMBER',       Guild.ExpelGuildMember,         True),
    '732b': ('PACKET_GUILD_UPDATE_NOTICE',      Guild.UpdateGuildNotice,        True),

    '062b': ('PACKET_ROOM_JOIN',                Room.join_room,             True),
    '092b': ('PACKET_ROOM_CREATE',              Room.create,                False),
    '0e2b': ('PACKET_ROOM_QUICK_JOIN',          Room.quick_join,            True),
    '0b2b': ('PACKET_ROOM_START_GAME',          Room.start_game,            False),
    '392b': ('PACKET_ROOM_UPDATE_SLOT_STATUS',  Room.set_status,            False),
    '402b': ('PACKET_ROOM_KICK_PLAYER',         Room.kick_player,           False),
    '422b': ('PACKET_ROOM_EXIT',                Room.exit_room,             False),
    '652b': ('PACKET_ROOM_SET_LEVEL',           Room.set_level,             False),
    '7a2b': ('PACKET_ROOM_SET_DIFFICULTY',      Room.set_difficulty,        False),
    '782b': ('PACKET_ROOM_ENTER_SHOP',          Room.enter_shop,            False),
    '792b': ('PACKET_ROOM_EXIT_SHOP',           Room.exit_shop,             True),

    '6f2b': ('PACKET_GAME_PLAYER_DEATH',        Game.player_death_rpc,      False),
    '362b': ('PACKET_GAME_USE_FIELD_PACK',      Game.use_field_pack,        True),
    '3a2b': ('PACKET_GAME_MONSTER_DEATH',       Game.monster_kill,          False),
    '3c2b': ('PACKET_GAME_USE_ITEM',            Game.use_item,              True),
    '3e2b': ('PACKET_GAME_LOAD_FINISH',         Game.load_finish,           False),
    '3b2b': ('PACKET_GAME_LOSE',                Game.game_end_rpc,          True),
    '462b': ('PACKET_GAME_WIN',                 Game.game_end_rpc,          True),
    'a627': ('PACKET_GAME_CHAT_COMMAND',        Game.chat_command,          False),
    'a628': ('PACKET_GAME_SET_ATTACK_SCORE',    Game.set_score,             False)
}