# Packet name             # Header      # Client-side function name             Packet ID

REPLY_USER_OUT          = b'\x2E\x27'   # CBattleRoom::ReplyUserOut()           10030
REPLY_GAME_LIST         = b'\xEF\x2E'   # CLobby::ReplyGameList()               12271
REPLY_GAME_INFO_UPDATE  = b'\x20\x2F'   # CBattleRoom::ReplyGameInfoUpdate()    12064
REPLY_JOIN_GAME         = b'\x28\x2F'   # CLobby::ReplyJoinGame()               12072
REPLY_ADD_CLIENT_INFO   = b'\x29\x27'   # CBattleRoom::AddClientInfo()          12073
REPLY_GAME_JOIN_NEW     = b'\xEE\x2E'   # CLobby::ReplyGameJoinNew()            12014
REPLY_START_GAME        = b'\xF3\x2E'   # CBattleRoom::ReplyStartGame()         12019
REPLY_CHANGE_LEVEL      = b'\x4A\x2F'   #                                       12106
REPLY_ROOM_ENTER_SHOP   = b'\x60\x2F'   #                                       12128
REPLY_ROOM_EXIT_SHOP    = b'\x61\x2F'   #                                       12129
REPLY_SET_DIFFICULTY    = b'\x62\x2F'   #                                       12130
REPLY_CHANGE_PASSWORD   = b'\x38\x2F'   #                                       12088
