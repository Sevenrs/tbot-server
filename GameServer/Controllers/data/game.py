MODE_BATTLE = 0
MODE_TEAM_BATTLE = 1
MODE_PLANET = 2
MODE_MILITARY = 3
MODE_DEATHMATCH = 4

TEAM_NONE = 0
TEAM_RED = 1
TEAM_BLUE = 2

DIFFICULTY_EASY = 0
DIFFICULTY_MEDIUM = 1
DIFFICULTY_HARD = 2

ROOM_CALLBACKS = ['event_weekends', 'event_christmas', 'callback_monster_kill']

# Player data is used to count numbers per slot.
# So if a slot has two monster kills, an object in monster_kills with key 0 would be 2.
# This is required because if we rely on slots, the tracking would not be accurate because slots can be removed.
PLAYER_DATA_DEFAULT = {
    'monster_kills': {},  # Amount of monster kills per slot
    'attack_points': {},  # Attack score per slot
    'pushed_mobs': []  # Array containing the killed mobs which have been pushed
}
