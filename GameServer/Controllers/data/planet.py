from GameServer.Controllers.data.drops import *

# This table contains the experience points to award per planet level.
# Structure: Level index, base experience, minutes, recommended level, minimum attack score to pass the level and minimum monster kills

PLANET_MAP_TABLE = {
    0: (60,     7.5,    1,  1100,   17),    # [Lv01]Training Camp
    1: (60,     10.5,   3,  1400,   13),    # [Lv03]Base Camp
    2: (80,     10.5,   6,  1800,   27),    # [Lv06]Camp-Spike
    3: (80,     15,     8,  1800,   38),    # [Lv08]Camp-Spike2
    4: (120,    18,     10, 2000,   22),    # [Lv10]Planet-Alderan
    5: (160,    19.5,   13, 2600,   20),    # [Lv13]Alderan-Entrance
    6: (160,    19.5,   16, 500,    24),    # [Lv16]Mine-Alderan
    7: (170,    21,     18, 500,    25),    # [Lv18]Mine-Alderan2
    8: (250,    21,     20, 3100,   25),    # [Lv20]Mine-Blaster
    9: (290,    22.5,   23, 3100,   27),    # [Lv23]Lava-Sea1
    10: (300,   22.5,   26, 500,    25),    # [Lv26]Lava-Sea2
    11: (330,   22.5,   28, 800,    47),    # [Lv28]Lava-Sea3
    12: (450,   22.5,   30, 800,    17),    # [Lv30]Acurin-Ruins1
    13: (450,   22.5,   33, 1300,   31),    # [Lv33]Acurin-Ruins2
    14: (500,   22.5,   36, 4400,   62),    # [Lv36]Planet-Acurin
    15: (520,   24,     38, 4500,   48),    # [Lv38]Planet-Acurin2
    16: (630,   24,     40, 4800,   41),    # [Lv40]Port-Acurin
    17: (630,   24,     43, 4900,   29),    # [Lv43]Escape-Acurin
    18: (650,   24,     46, 5500,   33),    # [Lv46]Planet-MECA
    19: (650,   24,     48, 5800,   64),    # [Lv48]Planet-MECA2
    20: (700,   24.5,   50, 5500,   44),    # [Lv50]Hidden-Archive
    21: (700,   25.5,   53, 6000,   39),    # [Lv53]Secret-passage
    22: (860,   25.5,   56, 10000,  8),     # [Lv56]Destroy-all
    23: (887,   25.5,   58, 6200,   39),    # [Lv58]Destroy-all2
    24: (1288,  27,     60, 13000,  8),     # [Lv60]Escape-From-MECA
    25: (1324,  27,     61, 4500,   15),    # [Lv61]Ship Takeover
    26: (1395,  27,     63, 5800,   55),    # [Lv63]MeraMountin
    27: (1402,  27,     66, 600,    44),    # [Lv66]MeraMountin2
    28: (1420,  27,     68, 900,    55),    # [Lv68]MeraMountin3
    29: (2266,  27,     70, 1000,   60),    # [Lv70]MeraMountin4

    30: (120,   18,     8,  2800,   21),    # [Lv08]The-Fallen(Elite)
    31: (255,   36,     18, 3500,   27),    # [Lv18]Lava-Field(Elite)
    32: (495,   45,     28, 4000,   25),    # [Lv28]The-Pirate(Elite)
    33: (780,   45,     38, 5000,   40),    # [Lv38]Evil-Port(Elite)
    34: (975,   48,     48, 5200,   49),    # [Lv48]Bloodway(Elite)
}
# This table contains the mob table from which to drops boxes from
PLANET_BOX_MOBS = {

    # [Lv01]Training Camp
    0: [
        32,
        33,
        50  # Boss
    ],

    # [Lv03]Base Camp
    1: [
        2,
        24 # Boss
    ],

    # [Lv06]Camp-Spike
    2: [
        18,
        36 # Boss
    ],

    # [Lv08]Camp-Spike2
    3: [
        33,
        34,
        44,
        45,
        50 # Boss
    ],

    # [Lv10]Planet-Alderan
    4: [
        20,
        21,
        23,
        40,
        47,
        49  # Boss
    ],

    # [Lv13]Alderan-Entrance
    5: [
        11,
        14,
        37,
        44  # Boss
    ],

    # [Lv16]Mine-Alderan
    6: [
        12,
        23,
        24,
        25,
        30,
        34,
        35,
        47,
        45 # Boss
    ],

    # [Lv18]Mine-Alderan2
    7: [
        33,
        34,
        35,
        71,
        89,
        90,
        91,
        83 # Boss
    ],

    # [Lv20]Mine-Blaster
    8: [
        24,
        25,
        34,
        35,
        41,
        42,
        43,
        44,
        49,
        50,
        55 # Boss
    ],

    # [Lv23]Lava-Sea1
    9: [
        21,
        33,
        34,
        35,
        50 # Boss
    ],

    # [Lv26]Lava-Sea2
    10: [
        28,
        29,
        30,
        67,
        72,
        73,
        74,
        75,
        76 # Boss
    ],

    # [Lv28]Lava-Sea3
    11: [
        28,
        29,
        95,
        96,
        97,
        88 # Boss
    ],

    # [Lv30]Acurin-Ruins1
    12: [
        16,
        21,
        33,
        39,
        40,
        44,
        56,
        59,
        76,
        78,
        79,
        77,
        71 # Boss
    ],

    # [Lv33]Acurin-Ruins2
    13: [
        0,
        14,
        24,
        25,
        26,
        40,
        41,
        49,
        58,
        71,
        72,
        78,
        79,
        80,
        70 # Boss
    ],

    # [Lv36]Planet-Acurin
    14: [
        14,
        25,
        31,
        36,
        44,
        50,
        53,
        66,
        69,
        70,
        76,
        81,
        101 # Boss
    ],

    # [Lv38]Planet-Acurin2
    15: [
        12,
        17,
        30,
        35,
        38,
        39,
        44,
        49,
        51,
        53,
        66,
        67,
        72,
        73,
        76,
        89,
        100,
        109,
        110,
        97  # Boss
    ],

    # [Lv40]Port-Acurin
    16: [
        26,
        27,
        28,
        33,
        77 # Boss
    ],

    # [Lv43]Escape-Acurin
    17: [
        9,
        30,
        62,
        64,
        47,
        48,
        53,
        61 # Boss
    ],

    # [Lv46]Planet-MECA
    18: [
        16,
        17,
        43,
        44,
        45,
        56,
        69,
        70,
        71,
        67,
        77 # Boss
    ],

    # [Lv48]Planet-MECA2
    19: [
        108,
        107,
        105 # Boss
    ],

    # [Lv50]Hidden-Archive
    20: [
        30,
        51,
        50,
        49,
        61,
        71,
        69,
        70,
        89,
        90,
        83 # Boss
    ],

    # [Lv53]Secret-passage
    21: [
        9,
        21,
        41,
        40,
        42,
        43,
        72,
        73,
        87,
        88,
        81 # Boss
    ],

    # [Lv56]Destroy-all
    22: [
        35,
        36,
        65,
        101,
        102,
        107,
        105 # Boss
    ],

    # [Lv58]Destroy-all2
    23: [
        44,
        100 # Boss
    ],

    # [Lv60]Escape-From-MECA
    24: [
        38,
        39,
        40,
        52,
        53,
        55,
        73,
        74,
        97,
        99,
        98 # Boss
    ],

    # [Lv61]Ship Takeover
    25: [
        19,
        20,
        50,
        51,
        52,
        75,
        76,
        96,
        97,
        102
    ],

    # [Lv63]MeraMountin
    26: [
        19,
        20,
        21,
        54,
        55,
        77,
        105,
        121,
        122,
        123,
        113 # Boss
    ],

    # [Lv66]MeraMountin2
    27: [
        29,
        30,
        31,
        50,
        60,
        61,
        62,
        95,
        96,
        97,
        118,
        119,
        120,
        122 # Boss
    ],

    # [Lv68]MeraMountin3
    28: [
        43,
        44,
        45,
        46,
        47,
        77,
        91,
        92,
        117,
        118,
        123 # Boss
    ],

    # [Lv70]MeraMountin4
    29: [
        43,
        44,
        45,
        46,
        87,
        125,
        121 # Boss
    ],

    # [Lv08]The-Fallen([Elite)
    30: [
        2,
        22,
        27,
        33  # Boss
    ],

    # [Lv18]Lava-Field([Elite)
    31: [
        25,
        33,
        34,
        35,
        52,
        53,
        50 # Boss
    ],

    # [Lv28]The-Pirate([Elite)
    32: [
        9,
        10,
        25,
        23,
        34,
        35,
        43,
        42,
        41,
        49,
        55 # Boss
    ],

    # [Lv38]Evil-Port([Elite)
    33: [
        16,
        17,
        24,
        26,
        28,
        54,
        74,
        75,
        76,
        77 # Boss
    ],

    # [Lv48]Bloodway(Elite)
    34: [
        30,
        37,
        49,
        50,
        61,
        69,
        70,
        89,
        90,
        83 # Boss
    ]
}

'''
This object contains all the monster IDs that should drop assist canisters, meaning they would drop many
'''
PLANET_ASSISTS = {


    # [Lv46]Planet-MECA
    18: [
        34
    ],

    # [Lv50]Hidden-Archive
    20: [
        60
    ],

    # [Lv53]Secret-passage
    21: [
        28
    ],

    # [Lv56]Destroy-all
    22: [
        64
    ],

    # [Lv60]Escape-From-MECA
    24: [
        56
    ],

    # [Lv61]Ship Takeover
    25: [
        33,
        59
    ],

    # [Lv63]MeraMountin
    26: [
        75
    ],

    # [Lv66]MeraMountin2
    27: [
        82
    ],

    # [Lv68]MeraMountin3
    28: [
        79
    ],

    # [Lv70]MeraMountin4
    29: [
        88
    ],

    # [Lv48]Bloodway(Elite)
    34: [
        60
    ]

}

'''
This object contains the mob IDs that should drop canisters even if they have respawned
'''
PLANET_CANISTER_EXCEPTIONS = {

    # [Lv30]Acurin-Ruins1
    12: [
        67,
        68,
        69,
        70,
        72,
        73,
        74,
        75
    ]

}

'''
This object contains all box drop types and their chances per planet map
'''
PLANET_BOXES = {

    #[Lv01]Training Camp
    0: [
        (BOX_GUN, 0.04),
        (BOX_EF, 0.04),
        (BOX_MINI_BOT, 0.04),
        (BOX_HEAD, 0.04),
        (BOX_BODY, 0.04),
        (BOX_ARMS, 0.04)
    ],

    # [Lv03]Base Camp
    1: [
        (BOX_GUN, 0.04),
        (BOX_EF, 0.04),
        (BOX_MINI_BOT, 0.04),
        (BOX_HEAD, 0.04),
        (BOX_BODY, 0.04),
        (BOX_ARMS, 0.04)
    ],

    # [Lv06]Camp-Spike
    2: [
        (BOX_GUN, 0.04),
        (BOX_EF, 0.04),
        (BOX_MINI_BOT, 0.04),
        (BOX_HEAD, 0.04),
        (BOX_BODY, 0.04),
        (BOX_ARMS, 0.04)
    ],

    # [Lv08]Camp-Spike2
    3: [
        (BOX_GUN, 0.04),
        (BOX_EF, 0.04),
        (BOX_MINI_BOT, 0.04),
        (BOX_HEAD, 0.04),
        (BOX_BODY, 0.04),
        (BOX_ARMS, 0.04)
    ],

    # [Lv10]Planet-Alderan
    4: [
        (BOX_GUN, 0.04),
        (BOX_EF, 0.04),
        (BOX_MINI_BOT, 0.04),
        (BOX_HEAD, 0.04),
        (BOX_BODY, 0.04),
        (BOX_ARMS, 0.04)
    ],

    # [Lv13]Alderan-Entrance
    5: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv16]Mine-Alderan
    6: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv18]Mine-Alderan2
    7: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv20]Mine-Blaster
    8: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv23]Lava-Sea1
    9: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv26]Lava-Sea2
    10: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv28]Lava-Sea3
    11: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv30]Acurin-Ruins1
    12: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv33]Acurin-Ruins2
    13: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv36]Planet-Acurin
    14: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv38]Planet-Acurin2
    15: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv40]Port-Acurin
    16: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv43]Escape-Acurin
    17: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv46]Planet-MECA
    18: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv48]Planet-MECA2
    19: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv50]Hidden-Archive
    20: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv53]Secret-passage
    21: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv56]Destroy-all
    22: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv58]Destroy-all2
    23: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv60]Escape-From-MECA
    24: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv61]Ship Takeover
    25: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv63]MeraMountin
    26: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv66]MeraMountin2
    27: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv68]MeraMountin3
    28: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv70]MeraMountin4
    29: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv08]The-Fallen(Elite)
    30: [
        (BOX_GUN, 0.04),
        (BOX_EF, 0.04),
        (BOX_MINI_BOT, 0.04),
        (BOX_HEAD, 0.04),
        (BOX_BODY, 0.04),
        (BOX_ARMS, 0.04)
    ],

    # [Lv18]Lava-Field(Elite)
    31: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv28]The-Pirate(Elite)
    32: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv38]Evil-Port(Elite)
    33: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ],

    # [Lv48]Bloodway(Elite)
    34: [
        (BOX_GUN, 0.018),
        (BOX_SHIELD, 0.018),
        (BOX_EF, 0.018),
        (BOX_SHOULDER, 0.018),
        (BOX_MINI_BOT, 0.018),
        (BOX_HEAD, 0.018),
        (BOX_BODY, 0.018),
        (BOX_ARMS, 0.018)
    ]
}

'''
For each type defined in the object above, this contains all their drops and their chances
'''
PLANET_DROPS = {

    #[Lv01]Training Camp
    0: {
        BOX_GUN: [
            (3021101, 0.60), # HydraGun(+1)
            (3021102, 0.25), # HydraGun(+2)
            (3021103, 0.15)  # HydraGun(+3)
        ],

        BOX_EF: [
            (3031101, 0.33), # S-TornadoCRT(+1)
            (3031102, 0.33), # S-TornadoMIS(+1)
            (3031103, 0.33)  # S-TornadoBST(+1)
        ],

        BOX_MINI_BOT: [
            (3011101, 0.20), # BipadCRT(+1)
            (3011102, 0.20), # BipadMIS(+1)
            (3011103, 0.20), # BipadBST(+1)
            (3011104, 0.14), # BipadCRT(+2)
            (3011105, 0.13), # BipadMIS(+2)
            (3011106, 0.13)  # BipadBST(+2)
        ],

        BOX_HEAD: [
            (1010101, 0.60),  # HammererCRT(+1) — CrossgearMIS(+1) — ChainShellSP(+1)
            (1010102, 0.30),  # HammererCRT(+2) — CrossgearMIS(+2) — ChainShellSP(+2)
            (1010103, 0.10)   # HammererCRT(+3) — CrossgearMIS(+3) — ChainShellSP(+3)
        ],

        BOX_BODY: [
            (1020101, 0.60),  # HammererCRT(+1) — CrossgearBST(+1) — ChainShellMX(+1)
            (1020102, 0.30),  # HammererCRT(+2) — CrossgearBST(+2) — ChainShellMX(+2)
            (1020103, 0.10)   # HammererCRT(+3) — CrossgearBST(+3) — ChainShellMX(+3)
        ],

        BOX_ARMS: [
            (1030101, 0.60),  # HammererTD(+1) — CrossgearGUN(+1) — ChainShellTG(+1)
            (1030102, 0.30),  # HammererTD(+2) — CrossgearGUN(+2) — ChainShellTG(+2)
            (1030103, 0.10)   # HammererTD(+3) — CrossgearGUN(+3) — ChainShellTG(+3)
        ]
    },

    # [Lv03]Base Camp
    1: {
        BOX_GUN: [
            (3021101, 0.20), # HydraGun(+1)
            (3021102, 0.70), # HydraGun(+2)
            (3021103, 0.10)  # HydraGun(+3)
        ],

        BOX_EF: [
            (3031101, 0.33), # S-TornadoCRT(+1)
            (3031102, 0.33), # S-TornadoMIS(+1)
            (3031103, 0.33)  # S-TornadoBST(+1)
        ],

        BOX_MINI_BOT: [
            (3011101, 0.15), # BipadCRT(+1)
            (3011102, 0.15), # BipadMIS(+1)
            (3011103, 0.15), # BipadBST(+1)
            (3011104, 0.15), # BipadCRT(+2)
            (3011105, 0.15), # BipadMIS(+2)
            (3011106, 0.15), # BipadBST(+2)
            (3011107, 0.04), # BipadCRT(+3)
            (3011108, 0.03), # BipadMIS(+3)
            (3011109, 0.03)  # BipadBST(+3)
        ],

        BOX_HEAD: [
            (1010101, 0.60),  # HammererCRT(+1) — CrossgearMIS(+1) — ChainShellSP(+1)
            (1010102, 0.30),  # HammererCRT(+2) — CrossgearMIS(+2) — ChainShellSP(+2)
            (1010103, 0.10)   # HammererCRT(+3) — CrossgearMIS(+3) — ChainShellSP(+3)
        ],

        BOX_BODY: [
            (1020101, 0.60),  # HammererCRT(+1) — CrossgearBST(+1) — ChainShellMX(+1)
            (1020102, 0.30),  # HammererCRT(+2) — CrossgearBST(+2) — ChainShellMX(+2)
            (1020103, 0.10)   # HammererCRT(+3) — CrossgearBST(+3) — ChainShellMX(+3)
        ],

        BOX_ARMS: [
            (1030101, 0.60),  # HammererTD(+1) — CrossgearGUN(+1) — ChainShellTG(+1)
            (1030102, 0.30),  # HammererTD(+2) — CrossgearGUN(+2) — ChainShellTG(+2)
            (1030103, 0.10)   # HammererTD(+3) — CrossgearGUN(+3) — ChainShellTG(+3)
        ]
    },

    # [Lv06]Camp-Spike
    2: {
        BOX_GUN: [
            (3021101, 0.10), # HydraGun(+1)
            (3021102, 0.50), # HydraGun(+2)
            (3021103, 0.20), # HydraGun(+3)
            (3021201, 0.20)  # smartGun(+1)
        ],

        BOX_EF: [
            (3031101, 0.20), # S-TornadoCRT(+1)
            (3031102, 0.20), # S-TornadoMIS(+1)
            (3031103, 0.20), # S-TornadoBST(+1)
            (3031104, 0.10), # S-TornadoCRT(+2)
            (3031105, 0.10), # S-TornadoMIS(+2)
            (3031106, 0.10), # S-TornadoBST(+2)
            (3031107, 0.04), # S-TornadoCRT(+3)
            (3031108, 0.03), # S-TornadoMIS(+3)
            (3031109, 0.03)  # S-TornadoBST(+3)
        ],

        BOX_MINI_BOT: [
            (3011107, 0.10),    # BipadCRT(+3)
            (3011104, 0.10),    # BipadCRT(+2)
            (3011105, 0.10),    # BipadMIS(+2)
            (3011106, 0.10),    # BipadBST(+2)
            (3011109, 0.10),    # BipadBST(+3)
            (3011108, 0.10),    # BipadMIS(+3)
            (3011202, 0.075),   # BisliderMIS(+1)
            (3011201, 0.065),   # BisliderCRT(+1)
            (3011101, 0.065),   # BipadCRT(+1)
            (3011103, 0.065),   # BipadBST(+1)
            (3011102, 0.065),   # BipadMIS(+1)
            (3011203, 0.065)    # BisliderBST(+1)
        ],

        BOX_HEAD: [
            (1010201, 0.60),  # SpikeyCRT(+1) — Lea-ClawMIS(+1) — TweezerHeadSP(+1)
            (1010202, 0.30),  # SpikeyCRT(+2) — Lea-ClawMIS(+2) — TweezerHeadSP(+2)
            (1010203, 0.10)   # SpikeyCRT(+3) — Lea-ClawMIS(+3) — TweezerHeadSP(+3)
        ],

        BOX_BODY: [
            (1020201, 0.60),  # SpikeyTA(+1) — Lea-ClawBST(+1) — TweezerHeadMX(+1)
            (1020202, 0.30),  # SpikeyTA(+2) — Lea-ClawBST(+2) — TweezerHeadMX(+2)
            (1020203, 0.10)   # SpikeyTA(+3) — Lea-ClawBST(+3) — TweezerHeadMX(+3)
        ],

        BOX_ARMS: [
            (1030201, 0.60),  # SpikeyTD(+1) — Lea-ClawGUN(+1) — TweezerHeadTG(+1)
            (1030202, 0.30),  # SpikeyTD(+2) — Lea-ClawGUN(+2) — TweezerHeadTG(+2)
            (1030203, 0.10)   # SpikeyTD(+3) — Lea-ClawGUN(+3) — TweezerHeadTG(+3)
        ]
    },

    # [Lv08]Camp-Spike2
    3: {
        BOX_GUN: [
            (3021102, 0.30), # HydraGun(+2)
            (3021103, 0.20), # HydraGun(+3)
            (3021201, 0.40), # smartGun(+1)
            (3021202, 0.10)  # smartGun(+2)
        ],

        BOX_EF: [
            (3031104, 0.20), # S-TornadoCRT(+2)
            (3031105, 0.20), # S-TornadoMIS(+2)
            (3031106, 0.20), # S-TornadoBST(+2)
            (3031101, 0.075), # S-TornadoCRT(+1)
            (3031102, 0.065), # S-TornadoMIS(+1)
            (3031103, 0.065), # S-TornadoBST(+1)
            (3031107, 0.065), # S-TornadoCRT(+3)
            (3031108, 0.065), # S-TornadoMIS(+3)
            (3031109, 0.065)  # S-TornadoBST(+3)
        ],

        BOX_MINI_BOT: [
            (3011107, 0.20), # BipadCRT(+3)
            (3011108, 0.20), # BipadMIS(+3)
            (3011109, 0.20), # BipadBST(+3)
            (3011104, 0.075), # BipadCRT(+2)
            (3011105, 0.065), # BipadMIS(+2)
            (3011106, 0.065), # BipadBST(+2)
            (3011201, 0.065), # BisliderCRT(+1)
            (3011202, 0.065), # BisliderMIS(+1)
            (3011203, 0.065)  # BisliderBST(+1)
        ],

        BOX_HEAD: [
            (1010201, 0.60),  # SpikeyCRT(+1) — Lea-ClawMIS(+1) — TweezerHeadSP(+1)
            (1010202, 0.30),  # SpikeyCRT(+2) — Lea-ClawMIS(+2) — TweezerHeadSP(+2)
            (1010203, 0.10)   # SpikeyCRT(+3) — Lea-ClawMIS(+3) — TweezerHeadSP(+3)
        ],

        BOX_BODY: [
            (1020201, 0.60),  # SpikeyTA(+1) — Lea-ClawBST(+1) — TweezerHeadMX(+1)
            (1020202, 0.30),  # SpikeyTA(+2) — Lea-ClawBST(+2) — TweezerHeadMX(+2)
            (1020203, 0.10)   # SpikeyTA(+3) — Lea-ClawBST(+3) — TweezerHeadMX(+3)
        ],

        BOX_ARMS: [
            (1030201, 0.60),  # SpikeyTD(+1) — Lea-ClawGUN(+1) — TweezerHeadTG(+1)
            (1030202, 0.30),  # SpikeyTD(+2) — Lea-ClawGUN(+2) — TweezerHeadTG(+2)
            (1030203, 0.10)   # SpikeyTD(+3) — Lea-ClawGUN(+3) — TweezerHeadTG(+3)
        ]
    },

    # [Lv10]Planet-Alderan
    4: {
        BOX_GUN: [
            (3021103, 0.40), # HydraGun(+3)
            (3021201, 0.20), # smartGun(+1)
            (3021202, 0.30), # smartGun(+2)
            (3021202, 0.10)  # smartGun(+3)
        ],

         BOX_EF: [
             (3031107, 0.10), # S-TornadoCRT(+3)
             (3031104, 0.10), # S-TornadoCRT(+2)
             (3031105, 0.10), # S-TornadoMIS(+2)
             (3031106, 0.10), # S-TornadoBST(+2)
             (3031109, 0.10), # S-TornadoBST(+3)
             (3031108, 0.10), # S-TornadoMIS(+3)
             (3031202, 0.075), # BlueCloudMIS(+1)
             (3031201, 0.065), # BlueCloudCRT(+1)
             (3031101, 0.065), # S-TornadoCRT(+1)
             (3031103, 0.065), # S-TornadoBST(+1)
             (3031102, 0.065), # S-TornadoMIS(+1)
             (3031203, 0.065)  # BlueCloudBST(+1)
         ],

        BOX_MINI_BOT: [
            (3011201, 0.125), # BisliderCRT(+1)
            (3011203, 0.125), # BisliderBST(+1)
            (3011202, 0.125), # BisliderMIS(+1)
            (3011107, 0.10),  # BipadCRT(+3)
            (3011108, 0.10),  # BipadMIS(+3)
            (3011109, 0.10),  # BipadBST(+3)
            (3011205, 0.0625),# BisliderMIS(+2)
            (3011204, 0.0625),# BisliderCRT(+2)
            (3011104, 0.05),  # BipadCRT(+2)
            (3011106, 0.05),  # BipadBST(+2)
            (3011105, 0.05),  # BipadMIS(+2)
            (3011206, 0.05)   # BisliderBST(+2)
        ],

        BOX_HEAD: [
            (1010201, 0.60),  # SpikeyCRT(+1) — Lea-ClawMIS(+1) — TweezerHeadSP(+1)
            (1010202, 0.30),  # SpikeyCRT(+2) — Lea-ClawMIS(+2) — TweezerHeadSP(+2)
            (1010203, 0.10)   # SpikeyCRT(+3) — Lea-ClawMIS(+3) — TweezerHeadSP(+3)
        ],

        BOX_BODY: [
            (1020201, 0.60),  # SpikeyTA(+1) — Lea-ClawBST(+1) — TweezerHeadMX(+1)
            (1020202, 0.30),  # SpikeyTA(+2) — Lea-ClawBST(+2) — TweezerHeadMX(+2)
            (1020203, 0.10)   # SpikeyTA(+3) — Lea-ClawBST(+3) — TweezerHeadMX(+3)
        ],

        BOX_ARMS: [
            (1030201, 0.60),  # SpikeyTD(+1) — Lea-ClawGUN(+1) — TweezerHeadTG(+1)
            (1030202, 0.30),  # SpikeyTD(+2) — Lea-ClawGUN(+2) — TweezerHeadTG(+2)
            (1030203, 0.10)   # SpikeyTD(+3) — Lea-ClawGUN(+3) — TweezerHeadTG(+3)
        ]
    },

    # [Lv13]Alderan-Entrance
    5: {
        BOX_GUN: [
            (3021201, 0.20), # smartGun(+1)
            (3021103, 0.30), # HydraGun(+3)
            (3021202, 0.40), # smartGun(+2)
            (3021203, 0.10)  # smartGun(+3)
        ],

        BOX_SHIELD: [
            (3051101, 0.33), # AegisTD(+1)
            (3051104, 0.33), # AegisGUN(+1)
            (3051107, 0.33)  # AegisTG(+1)
        ],

        BOX_EF: [
            (3031107, 0.15),  # S-TornadoCRT(+3)
            (3031108, 0.15),  # S-TornadoMIS(+3)
            (3031109, 0.15),  # S-TornadoBST(+3)
            (3031201, 0.15),  # BlueCloudCRT(+1)
            (3031202, 0.15),  # BlueCloudMIS(+1)
            (3031203, 0.15),  # BlueCloudBST(+1)
            (3031104, 0.04),  # S-TornadoCRT(+2)
            (3031105, 0.03),  # S-TornadoMIS(+2)
            (3031106, 0.03)   # S-TornadoBST(+2)
        ],

        BOX_SHOULDER: [
            (3060101, 0.33), # ShoulderGrdTD(+1)
            (3060104, 0.33), # ShoulderGrdGUN(+1)
            (3060107, 0.33)  # ShoulderGrdTG(+1)
        ],

        BOX_MINI_BOT: [
            (3011201, 0.15), # BisliderCRT(+1)
            (3011202, 0.15), # BisliderMIS(+1)
            (3011203, 0.15), # BisliderBST(+1)
            (3011204, 0.15), # BisliderCRT(+2)
            (3011205, 0.15), # BisliderMIS(+2)
            (3011206, 0.15), # BisliderBST(+2)
            (3011207, 0.04), # BisliderCRT(+3)
            (3011208, 0.03), # BisliderMIS(+3)
            (3011209, 0.03)  # BisliderBST(+3)
        ],

        BOX_HEAD: [
            (1010201, 0.60),  # SpikeyCRT(+1) — Lea-ClawMIS(+1) — TweezerHeadSP(+1)
            (1010202, 0.30),  # SpikeyCRT(+2) — Lea-ClawMIS(+2) — TweezerHeadSP(+2)
            (1010203, 0.10)   # SpikeyCRT(+3) — Lea-ClawMIS(+3) — TweezerHeadSP(+3)
        ],

        BOX_BODY: [
            (1020201, 0.60),  # SpikeyTA(+1) — Lea-ClawBST(+1) — TweezerHeadMX(+1)
            (1020202, 0.30),  # SpikeyTA(+2) — Lea-ClawBST(+2) — TweezerHeadMX(+2)
            (1020203, 0.10)   # SpikeyTA(+3) — Lea-ClawBST(+3) — TweezerHeadMX(+3)
        ],

        BOX_ARMS: [
            (1030201, 0.60),  # SpikeyTD(+1) — Lea-ClawGUN(+1) — TweezerHeadTG(+1)
            (1030202, 0.30),  # SpikeyTD(+2) — Lea-ClawGUN(+2) — TweezerHeadTG(+2)
            (1030203, 0.10)   # SpikeyTD(+3) — Lea-ClawGUN(+3) — TweezerHeadTG(+3)
        ]
    },

    # [Lv16]Mine-Alderan
    6: {
        BOX_GUN: [
            (3021203, 0.40), # smartGun(+3)
            (3021202, 0.30), # smartGun(+2)
            (3021103, 0.15), # HydraGun(+3)
            (3021301, 0.15)  # FableShooter(+1)
        ],

        BOX_SHIELD: [
            (3051101, 0.20), # AegisTD(+1)
            (3051104, 0.20), # AegisGUN(+1)
            (3051107, 0.20), # AegisTG(+1)
            (3051102, 0.14), # AegisTD(+2)
            (3051105, 0.13), # AegisGUN(+2)
            (3051108, 0.13)  # AegisTG(+2)
        ],

        BOX_EF: [
            (3031201, 0.125),   # BlueCloudCRT(+1)
            (3031202, 0.125),   # BlueCloudMIS(+1)
            (3031203, 0.125),   # BlueCloudBST(+1)
            (3031204, 0.10),    # BlueCloudCRT(+2)
            (3031206, 0.10),    # BlueCloudBST(+2)
            (3031205, 0.10),    # BlueCloudMIS(+2)
            (3031208, 0.0625),  # BlueCloudMIS(+3)
            (3031207, 0.0625),  # BlueCloudCRT(+3)
            (3031107, 0.05),    # S-TornadoCRT(+3)
            (3031109, 0.05),    # S-TornadoBST(+3)
            (3031108, 0.05),    # S-TornadoMIS(+3)
            (3031209, 0.05)     # BlueCloudBST(+3)
        ],

        BOX_SHOULDER: [
            (3060101, 0.20), # ShoulderGrdTD(+1)
            (3060104, 0.20), # ShoulderGrdGUN(+1)
            (3060107, 0.20), # ShoulderGrdTG(+1)
            (3060102, 0.14), # ShoulderGrdTD(+2)
            (3060105, 0.13), # ShoulderGrdGUN(+2)
            (3060108, 0.13)  # ShoulderGrdTG(+2)
        ],

        BOX_MINI_BOT: [
            (3011207, 0.10),    # BisliderCRT(+3)
            (3011204, 0.10),    # BisliderCRT(+2)
            (3011205, 0.10),    # BisliderMIS(+2)
            (3011206, 0.10),    # BisliderBST(+2)
            (3011209, 0.10),    # BisliderBST(+3)
            (3011208, 0.10),    # BisliderMIS(+3)
            (3011302, 0.075),   # TrilbiteMIS(+1)
            (3011301, 0.065),   # TrilbiteCRT(+1)
            (3011201, 0.065),   # BisliderCRT(+1)
            (3011203, 0.065),   # BisliderBST(+1)
            (3011202, 0.065),   # BisliderMIS(+1)
            (3011303, 0.065)    # TrilbiteBST(+1)
        ],

        BOX_HEAD: [
            (1010301, 0.60),  # StonehazardCRT(+1) — Seven-PearceMIS(+1) — ChestBusterSP(+1)
            (1010302, 0.30),  # StonehazardCRT(+2) — Seven-PearceMIS(+2) — ChestBusterSP(+2)
            (1010303, 0.10)   # StonehazardCRT(+3) — Seven-PearceMIS(+3) — ChestBusterSP(+3)
        ],

        BOX_BODY: [
            (1020301, 0.60),  # StonehazardTA(+1) — Seven-PearceBST(+1) — ChestBusterMX(+1)
            (1020302, 0.30),  # StonehazardTA(+2) — Seven-PearceBST(+2) — ChestBusterMX(+2)
            (1020303, 0.10)   # StonehazardTA(+3) — Seven-PearceBST(+3) — ChestBusterMX(+3)
        ],

        BOX_ARMS: [
            (1030301, 0.60),  # StonehazardTD(+1) — Seven-PearceGUN(+1) — ChestBusterTG(+1)
            (1030302, 0.30),  # StonehazardTD(+2) — Seven-PearceGUN(+2) — ChestBusterTG(+2)
            (1030303, 0.10)   # StonehazardTD(+3) — Seven-PearceGUN(+3) — ChestBusterTG(+3)
        ]
    },

    # [Lv18]Mine-Alderan2
    7: {
        BOX_GUN: [
            (3021203, 0.60), # smartGun(+3)
            (3021301, 0.30), # FableShooter(+1)
            (3021202, 0.10)  # smartGun(+2)
        ],

        BOX_SHIELD: [
            (3051101, 0.20), # AegisTD(+1)
            (3051104, 0.20), # AegisGUN(+1)
            (3051107, 0.20), # AegisTG(+1)
            (3051102, 0.10), # AegisTD(+2)
            (3051105, 0.10), # AegisGUN(+2)
            (3051108, 0.10), # AegisTG(+2)
            (3051103, 0.04), # AegisTD(+3)
            (3051106, 0.03), # AegisGUN(+3)
            (3051109, 0.03)  # AegisTG(+3)
        ],

        BOX_EF: [
            (3031204, 0.20),  # BlueCloudCRT(+2)
            (3031205, 0.20),  # BlueCloudMIS(+2)
            (3031206, 0.20),  # BlueCloudBST(+2)
            (3031201, 0.075), # BlueCloudCRT(+1)
            (3031202, 0.065), # BlueCloudMIS(+1)
            (3031203, 0.065), # BlueCloudBST(+1)
            (3031207, 0.065), # BlueCloudCRT(+3)
            (3031208, 0.065), # BlueCloudMIS(+3)
            (3031209, 0.065)  # BlueCloudBST(+3)
        ],

        BOX_SHOULDER: [
            (3060101, 0.20), # ShoulderGrdTD(+1)
            (3060104, 0.20), # ShoulderGrdGUN(+1)
            (3060107, 0.20), # ShoulderGrdTG(+1)
            (3060102, 0.10), # ShoulderGrdTD(+2)
            (3060105, 0.10), # ShoulderGrdGUN(+2)
            (3060108, 0.10), # ShoulderGrdTG(+2)
            (3060103, 0.04), # ShoulderGrdTD(+3)
            (3060106, 0.03), # ShoulderGrdGUN(+3)
            (3060109, 0.03)  # ShoulderGrdTG(+3)
        ],

        BOX_MINI_BOT: [
            (3011207, 0.20),    # BisliderCRT(+3)
            (3011208, 0.20),    # BisliderMIS(+3)
            (3011209, 0.20),    # BisliderBST(+3)
            (3011204, 0.075),   # BisliderCRT(+2)
            (3011205, 0.065),   # BisliderMIS(+2)
            (3011206, 0.065),   # BisliderBST(+2)
            (3011301, 0.065),   # TrilbiteCRT(+1)
            (3011302, 0.065),   # TrilbiteMIS(+1)
            (3011303, 0.065)    # TrilbiteBST(+1)
        ],

        BOX_HEAD: [
            (1010301, 0.60),  # StonehazardCRT(+1) — Seven-PearceMIS(+1) — ChestBusterSP(+1)
            (1010302, 0.30),  # StonehazardCRT(+2) — Seven-PearceMIS(+2) — ChestBusterSP(+2)
            (1010303, 0.10)   # StonehazardCRT(+3) — Seven-PearceMIS(+3) — ChestBusterSP(+3)
        ],

        BOX_BODY: [
            (1020301, 0.60),  # StonehazardTA(+1) — Seven-PearceBST(+1) — ChestBusterMX(+1)
            (1020302, 0.30),  # StonehazardTA(+2) — Seven-PearceBST(+2) — ChestBusterMX(+2)
            (1020303, 0.10)   # StonehazardTA(+3) — Seven-PearceBST(+3) — ChestBusterMX(+3)
        ],

        BOX_ARMS: [
            (1030301, 0.60),  # StonehazardTD(+1) — Seven-PearceGUN(+1) — ChestBusterTG(+1)
            (1030302, 0.30),  # StonehazardTD(+2) — Seven-PearceGUN(+2) — ChestBusterTG(+2)
            (1030303, 0.10)   # StonehazardTD(+3) — Seven-PearceGUN(+3) — ChestBusterTG(+3)
        ]
    },

    # [Lv20]Mine-Blaster
    8: {
        BOX_GUN: [
            (3021301, 0.70), # FableShooter(+1)
            (3021203, 0.30)  # smartGun(+3)
        ],

        BOX_SHIELD: [
            (3051101, 0.20), # AegisTD(+2)
            (3051105, 0.20), # AegisGUN(+2)
            (3051108, 0.20), # AegisTG(+2)
            (3051101, 0.08), # AegisTD(+1)
            (3051103, 0.06), # AegisTD(+3)
            (3051104, 0.07), # AegisGUN(+1)
            (3051106, 0.06), # AegisGUN(+3)
            (3051107, 0.07), # AegisTG(+1)
            (3051109, 0.06)  # AegisTG(+3)
        ],

        BOX_EF: [
            (3031207, 0.10),  # BlueCloudCRT(+3)
            (3031204, 0.10),  # BlueCloudCRT(+2)
            (3031205, 0.10),  # BlueCloudMIS(+2)
            (3031206, 0.10),  # BlueCloudBST(+2)
            (3031209, 0.10),  # BlueCloudBST(+3)
            (3031208, 0.10),  # BlueCloudMIS(+3)
            (3031302, 0.075),  # CirclerMIS(+1)
            (3031301, 0.065),  # CirclerCRT(+1)
            (3031201, 0.065),  # BlueCloudCRT(+1)
            (3031203, 0.065),  # BlueCloudBST(+1)
            (3031202, 0.065),  # BlueCloudMIS(+1)
            (3031303, 0.065)   # CirclerBST(+1)
        ],

        BOX_SHOULDER: [
            (3060102, 0.20), # ShoulderGrdTD(+2)
            (3060105, 0.20), # ShoulderGrdGUN(+2)
            (3060108, 0.20), # ShoulderGrdTG(+2)
            (3060101, 0.08), # ShoulderGrdTD(+1)
            (3060103, 0.06), # ShoulderGrdTD(+3)
            (3060104, 0.07), # ShoulderGrdGUN(+1)
            (3060106, 0.06), # ShoulderGrdGUN(+3)
            (3060107, 0.07), # ShoulderGrdTG(+1)
            (3060109, 0.06)  # ShoulderGrdTG(+3)
        ],

        BOX_MINI_BOT: [
            (3011301, 0.125), # TrilbiteCRT(+1)
            (3011303, 0.125), # TrilbiteBST(+1)
            (3011302, 0.125), # TrilbiteMIS(+1)
            (3011207, 0.10),  # BisliderCRT(+3)
            (3011208, 0.10),  # BisliderMIS(+3)
            (3011209, 0.10),  # BisliderBST(+3)
            (3011305, 0.0625),# TrilbiteMIS(+2)
            (3011304, 0.0625),# TrilbiteCRT(+2)
            (3011204, 0.05),  # BisliderCRT(+2)
            (3011206, 0.05),  # BisliderBST(+2)
            (3011205, 0.05),  # BisliderMIS(+2)
            (3011306, 0.05)   # TrilbiteBST(+2)
        ],

        BOX_HEAD: [
            (1010301, 0.60),  # StonehazardCRT(+1) — Seven-PearceMIS(+1) — ChestBusterSP(+1)
            (1010302, 0.30),  # StonehazardCRT(+2) — Seven-PearceMIS(+2) — ChestBusterSP(+2)
            (1010303, 0.10)   # StonehazardCRT(+3) — Seven-PearceMIS(+3) — ChestBusterSP(+3)
        ],

        BOX_BODY: [
            (1020301, 0.60),  # StonehazardTA(+1) — Seven-PearceBST(+1) — ChestBusterMX(+1)
            (1020302, 0.30),  # StonehazardTA(+2) — Seven-PearceBST(+2) — ChestBusterMX(+2)
            (1020303, 0.10)   # StonehazardTA(+3) — Seven-PearceBST(+3) — ChestBusterMX(+3)
        ],

        BOX_ARMS: [
            (1030301, 0.60),  # StonehazardTD(+1) — Seven-PearceGUN(+1) — ChestBusterTG(+1)
            (1030302, 0.30),  # StonehazardTD(+2) — Seven-PearceGUN(+2) — ChestBusterTG(+2)
            (1030303, 0.10)   # StonehazardTD(+3) — Seven-PearceGUN(+3) — ChestBusterTG(+3)
        ]
    },

    # [Lv23]Lava-Sea1
    9: {
        BOX_GUN: [
            (3021301, 0.40), # FableShooter(+1)
            (3021302, 0.30), # FableShooter(+2)
            (3021203, 0.15), # smartGun(+3)
            (3021401, 0.15)  # PaletteGun(+1)
        ],

        BOX_SHIELD: [
            (3051103, 0.20), # AegisTD(+2)
            (3051106, 0.20), # AegisGUN(+3)
            (3051109, 0.20), # AegisTG(+3)
            (3051102, 0.10), # AegisTD(+2)
            (3051105, 0.10), # AegisGUN(+2)
            (3051108, 0.10), # AegisTG(+2)
            (3050101, 0.04), # HonorshieldTD(+1)
            (3050104, 0.03), # HonorshieldGUN(+1)
            (3050107, 0.03)  # HonorshieldTG(+1)
        ],

        BOX_EF: [
            (3031207, 0.15), # BlueCloudCRT(+3)
            (3031208, 0.15), # BlueCloudMIS(+3)
            (3031209, 0.15), # BlueCloudBST(+3)
            (3031301, 0.15), # CirclerCRT(+1)
            (3031302, 0.15), # CirclerMIS(+1)
            (3031303, 0.15), # CirclerBST(+1)
            (3031204, 0.04), # BlueCloudCRT(+2)
            (3031205, 0.03), # BlueCloudMIS(+2)
            (3031206, 0.03)  # BlueCloudBST(+2)
        ],

        BOX_SHOULDER: [
            (3060103, 0.20), # ShoulderGrdTD(+3)
            (3060106, 0.20), # ShoulderGrdGUN(+3)
            (3060109, 0.20), # ShoulderGrdTG(+3)
            (3060102, 0.10), # ShoulderGrdTD(+2)
            (3060105, 0.10), # ShoulderGrdGUN(+2)
            (3060108, 0.10), # ShoulderGrdTG(+2)
            (3060201, 0.04), # HeavyShldrTD(+1)
            (3060204, 0.03), # HeavyShldrGUN(+1)
            (3060207, 0.03)  # HeavyShldrTG(+1)
        ],

        BOX_MINI_BOT: [
            (3011301, 0.15), # TrilbiteCRT(+1)
            (3011302, 0.15), # TrilbiteMIS(+1)
            (3011303, 0.15), # TrilbiteBST(+1)
            (3011304, 0.15), # TrilbiteCRT(+2)
            (3011305, 0.15), # TrilbiteMIS(+2)
            (3011306, 0.15), # TrilbiteBST(+2)
            (3011307, 0.04), # TrilbiteCRT(+3)
            (3011308, 0.03), # TrilbiteMIS(+3)
            (3011309, 0.03)  # TrilbiteBST(+3)
        ],

        BOX_HEAD: [
            (1010401, 0.60),  # CrashcannonCRT(+1) — CresentJetMIS(+1) — DuskrunnerSP(+1)
            (1010402, 0.30),  # CrashcannonCRT(+2) — CresentJetMIS(+2) — DuskrunnerSP(+2)
            (1010403, 0.10)   # CrashcannonCRT(+3) — CresentJetMIS(+3) — DuskrunnerSP(+3)
        ],

        BOX_BODY: [
            (1020401, 0.60),  # CrashcannonTA(+1) — CresentJetBST(+1) — DuskrunnerMX(+1)
            (1020402, 0.30),  # CrashcannonTA(+2) — CresentJetBST(+2) — DuskrunnerMX(+2)
            (1020403, 0.10)   # CrashcannonTA(+3) — CresentJetBST(+3) — DuskrunnerMX(+3)
        ],

        BOX_ARMS: [
            (1030401, 0.60),  # CrashcannonTD(+1) — CresentJetGUN(+1) — DuskrunnerTG(+1)
            (1030402, 0.30),  # CrashcannonTD(+2) — CresentJetGUN(+2) — DuskrunnerTG(+2)
            (1030403, 0.10)   # CrashcannonTD(+3) — CresentJetGUN(+3) — DuskrunnerTG(+3)
        ]
    },

     # [Lv26]Lava-Sea2
    10: {
        BOX_GUN: [
            (3021302, 0.50), # FableShooter(+2)
            (3021401, 0.30), # PaletteGun(+1)
            (3021301, 0.10), # FableShooter(+1)
            (3021303, 0.10)  # FableShooter(+3)
        ],

        BOX_SHIELD: [
            (3051103, 0.20), # HonorshieldTD(+1)
            (3051103, 0.20), # HonorshieldGUN(+1)
            (3051103, 0.20), # HonorshieldTG(+1)
            (3051103, 0.10), # AegisTD(+3)
            (3051103, 0.10), # AegisGUN(+3)
            (3051103, 0.10), # AegisTG(+3)
            (3051103, 0.04), # HonorshieldTD(+2)
            (3051103, 0.03), # HonorshieldGUN(+2)
            (3051103, 0.03)  # HonorshieldTG(+2)
        ],

        BOX_EF: [
            (3031301, 0.125),   # CirclerCRT(+1)
            (3031302, 0.125),   # CirclerMIS(+1)
            (3031303, 0.125),   # CirclerBST(+1)
            (3031304, 0.10),    # CirclerCRT(+2)
            (3031306, 0.10),    # CirclerBST(+2)
            (3031305, 0.10),    # CirclerMIS(+2)
            (3031308, 0.0625),  # CirclerMIS(+3)
            (3031307, 0.0625),  # CirclerCRT(+3)
            (3031207, 0.05),    # BlueCloudCRT(+3)
            (3031209, 0.05),    # BlueCloudBST(+3)
            (3031208, 0.05),    # BlueCloudMIS(+3)
            (3031309, 0.05)     # CirclerBST(+3)
        ],

        BOX_SHOULDER: [
            (3060201, 0.20), # HeavyShldrTD(+1)
            (3060204, 0.20), # HeavyShldrGUN(+1)
            (3060207, 0.20), # HeavyShldrTG(+1)
            (3060103, 0.10), # ShoulderGrdTD(+3)
            (3060106, 0.10), # ShoulderGrdGUN(+3)
            (3060109, 0.10), # ShoulderGrdTG(+3)
            (3060202, 0.04), # HeavyShldrTD(+2)
            (3060205, 0.03), # HeavyShldrGUN(+2)
            (3060208, 0.03)  # HeavyShldrTG(+2)
        ],

        BOX_MINI_BOT: [
            (3011307, 0.10),    # TrilbiteCRT(+3)
            (3011304, 0.10),    # TrilbiteCRT(+2)
            (3011305, 0.10),    # TrilbiteMIS(+2)
            (3011306, 0.10),    # TrilbiteBST(+2)
            (3011309, 0.10),    # TrilbiteBST(+3)
            (3011308, 0.10),    # TrilbiteMIS(+3)
            (3011402, 0.075),   # MinisatMIS(+1)
            (3011401, 0.065),   # MinisatCRT(+1)
            (3011301, 0.065),   # TrilbiteCRT(+1)
            (3011303, 0.065),   # TrilbiteBST(+1)
            (3011302, 0.065),   # TrilbiteMIS(+1)
            (3011403, 0.065)    # MinisatBST(+1)
        ],

        BOX_HEAD: [
            (1010401, 0.60),  # CrashcannonCRT(+1) — CresentJetMIS(+1) — DuskrunnerSP(+1)
            (1010402, 0.30),  # CrashcannonCRT(+2) — CresentJetMIS(+2) — DuskrunnerSP(+2)
            (1010403, 0.10)   # CrashcannonCRT(+3) — CresentJetMIS(+3) — DuskrunnerSP(+3)
        ],

        BOX_BODY: [
            (1020401, 0.60),  # CrashcannonTA(+1) — CresentJetBST(+1) — DuskrunnerMX(+1)
            (1020402, 0.30),  # CrashcannonTA(+2) — CresentJetBST(+2) — DuskrunnerMX(+2)
            (1020403, 0.10)   # CrashcannonTA(+3) — CresentJetBST(+3) — DuskrunnerMX(+3)
        ],

        BOX_ARMS: [
            (1030401, 0.60),  # CrashcannonTD(+1) — CresentJetGUN(+1) — DuskrunnerTG(+1)
            (1030402, 0.30),  # CrashcannonTD(+2) — CresentJetGUN(+2) — DuskrunnerTG(+2)
            (1030403, 0.10)   # CrashcannonTD(+3) — CresentJetGUN(+3) — DuskrunnerTG(+3)
        ]
    },

    # [Lv28]Lava-Sea3
    11: {
        BOX_GUN: [
            (3021401, 0.50), # PaletteGun(+1)
            (3021302, 0.20), # FableShooter(+2)
            (3021303, 0.20), # FableShooter(+3)
            (3021402, 0.10)  # PaletteGun(+2)
        ],

        BOX_SHIELD: [
            (3050104, 0.15), # HonorshieldGUN(+1)
            (3050101, 0.15), # HonorshieldTG(+1)
            (3050107, 0.15), # HonorshieldTD(+1)
            (3050108, 0.10), # HonorshieldTG(+2)
            (3050102, 0.10), # HonorshieldTD(+2)
            (3050105, 0.10), # HonorshieldGUN(+2)
            (3050106, 0.05), # HonorshieldGUN(+3)
            (3051103, 0.04), # AegisTD(+3)
            (3050103, 0.04), # HonorshieldTD(+3)
            (3051109, 0.04), # AegisTG(+3)
            (3051106, 0.04), # AegisGUN(+3)
            (3050109, 0.04)  # HonorshieldTG(+3)
        ],

        BOX_EF: [
            (3031304, 0.20), # CirclerCRT(+2)
            (3031305, 0.20), # CirclerMIS(+2)
            (3031306, 0.20), # CirclerBST(+2)
            (3031301, 0.075), # CirclerCRT(+1)
            (3031302, 0.075), # CirclerMIS(+1)
            (3031303, 0.075), # CirclerBST(+1)
            (3031307, 0.075), # CirclerCRT(+3)
            (3031308, 0.075), # CirclerMIS(+3)
            (3031309, 0.075)  # CirclerBST(+3)
        ],

        BOX_SHOULDER: [
            (3060204, 0.15), # HeavyShldrGUN(+1)
            (3060207, 0.15), # HeavyShldrTG(+1)
            (3060201, 0.15), # HeavyShldrTD(+1)
            (3060208, 0.10), # HeavyShldrTG(+2)
            (3060202, 0.10), # HeavyShldrTD(+2)
            (3060205, 0.10), # HeavyShldrGUN(+2)
            (3060206, 0.05), # HeavyShldrGUN(+3)
            (3060103, 0.04), # ShoulderGrdTD(+3)
            (3060203, 0.04), # HeavyShldrTD(+3)
            (3060109, 0.04), # ShoulderGrdTG(+3)
            (3060106, 0.04), # ShoulderGrdGUN(+3)
            (3060209, 0.04)  # HeavyShldrTG(+3)
        ],

        BOX_MINI_BOT: [
            (3011307, 0.20),    # TrilbiteCRT(+3)
            (3011308, 0.20),    # TrilbiteMIS(+3)
            (3011309, 0.20),    # TrilbiteBST(+3)
            (3011304, 0.075),   # TrilbiteCRT(+2)
            (3011305, 0.065),   # TrilbiteMIS(+2)
            (3011306, 0.065),   # TrilbiteBST(+2)
            (3011401, 0.065),   # MinisatCRT(+1)
            (3011402, 0.065),   # MinisatMIS(+1)
            (3011403, 0.065)    # MinisatBST(+1)
        ],

        BOX_HEAD: [
            (1010401, 0.60),  # CrashcannonCRT(+1) — CresentJetMIS(+1) — DuskrunnerSP(+1)
            (1010402, 0.30),  # CrashcannonCRT(+2) — CresentJetMIS(+2) — DuskrunnerSP(+2)
            (1010403, 0.10)   # CrashcannonCRT(+3) — CresentJetMIS(+3) — DuskrunnerSP(+3)
        ],

        BOX_BODY: [
            (1020401, 0.60),  # CrashcannonTA(+1) — CresentJetBST(+1) — DuskrunnerMX(+1)
            (1020402, 0.30),  # CrashcannonTA(+2) — CresentJetBST(+2) — DuskrunnerMX(+2)
            (1020403, 0.10)   # CrashcannonTA(+3) — CresentJetBST(+3) — DuskrunnerMX(+3)
        ],

        BOX_ARMS: [
            (1030401, 0.60),  # CrashcannonTD(+1) — CresentJetGUN(+1) — DuskrunnerTG(+1)
            (1030402, 0.30),  # CrashcannonTD(+2) — CresentJetGUN(+2) — DuskrunnerTG(+2)
            (1030403, 0.10)   # CrashcannonTD(+3) — CresentJetGUN(+3) — DuskrunnerTG(+3)
        ]
    },

    # [Lv30]Acurin-Ruins1
    12: {
        BOX_GUN: [
            (3021303, 0.40), # FableShooter(+3)
            (3021401, 0.30), # PaletteGun(+1)
            (3021402, 0.20), # PaletteGun(+2)
            (3021302, 0.10)  # FableShooter(+2)
        ],

        BOX_SHIELD: [
            (3050102, 0.20), # HonorshieldTD(+2)
            (3050105, 0.20), # HonorshieldGUN(+2)
            (3050108, 0.20), # HonorshieldTG(+2)
            (3050101, 0.08), # HonorshieldTD(+1)
            (3050103, 0.06), # HonorshieldTD(+3)
            (3050104, 0.07), # HonorshieldGUN(+1)
            (3050106, 0.06), # HonorshieldGUN(+3)
            (3050107, 0.07), # HonorshieldTG(+1)
            (3050109, 0.06)  # HonorshieldTG(+3)
        ],

        BOX_EF: [
            (3031307, 0.10), # CirclerCRT(+3)
            (3031304, 0.10), # CirclerCRT(+2)
            (3031305, 0.10), # CirclerMIS(+2)
            (3031306, 0.10), # CirclerBST(+2)
            (3031309, 0.10), # CirclerBST(+3)
            (3031308, 0.10), # CirclerMIS(+3)
            (3031402, 0.075), # T-BeaconMIS(+1)
            (3031401, 0.065), # T-BeaconCRT(+1)
            (3031301, 0.065), # CirclerCRT(+1)
            (3031303, 0.065), # CirclerBST(+1)
            (3031302, 0.065), # CirclerMIS(+1)
            (3031403, 0.065)  # T-BeaconBST(+1)
        ],

        BOX_SHOULDER: [
            (3060202, 0.20), # HeavyShldrTD(+2)
            (3060205, 0.20), # HeavyShldrGUN(+2)
            (3060208, 0.20), # HeavyShldrTG(+2)
            (3060201, 0.08), # HeavyShldrTD(+1)
            (3060203, 0.06), # HeavyShldrTD(+3)
            (3060204, 0.07), # HeavyShldrGUN(+1)
            (3060206, 0.06), # HeavyShldrGUN(+3)
            (3060207, 0.07), # HeavyShldrTG(+1)
            (3060209, 0.06)  # HeavyShldrTG(+3)
        ],

        BOX_MINI_BOT: [
            (3011401, 0.125), # MinisatCRT(+1)
            (3011403, 0.125), # MinisatBST(+1)
            (3011402, 0.125), # MinisatMIS(+1)
            (3011307, 0.10),  # TrilbiteCRT(+3)
            (3011308, 0.10),  # TrilbiteMIS(+3)
            (3011309, 0.10),  # TrilbiteBST(+3)
            (3011405, 0.0625),# MinisatMIS(+2)
            (3011404, 0.0625),# MinisatCRT(+2)
            (3011304, 0.05),  # TrilbiteCRT(+2)
            (3011306, 0.05),  # TrilbiteBST(+2)
            (3011305, 0.05),  # TrilbiteMIS(+2)
            (3011406, 0.05)   # MinisatBST(+2)
        ],

        BOX_HEAD: [
            (1010401, 0.60),  # CrashcannonCRT(+1) — CresentJetMIS(+1) — DuskrunnerSP(+1)
            (1010402, 0.30),  # CrashcannonCRT(+2) — CresentJetMIS(+2) — DuskrunnerSP(+2)
            (1010403, 0.10)   # CrashcannonCRT(+3) — CresentJetMIS(+3) — DuskrunnerSP(+3)
        ],

        BOX_BODY: [
            (1020401, 0.60),  # CrashcannonTA(+1) — CresentJetBST(+1) — DuskrunnerMX(+1)
            (1020402, 0.30),  # CrashcannonTA(+2) — CresentJetBST(+2) — DuskrunnerMX(+2)
            (1020403, 0.10)   # CrashcannonTA(+3) — CresentJetBST(+3) — DuskrunnerMX(+3)
        ],

        BOX_ARMS: [
            (1030401, 0.60),  # CrashcannonTD(+1) — CresentJetGUN(+1) — DuskrunnerTG(+1)
            (1030402, 0.30),  # CrashcannonTD(+2) — CresentJetGUN(+2) — DuskrunnerTG(+2)
            (1030403, 0.10)   # CrashcannonTD(+3) — CresentJetGUN(+3) — DuskrunnerTG(+3)
        ]
    },

    # [Lv33]Acurin-Ruins2
    13: {
        BOX_GUN: [
            (3021402, 0.40), # PaletteGun(+2)
            (3021303, 0.30), # FableShooter(+3)
            (3021401, 0.15), # PaletteGun(+1)
            (3021403, 0.15)  # PaletteGun(+3)
        ],

        BOX_SHIELD: [
            (3050103, 0.20), # HonorshieldTD(+3)
            (3050106, 0.20), # HonorshieldGUN(+3)
            (3050109, 0.20), # HonorshieldTG(+3)
            (3050102, 0.10), # HonorshieldTD(+2)
            (3050105, 0.10), # HonorshieldGUN(+2)
            (3050108, 0.10), # HonorshieldTG(+2)
            (3050201, 0.04), # BucklerShldTD(+1)
            (3050204, 0.03), # BucklerShldGUN(+1)
            (3050207, 0.03)  # BucklerShldTG(+1)
        ],

        BOX_EF: [
            (3031307, 0.15), # CirclerCRT(+3)
            (3031308, 0.15), # CirclerMIS(+3)
            (3031309, 0.15), # CirclerBST(+3)
            (3031401, 0.15), # T-BeaconCRT(+1)
            (3031402, 0.15), # T-BeaconMIS(+1)
            (3031403, 0.15), # T-BeaconBST(+1)
            (3031304, 0.04), # CirclerCRT(+2)
            (3031305, 0.03), # CirclerMIS(+2)
            (3031306, 0.03)  # CirclerBST(+2)
        ],

        BOX_SHOULDER: [
            (3060203, 0.20), # HeavyShldrTD(+3)
            (3060206, 0.20), # HeavyShldrGUN(+3)
            (3060209, 0.20), # HeavyShldrTG(+3)
            (3060202, 0.10), # HeavyShldrTD(+2)
            (3060205, 0.10), # HeavyShldrGUN(+2)
            (3060208, 0.10), # HeavyShldrTG(+2)
            (3060301, 0.04), # SoftShldrTD(+1)
            (3060304, 0.03), # SoftShldrGUN(+1)
            (3060307, 0.03)  # SoftShldrTG(+1)
        ],

        BOX_MINI_BOT: [
            (3011401, 0.15), # MinisatCRT(+1)
            (3011402, 0.15), # MinisatMIS(+1)
            (3011403, 0.15), # MinisatBST(+1)
            (3011404, 0.15), # MinisatCRT(+2)
            (3011405, 0.15), # MinisatMIS(+2)
            (3011406, 0.15), # MinisatBST(+2)
            (3011407, 0.04), # MinisatCRT(+3)
            (3011408, 0.03), # MinisatMIS(+3)
            (3011409, 0.03)  # MinisatBST(+3)
        ],

        BOX_HEAD: [
            (1010501, 0.60),  # LycaonLaunchCRT(+1) — BladeShooterMIS(+1) — SticleSP(+1)
            (1010502, 0.30),  # LycaonLaunchCRT(+2) — BladeShooterMIS(+2) — SticleSP(+2)
            (1010503, 0.10)   # LycaonLaunchCRT(+3) — BladeShooterMIS(+3) — SticleSP(+3)
        ],

        BOX_BODY: [
            (1020501, 0.60),  # LycaonLaunchTA(+1) — BladeShooterBST(+1) — SticleMX(+1)
            (1020502, 0.30),  # LycaonLaunchTA(+2) — BladeShooterBST(+2) — SticleMX(+2)
            (1020503, 0.10)   # LycaonLaunchTA(+3) — BladeShooterBST(+3) — SticleMX(+3)
        ],

        BOX_ARMS: [
            (1030501, 0.60),  # LycaonLaunchTD(+1) — BladeShooterGUN(+1) — SticleTG(+1)
            (1030502, 0.30),  # LycaonLaunchTD(+2) — BladeShooterGUN(+2) — SticleTG(+2)
            (1030503, 0.10)   # LycaonLaunchTD(+3) — BladeShooterGUN(+3) — SticleTG(+3)
        ]
    },

    # [Lv36]Planet-Acurin
    14: {
        BOX_GUN: [
            (3021403, 0.40), # PaletteGun(+3)
            (3021402, 0.30), # PaletteGun(+2)
            (3021303, 0.15), # FableShooter(+3)
            (3021501, 0.15)  # LightningGun(+1)
        ],

        BOX_SHIELD: [
            (3050201, 0.20), # BucklerShldTD(+1)
            (3050204, 0.20), # BucklerShldGUN(+1)
            (3050207, 0.20), # BucklerShldTG(+1)
            (3050103, 0.10), # HonorshieldTD(+3)
            (3050106, 0.10), # HonorshieldGUN(+3)
            (3050109, 0.10), # HonorshieldTG(+3)
            (3050202, 0.04), # BucklerShldTD(+2)
            (3050205, 0.03), # BucklerShldGUN(+2)
            (3050208, 0.03)  # BucklerShldTG(+2)
        ],

        BOX_EF: [
            (3031401, 0.125),   # T-BeaconCRT(+1)
            (3031402, 0.125),   # T-BeaconMIS(+1)
            (3031403, 0.125),   # T-BeaconBST(+1)
            (3031404, 0.10),    # T-BeaconCRT(+2)
            (3031406, 0.10),    # T-BeaconBST(+2)
            (3031405, 0.10),    # T-BeaconMIS(+2)
            (3031408, 0.0625),  # T-BeaconMIS(+3)
            (3031407, 0.0625),  # T-BeaconCRT(+3)
            (3031307, 0.05),    # CirclerCRT(+3)
            (3031309, 0.05),    # CirclerBST(+3)
            (3031308, 0.05),    # CirclerMIS(+3)
            (3031409, 0.05)     # T-BeaconBST(+3)
        ],

        BOX_SHOULDER: [
            (3060301, 0.20), # SoftShldrTD(+1)
            (3060304, 0.20), # SoftShldrGUN(+1)
            (3060307, 0.20), # SoftShldrTG(+1)
            (3060203, 0.10), # HeavyShldrTD(+3)
            (3060206, 0.10), # HeavyShldrGUN(+3)
            (3060209, 0.10), # HeavyShldrTG(+3)
            (3060302, 0.04), # SoftShldrTD(+2)
            (3060305, 0.03), # SoftShldrGUN(+2)
            (3060308, 0.03)  # SoftShldrTG(+2)
        ],

        BOX_MINI_BOT: [
            (3011407, 0.10),    # MinisatCRT(+3)
            (3011404, 0.10),    # MinisatCRT(+2)
            (3011405, 0.10),    # MinisatMIS(+2)
            (3011406, 0.10),    # MinisatBST(+2)
            (3011409, 0.10),    # MinisatBST(+3)
            (3011408, 0.10),    # MinisatMIS(+3)
            (3011502, 0.075),   # BabytankMIS(+1)
            (3011501, 0.065),   # BabytankCRT(+1)
            (3011401, 0.065),   # MinisatCRT(+1)
            (3011403, 0.065),   # MinisatBST(+1)
            (3011402, 0.065),   # MinisatMIS(+1)
            (3011503, 0.065)    # BabytankBST(+1)
        ],

        BOX_HEAD: [
            (1010501, 0.60),  # LycaonLaunchCRT(+1) — BladeShooterMIS(+1) — SticleSP(+1)
            (1010502, 0.30),  # LycaonLaunchCRT(+2) — BladeShooterMIS(+2) — SticleSP(+2)
            (1010503, 0.10)   # LycaonLaunchCRT(+3) — BladeShooterMIS(+3) — SticleSP(+3)
        ],

        BOX_BODY: [
            (1020501, 0.60),  # LycaonLaunchTA(+1) — BladeShooterBST(+1) — SticleMX(+1)
            (1020502, 0.30),  # LycaonLaunchTA(+2) — BladeShooterBST(+2) — SticleMX(+2)
            (1020503, 0.10)   # LycaonLaunchTA(+3) — BladeShooterBST(+3) — SticleMX(+3)
        ],

        BOX_ARMS: [
            (1030501, 0.60),  # LycaonLaunchTD(+1) — BladeShooterGUN(+1) — SticleTG(+1)
            (1030502, 0.30),  # LycaonLaunchTD(+2) — BladeShooterGUN(+2) — SticleTG(+2)
            (1030503, 0.10)   # LycaonLaunchTD(+3) — BladeShooterGUN(+3) — SticleTG(+3)
        ]
    },

    # [Lv38]Planet-Acurin2
    15: {
        BOX_GUN: [
            (3021403, 0.60), # PaletteGun(+3)
            (3021501, 0.30), # LightningGun(+1)
            (3021402, 0.10)  # PaletteGun(+2)
        ],

        BOX_SHIELD: [
            (3050204, 0.15), # BucklerShldGUN(+1)
            (3050207, 0.15), # BucklerShldTG(+1)
            (3050201, 0.15), # BucklerShldTD(+1)
            (3050208, 0.10), # BucklerShldTG(+2)
            (3050202, 0.10), # BucklerShldTD(+2)
            (3050205, 0.10), # BucklerShldGUN(+2)
            (3050206, 0.05), # BucklerShldGUN(+3)
            (3050103, 0.04), # HonorshieldTD(+3)
            (3050203, 0.04), # BucklerShldTD(+3)
            (3050109, 0.04), # HonorshieldTG(+3)
            (3050106, 0.04), # HonorshieldGUN(+3)
            (3050209, 0.04)  # BucklerShldTG(+3)
        ],

        BOX_EF: [
            (3031404, 0.20),    # T-BeaconCRT(+2)
            (3031405, 0.20),    # T-BeaconMIS(+2)
            (3031406, 0.20),    # T-BeaconBST(+2)
            (3031401, 0.075),   # T-BeaconCRT(+1)
            (3031402, 0.075),   # T-BeaconMIS(+1)
            (3031403, 0.075),   # T-BeaconBST(+1)
            (3031407, 0.075),   # T-BeaconCRT(+3)
            (3031408, 0.075),   # T-BeaconMIS(+3)
            (3031409, 0.075)    # T-BeaconBST(+3)
        ],

        BOX_SHOULDER: [
            (3060304, 0.15), # SoftShldrGUN(+1)
            (3060307, 0.15), # SoftShldrTG(+1)
            (3060301, 0.15), # SoftShldrTD(+1)
            (3060308, 0.10), # SoftShldrTG(+2)
            (3060302, 0.10), # SoftShldrTD(+2)
            (3060305, 0.10), # SoftShldrGUN(+2)
            (3060306, 0.05), # SoftShldrGUN(+3)
            (3060203, 0.04), # HeavyShldrTD(+3)
            (3060303, 0.04), # SoftShldrTD(+3)
            (3060209, 0.04), # HeavyShldrTG(+3)
            (3060206, 0.04), # HeavyShldrGUN(+3)
            (3060309, 0.04)  # SoftShldrTG(+3)
        ],

        BOX_MINI_BOT: [
            (3011407, 0.20),    # MinisatCRT(+3)
            (3011408, 0.20),    # MinisatMIS(+3)
            (3011409, 0.20),    # MinisatBST(+3)
            (3011404, 0.075),   # MinisatCRT(+2)
            (3011405, 0.065),   # MinisatMIS(+2)
            (3011406, 0.065),   # MinisatBST(+2)
            (3011501, 0.065),   # BabytankCRT(+1)
            (3011502, 0.065),   # BabytankMIS(+1)
            (3011503, 0.065)    # BabytankBST(+1)
        ],

        BOX_HEAD: [
            (1010501, 0.60),  # LycaonLaunchCRT(+1) — BladeShooterMIS(+1) — SticleSP(+1)
            (1010502, 0.30),  # LycaonLaunchCRT(+2) — BladeShooterMIS(+2) — SticleSP(+2)
            (1010503, 0.10)   # LycaonLaunchCRT(+3) — BladeShooterMIS(+3) — SticleSP(+3)
        ],

        BOX_BODY: [
            (1020501, 0.60),  # LycaonLaunchTA(+1) — BladeShooterBST(+1) — SticleMX(+1)
            (1020502, 0.30),  # LycaonLaunchTA(+2) — BladeShooterBST(+2) — SticleMX(+2)
            (1020503, 0.10)   # LycaonLaunchTA(+3) — BladeShooterBST(+3) — SticleMX(+3)
        ],

        BOX_ARMS: [
            (1030501, 0.60),  # LycaonLaunchTD(+1) — BladeShooterGUN(+1) — SticleTG(+1)
            (1030502, 0.30),  # LycaonLaunchTD(+2) — BladeShooterGUN(+2) — SticleTG(+2)
            (1030503, 0.10)   # LycaonLaunchTD(+3) — BladeShooterGUN(+3) — SticleTG(+3)
        ]
    },

    # [Lv40]Port-Acurin
    16: {
        BOX_GUN: [
            (3021501, 0.60), # LightningGun(+1)
            (3021403, 0.40)  # PaletteGun(+3)
        ],

        BOX_SHIELD: [
            (3050202, 0.20), # BucklerShldTD(+2)
            (3050205, 0.20), # BucklerShldGUN(+2)
            (3050208, 0.20), # BucklerShldTG(+2)
            (3050201, 0.08), # BucklerShldTD(+1)
            (3050203, 0.06), # BucklerShldTD(+3)
            (3050204, 0.07), # BucklerShldGUN(+1)
            (3050206, 0.06), # BucklerShldGUN(+3)
            (3050207, 0.07), # BucklerShldTG(+1)
            (3050209, 0.06)  # BucklerShldTG(+3)
        ],

        BOX_EF: [
            (3031407, 0.10),    # T-BeaconCRT(+3)
            (3031404, 0.10),    # T-BeaconCRT(+2)
            (3031405, 0.10),    # T-BeaconMIS(+2)
            (3031406, 0.10),    # T-BeaconBST(+2)
            (3031409, 0.10),    # T-BeaconBST(+3)
            (3031408, 0.10),    # T-BeaconMIS(+3)
            (3031502, 0.075),   # SoundEnergyMIS(+1)
            (3031501, 0.065),   # SoundEnergyCRT(+1)
            (3031401, 0.065),   # T-BeaconCRT(+1)
            (3031403, 0.065),   # T-BeaconBST(+1)
            (3031402, 0.065),   # T-BeaconMIS(+1)
            (3031503, 0.065)    # SoundEnergyBST(+1)
        ],

        BOX_SHOULDER: [
            (3060302, 0.20), # SoftShldrTD(+2)
            (3060305, 0.20), # SoftShldrGUN(+2)
            (3060308, 0.20), # SoftShldrTG(+2)
            (3060301, 0.08), # SoftShldrTD(+1)
            (3060303, 0.06), # SoftShldrTD(+3)
            (3060304, 0.07), # SoftShldrGUN(+1)
            (3060306, 0.06), # SoftShldrGUN(+3)
            (3060307, 0.07), # SoftShldrTG(+1)
            (3060309, 0.06)  # SoftShldrTG(+3)
        ],

        BOX_MINI_BOT: [
            (3011501, 0.125), # BabytankCRT(+1)
            (3011503, 0.125), # BabytankBST(+1)
            (3011502, 0.125), # BabytankMIS(+1)
            (3011407, 0.10),  # MinisatCRT(+3)
            (3011408, 0.10),  # MinisatMIS(+3)
            (3011409, 0.10),  # MinisatBST(+3)
            (3011505, 0.0625),# BabytankMIS(+2)
            (3011504, 0.0625),# BabytankCRT(+2)
            (3011404, 0.05),  # MinisatCRT(+2)
            (3011406, 0.05),  # MinisatBST(+2)
            (3011405, 0.05),  # MinisatMIS(+2)
            (3011506, 0.05)   # BabytankBST(+2)
        ],

        BOX_HEAD: [
            (1010501, 0.60),  # LycaonLaunchCRT(+1) — BladeShooterMIS(+1) — SticleSP(+1)
            (1010502, 0.30),  # LycaonLaunchCRT(+2) — BladeShooterMIS(+2) — SticleSP(+2)
            (1010503, 0.10)   # LycaonLaunchCRT(+3) — BladeShooterMIS(+3) — SticleSP(+3)
        ],

        BOX_BODY: [
            (1020501, 0.60),  # LycaonLaunchTA(+1) — BladeShooterBST(+1) — SticleMX(+1)
            (1020502, 0.30),  # LycaonLaunchTA(+2) — BladeShooterBST(+2) — SticleMX(+2)
            (1020503, 0.10)   # LycaonLaunchTA(+3) — BladeShooterBST(+3) — SticleMX(+3)
        ],

        BOX_ARMS: [
            (1030501, 0.60),  # LycaonLaunchTD(+1) — BladeShooterGUN(+1) — SticleTG(+1)
            (1030502, 0.30),  # LycaonLaunchTD(+2) — BladeShooterGUN(+2) — SticleTG(+2)
            (1030503, 0.10)   # LycaonLaunchTD(+3) — BladeShooterGUN(+3) — SticleTG(+3)
        ]
    },

    # [Lv43]Escape-Acurin
    17: {
        BOX_GUN: [
            (3021501, 0.40), # LightningGun(+1)
            (3021502, 0.30), # LightningGun(+2)
            (3021403, 0.15), # PaletteGun(+3)
            (3021601, 0.15)  # WhiteBlazer(+1)
        ],

        BOX_SHIELD: [
            (3050203, 0.20), # BucklerShldTD(+3)
            (3050206, 0.20), # BucklerShldGUN(+3)
            (3050209, 0.20), # BucklerShldTG(+3)
            (3050202, 0.10), # BucklerShldTD(+2)
            (3050205, 0.10), # BucklerShldGUN(+2)
            (3050208, 0.10), # BucklerShldTG(+2)
            (3050301, 0.04), # HeavyshieldTD(+1)
            (3050304, 0.03), # HeavyshieldGUN(+1)
            (3050307, 0.03)  # HeavyshieldTG(+1)
        ],

        BOX_EF: [
            (3031407, 0.15),  # T-BeaconCRT(+3)
            (3031408, 0.15),  # T-BeaconMIS(+3)
            (3031409, 0.15),  # T-BeaconBST(+3)
            (3031501, 0.15),  # SoundEnergyCRT(+1)
            (3031502, 0.15),  # SoundEnergyMIS(+1)
            (3031503, 0.15),  # SoundEnergyBST(+1)
            (3031404, 0.04),  # T-BeaconCRT(+2)
            (3031405, 0.03),  # T-BeaconMIS(+2)
            (3031406, 0.03)   # T-BeaconBST(+2)
        ],

        BOX_SHOULDER: [
            (3060303, 0.20), # SoftShldrTD(+3)
            (3060306, 0.20), # SoftShldrGUN(+3)
            (3060309, 0.20), # SoftShldrTG(+3)
            (3060302, 0.10), # SoftShldrTD(+2)
            (3060305, 0.10), # SoftShldrGUN(+2)
            (3060308, 0.10), # SoftShldrTG(+2)
            (3060401, 0.04), # BlockShldrTD(+1)
            (3060404, 0.03), # BlockShldrGUN(+1)
            (3060407, 0.03)  # BlockShldrTG(+1)
        ],

        BOX_MINI_BOT: [
            (3011501, 0.15), # BabytankCRT(+1)
            (3011502, 0.15), # BabytankMIS(+1)
            (3011503, 0.15), # BabytankBST(+1)
            (3011504, 0.15), # BabytankCRT(+2)
            (3011505, 0.15), # BabytankMIS(+2)
            (3011506, 0.15), # BabytankBST(+2)
            (3011507, 0.04), # BabytankCRT(+3)
            (3011508, 0.03), # BabytankMIS(+3)
            (3011509, 0.03)  # BabytankBST(+3)
        ],

        BOX_HEAD: [
            (1010601, 0.60),  # HyperDrillCRT(+1) — LandsliderMIS(+1) — SpikeHazardSP(+1)
            (1010602, 0.30),  # HyperDrillCRT(+2) — LandsliderMIS(+2) — SpikeHazardSP(+2)
            (1010603, 0.10)   # HyperDrillCRT(+3) — LandsliderMIS(+3) — SpikeHazardSP(+3)
        ],

        BOX_BODY: [
            (1020601, 0.60),  # HyperDrillTA(+1) — LandsliderBST(+1) — SpikeHazardMX(+1)
            (1020602, 0.30),  # HyperDrillTA(+2) — LandsliderBST(+2) — SpikeHazardMX(+2)
            (1020603, 0.10)   # HyperDrillTA(+3) — LandsliderBST(+3) — SpikeHazardMX(+3)
        ],

        BOX_ARMS: [
            (1030601, 0.60),  # HyperDrillTD(+1) — LandsliderGUN(+1) — SpikeHazardTG(+1)
            (1030602, 0.30),  # HyperDrillTD(+2) — LandsliderGUN(+2) — SpikeHazardTG(+2)
            (1030603, 0.10)   # HyperDrillTD(+3) — LandsliderGUN(+3) — SpikeHazardTG(+3)
        ]
    },

    # [Lv46]Planet-MECA
    18: {
        BOX_GUN: [
            (3021502, 0.40), # LightningGun(+2)
            (3021601, 0.30), # WhiteBlazer(+1)
            (3021501, 0.15), # LightningGun(+1)
            (3021503, 0.15)  # LightningGun(+3)
        ],

        BOX_SHIELD: [
            (3050304, 0.20),  # HeavyshieldTD(+1)
            (3050301, 0.20),  # HeavyshieldGUN(+1)
            (3050307, 0.20),  # HeavyshieldTG(+1)
            (3050203, 0.10),  # BucklerShldTD(+3)
            (3050206, 0.10),  # BucklerShldGUN(+3)
            (3050209, 0.10),  # BucklerShldTG(+3)
            (3050302, 0.04),  # HeavyshieldTD(+2)
            (3050305, 0.03),  # HeavyshieldGUN(+2)
            (3050308, 0.03)   # HeavyshieldTG(+2)
        ],

        BOX_EF: [
            (3031501, 0.125),   # SoundEnergyCRT(+1)
            (3031502, 0.125),   # SoundEnergyMIS(+1)
            (3031503, 0.125),   # SoundEnergyBST(+1)
            (3031504, 0.10),    # SoundEnergyCRT(+2)
            (3031506, 0.10),    # SoundEnergyBST(+2)
            (3031505, 0.10),    # SoundEnergyMIS(+2)
            (3031508, 0.0625),  # SoundEnergyMIS(+3)
            (3031507, 0.0625),  # SoundEnergyCRT(+3)
            (3031407, 0.05),    # T-BeaconCRT(+3)
            (3031409, 0.05),    # T-BeaconBST(+3)
            (3031408, 0.05),    # T-BeaconMIS(+3)
            (3031509, 0.05)     # SoundEnergyBST(+3)
        ],

        BOX_SHOULDER: [
            (3060401, 0.20),  # BlockShldrTD(+1)
            (3060404, 0.20),  # BlockShldrGUN(+1)
            (3060407, 0.20),  # BlockShldrTG(+1)
            (3060303, 0.10),  # SoftShldrTD(+3)
            (3060306, 0.10),  # SoftShldrGUN(+3)
            (3060309, 0.10),  # SoftShldrTG(+3)
            (3060402, 0.04),  # BlockShldrTD(+2)
            (3060405, 0.03),  # BlockShldrGUN(+2)
            (3060408, 0.03)   # BlockShldrTG(+2)
        ],

        BOX_MINI_BOT: [
            (3011507, 0.10),    # BabytankCRT(+3)
            (3011504, 0.10),    # BabytankCRT(+2)
            (3011505, 0.10),    # BabytankMIS(+2)
            (3011506, 0.10),    # BabytankBST(+2)
            (3011509, 0.10),    # BabytankBST(+3)
            (3011508, 0.10),    # BabytankMIS(+3)
            (3011602, 0.075),   # BeholderMIS(+1)
            (3011601, 0.065),   # BeholderCRT(+1)
            (3011501, 0.065),   # BabytankCRT(+1)
            (3011503, 0.065),   # BabytankBST(+1)
            (3011502, 0.065),   # BabytankMIS(+1)
            (3011603, 0.065)    # BeholderBST(+1)
        ],

        BOX_HEAD: [
            (1010601, 0.60),  # HyperDrillCRT(+1) — LandsliderMIS(+1) — SpikeHazardSP(+1)
            (1010602, 0.30),  # HyperDrillCRT(+2) — LandsliderMIS(+2) — SpikeHazardSP(+2)
            (1010603, 0.10)   # HyperDrillCRT(+3) — LandsliderMIS(+3) — SpikeHazardSP(+3)
        ],

        BOX_BODY: [
            (1020601, 0.60),  # HyperDrillTA(+1) — LandsliderBST(+1) — SpikeHazardMX(+1)
            (1020602, 0.30),  # HyperDrillTA(+2) — LandsliderBST(+2) — SpikeHazardMX(+2)
            (1020603, 0.10)   # HyperDrillTA(+3) — LandsliderBST(+3) — SpikeHazardMX(+3)
        ],

        BOX_ARMS: [
            (1030601, 0.60),  # HyperDrillTD(+1) — LandsliderGUN(+1) — SpikeHazardTG(+1)
            (1030602, 0.30),  # HyperDrillTD(+2) — LandsliderGUN(+2) — SpikeHazardTG(+2)
            (1030603, 0.10)   # HyperDrillTD(+3) — LandsliderGUN(+3) — SpikeHazardTG(+3)
        ]
    },

    # [Lv48]Planet-MECA2
    19: {
        BOX_GUN: [
            (3021601, 0.40), # WhiteBlazer(+1)
            (3021502, 0.30), # LightningGun(+2)
            (3021503, 0.20), # LightningGun(+3)
            (3021602, 0.10)  # WhiteBlazer(+2)
        ],

        BOX_SHIELD: [
            (3050304, 0.15), # HeavyshieldGUN(+1)
            (3050307, 0.15), # HeavyshieldTG(+1)
            (3050301, 0.15), # HeavyshieldTD(+1)
            (3050308, 0.10), # HeavyshieldTG(+2)
            (3050302, 0.10), # HeavyshieldTD(+2)
            (3050305, 0.10), # HeavyshieldGUN(+2)
            (3050306, 0.05), # HeavyshieldGUN(+3)
            (3050203, 0.04), # BucklerShldTD(+3)
            (3050209, 0.04), # HeavyshieldTD(+3)
            (3050303, 0.04), # BucklerShldTG(+3)
            (3050206, 0.04), # BucklerShldGUN(+3)
            (3050309, 0.04)  # HeavyshieldTG(+3)
        ],

        BOX_EF: [
            (3031504, 0.20),  # SoundEnergyCRT(+2)
            (3031505, 0.20),  # SoundEnergyMIS(+2)
            (3031506, 0.20),  # SoundEnergyBST(+2)
            (3031501, 0.075),  # SoundEnergyCRT(+1)
            (3031502, 0.075),  # SoundEnergyMIS(+1)
            (3031503, 0.075),  # SoundEnergyBST(+1)
            (3031507, 0.075),  # SoundEnergyCRT(+3)
            (3031508, 0.075),  # SoundEnergyMIS(+3)
            (3031509, 0.075)   # SoundEnergyBST(+3)
        ],

        BOX_SHOULDER: [
            (3060404, 0.15), # BlockShldrGUN(+1)
            (3060407, 0.15), # BlockShldrTG(+1)
            (3060401, 0.15), # BlockShldrTD(+1)
            (3060408, 0.10), # BlockShldrTG(+2)
            (3060402, 0.10), # BlockShldrTD(+2)
            (3060405, 0.10), # BlockShldrGUN(+2)
            (3060406, 0.05), # BlockShldrGUN(+3)
            (3060303, 0.04), # SoftShldrTD(+3)
            (3060403, 0.04), # BlockShldrTD(+3)
            (3060309, 0.04), # SoftShldrTG(+3)
            (3060306, 0.04), # SoftShldrGUN(+3)
            (3060409, 0.04)  # BlockShldrTG(+3)
        ],

        BOX_MINI_BOT: [
            (3011507, 0.20),    # BabytankCRT(+3)
            (3011508, 0.20),    # BabytankMIS(+3)
            (3011509, 0.20),    # BabytankBST(+3)
            (3011504, 0.075),   # BabytankCRT(+2)
            (3011505, 0.065),   # BabytankMIS(+2)
            (3011506, 0.065),   # BabytankBST(+2)
            (3011601, 0.065),   # BeholderCRT(+1)
            (3011602, 0.065),   # BeholderMIS(+1)
            (3011603, 0.065)    # BeholderBST(+1)
        ],

        BOX_HEAD: [
            (1010601, 0.60),  # HyperDrillCRT(+1) — LandsliderMIS(+1) — SpikeHazardSP(+1)
            (1010602, 0.30),  # HyperDrillCRT(+2) — LandsliderMIS(+2) — SpikeHazardSP(+2)
            (1010603, 0.10)   # HyperDrillCRT(+3) — LandsliderMIS(+3) — SpikeHazardSP(+3)
        ],

        BOX_BODY: [
            (1020601, 0.60),  # HyperDrillTA(+1) — LandsliderBST(+1) — SpikeHazardMX(+1)
            (1020602, 0.30),  # HyperDrillTA(+2) — LandsliderBST(+2) — SpikeHazardMX(+2)
            (1020603, 0.10)   # HyperDrillTA(+3) — LandsliderBST(+3) — SpikeHazardMX(+3)
        ],

        BOX_ARMS: [
            (1030601, 0.60),  # HyperDrillTD(+1) — LandsliderGUN(+1) — SpikeHazardTG(+1)
            (1030602, 0.30),  # HyperDrillTD(+2) — LandsliderGUN(+2) — SpikeHazardTG(+2)
            (1030603, 0.10)   # HyperDrillTD(+3) — LandsliderGUN(+3) — SpikeHazardTG(+3)
        ]
    },

    # [Lv50]Hidden-Archive
    20: {
        BOX_GUN: [
            (3021503, 0.40), # LightningGun(+3)
            (3021601, 0.30), # WhiteBlazer(+1)
            (3021602, 0.20), # WhiteBlazer(+2)
            (3021502, 0.10)  # LightningGun(+2)
        ],

        BOX_SHIELD: [
            (3050302, 0.20), # HeavyshieldTD(+2)
            (3050305, 0.20), # HeavyshieldGUN(+2)
            (3050308, 0.20), # HeavyshieldTG(+2)
            (3050301, 0.08), # HeavyshieldTD(+1)
            (3050303, 0.06), # HeavyshieldTD(+3)
            (3050304, 0.07), # HeavyshieldGUN(+1)
            (3050306, 0.06), # HeavyshieldGUN(+3)
            (3050307, 0.07), # HeavyshieldTG(+1)
            (3050309, 0.06)  # HeavyshieldTG(+3)
        ],

        BOX_EF: [
            (3031507, 0.10),    # SoundEnergyCRT(+3)
            (3031504, 0.10),    # SoundEnergyCRT(+2)
            (3031505, 0.10),    # SoundEnergyMIS(+2)
            (3031506, 0.10),    # SoundEnergyBST(+2)
            (3031509, 0.10),    # SoundEnergyBST(+3)
            (3031508, 0.10),    # SoundEnergyMIS(+3)
            (3031602, 0.075),   # SparkMIS(+1)
            (3031601, 0.065),   # SparkCRT(+1)
            (3031501, 0.065),   # SoundEnergyCRT(+1)
            (3031503, 0.065),   # SoundEnergyBST(+1)
            (3031502, 0.065),   # SoundEnergyMIS(+1)
            (3031603, 0.065)    # SparkBST(+1)
        ],

        BOX_SHOULDER: [
            (3060402, 0.20), # BlockShldrTD(+2)
            (3060405, 0.20), # BlockShldrGUN(+2)
            (3060408, 0.20), # BlockShldrTG(+2)
            (3060401, 0.08), # BlockShldrTD(+1)
            (3060403, 0.06), # BlockShldrTD(+3)
            (3060404, 0.07), # BlockShldrGUN(+1)
            (3060406, 0.06), # BlockShldrGUN(+3)
            (3060407, 0.07), # BlockShldrTG(+1)
            (3060409, 0.06)  # BlockShldrTG(+3)
        ],

        BOX_MINI_BOT: [
            (3011601, 0.125),   # BeholderCRT(+1)
            (3011603, 0.125),   # BeholderBST(+1)
            (3011602, 0.125),   # BeholderMIS(+1)
            (3011507, 0.10),    # BabytankCRT(+3)
            (3011508, 0.10),    # BabytankMIS(+3)
            (3011509, 0.10),    # BabytankBST(+3)
            (3011605, 0.0625),  # BeholderMIS(+2)
            (3011604, 0.0625),  # BeholderCRT(+2)
            (3011504, 0.05),    # BabytankCRT(+2)
            (3011506, 0.05),    # BabytankBST(+2)
            (3011505, 0.05),    # BabytankMIS(+2)
            (3011606, 0.05)     # BeholderBST(+2)
        ],

        BOX_HEAD: [
            (1010601, 0.60),  # HyperDrillCRT(+1) — LandsliderMIS(+1) — SpikeHazardSP(+1)
            (1010602, 0.30),  # HyperDrillCRT(+2) — LandsliderMIS(+2) — SpikeHazardSP(+2)
            (1010603, 0.10)   # HyperDrillCRT(+3) — LandsliderMIS(+3) — SpikeHazardSP(+3)
        ],

        BOX_BODY: [
            (1020601, 0.60),  # HyperDrillTA(+1) — LandsliderBST(+1) — SpikeHazardMX(+1)
            (1020602, 0.30),  # HyperDrillTA(+2) — LandsliderBST(+2) — SpikeHazardMX(+2)
            (1020603, 0.10)   # HyperDrillTA(+3) — LandsliderBST(+3) — SpikeHazardMX(+3)
        ],

        BOX_ARMS: [
            (1030601, 0.60),  # HyperDrillTD(+1) — LandsliderGUN(+1) — SpikeHazardTG(+1)
            (1030602, 0.30),  # HyperDrillTD(+2) — LandsliderGUN(+2) — SpikeHazardTG(+2)
            (1030603, 0.10)   # HyperDrillTD(+3) — LandsliderGUN(+3) — SpikeHazardTG(+3)
        ]
    },

    # [Lv53]Secret-passage
    21: {
        BOX_GUN: [
            (3021602, 0.40), # WhiteBlazer(+2)
            (3021503, 0.30), # LightningGun(+3)
            (3021601, 0.15), # WhiteBlazer(+1)
            (3021603, 0.15)  # WhiteBlazer(+3)
        ],

        BOX_SHIELD: [
            (3050303, 0.20), # HeavyshieldTD(+3)
            (3050306, 0.20), # HeavyshieldGUN(+3)
            (3050309, 0.20), # HeavyshieldTG(+3)
            (3050302, 0.10), # HeavyshieldTD(+2)
            (3050305, 0.10), # HeavyshieldGUN(+2)
            (3050308, 0.10), # HeavyshieldTG(+2)
            (3050401, 0.04), # TowershieldTD(+1)
            (3050404, 0.03), # TowershieldGUN(+1)
            (3050407, 0.03)  # TowershieldTG(+1)
        ],

        BOX_EF: [
            (3031507, 0.15),  # SoundEnergyCRT(+3)
            (3031508, 0.15),  # SoundEnergyMIS(+3)
            (3031509, 0.15),  # SoundEnergyBST(+3)
            (3031601, 0.15),  # SparkCRT(+1)
            (3031602, 0.15),  # SparkMIS(+1)
            (3031603, 0.15),  # SparkBST(+1)
            (3031504, 0.04),  # SoundEnergyCRT(+2)
            (3031505, 0.03),  # SoundEnergyMIS(+2)
            (3031506, 0.03)   # SoundEnergyBST(+2)
        ],

        BOX_SHOULDER: [
            (3060403, 0.20), # BlockShldrTD(+3)
            (3060406, 0.20), # BlockShldrGUN(+3)
            (3060409, 0.20), # BlockShldrTG(+3)
            (3060402, 0.10), # BlockShldrTD(+2)
            (3060405, 0.10), # BlockShldrGUN(+2)
            (3060408, 0.10), # BlockShldrTG(+2)
            (3060501, 0.04), # Spec-LightTD(+1)
            (3060504, 0.03), # Spec-LightGUN(+1)
            (3060507, 0.03)  # Spec-LightTG(+1)
        ],

        BOX_MINI_BOT: [
            (3011601, 0.15), # BeholderCRT(+1)
            (3011602, 0.15), # BeholderMIS(+1)
            (3011603, 0.15), # BeholderBST(+1)
            (3011604, 0.15), # BeholderCRT(+2)
            (3011605, 0.15), # BeholderMIS(+2)
            (3011606, 0.15), # BeholderBST(+2)
            (3011607, 0.04), # BeholderCRT(+3)
            (3011608, 0.03), # BeholderMIS(+3)
            (3011609, 0.03)  # BeholderBST(+3)
        ],

        BOX_HEAD: [
            (1010701, 0.60),  # fireroadCRT(+1) — SwordcasterMIS(+1) — MinusboltSP(+1)
            (1010702, 0.30),  # fireroadCRT(+2) — SwordcasterMIS(+2) — MinusboltSP(+2)
            (1010703, 0.10)   # fireroadCRT(+3) — SwordcasterMIS(+3) — MinusboltSP(+3)
        ],

        BOX_BODY: [
            (1020701, 0.60),  # fireroadTA(+1) — SwordcasterBST(+1) — MinusboltMX(+1)
            (1020702, 0.30),  # fireroadTA(+2) — SwordcasterBST(+2) — MinusboltMX(+2)
            (1020703, 0.10)   # fireroadTA(+3) — SwordcasterBST(+3) — MinusboltMX(+3)
        ],

        BOX_ARMS: [
            (1030701, 0.60),  # fireroadTD(+1) — SwordcasterGUN(+1) — MinusboltTG(+1)
            (1030702, 0.30),  # fireroadTD(+2) — SwordcasterGUN(+2) — MinusboltTG(+2)
            (1030703, 0.10)   # fireroadTD(+3) — SwordcasterGUN(+3) — MinusboltTG(+3)
        ]
    },

    # [Lv56]Destroy-all
    22: {
        BOX_GUN: [
            (3021603, 0.40), # WhiteBlazer(+3)
            (3021602, 0.30), # WhiteBlazer(+2)
            (3021503, 0.15), # LightningGun(+3)
            (3021701, 0.15)  # AuraBlazer(+1)
        ],

        BOX_SHIELD: [
            (3050401, 0.20), # TowershieldTD(+1)
            (3050404, 0.20), # TowershieldGUN(+1)
            (3050407, 0.20), # TowershieldTG(+1)
            (3050303, 0.10), # HeavyshieldTD(+3)
            (3050306, 0.10), # HeavyshieldGUN(+3)
            (3050309, 0.10), # HeavyshieldTG(+3)
            (3050402, 0.04), # TowershieldTD(+2)
            (3050405, 0.03), # TowershieldGUN(+2)
            (3050408, 0.03)  # TowershieldTG(+2)
        ],

        BOX_EF: [
            (3031601, 0.125),   # SparkCRT(+1)
            (3031602, 0.125),   # SparkMIS(+1)
            (3031603, 0.125),   # SparkBST(+1)
            (3031604, 0.10),    # SparkCRT(+2)
            (3031606, 0.10),    # SparkBST(+2)
            (3031605, 0.10),    # SparkMIS(+2)
            (3031608, 0.0625),  # SparkMIS(+3)
            (3031607, 0.0625),  # SparkCRT(+3)
            (3031507, 0.05),    # SoundEnergyCRT(+3)
            (3031509, 0.05),    # SoundEnergyBST(+3)
            (3031508, 0.05),    # SoundEnergyMIS(+3)
            (3031609, 0.05)     # SparkBST(+3)
        ],

        BOX_SHOULDER: [
            (3060501, 0.20), # Spec-LightTD(+1)
            (3060504, 0.20), # Spec-LightGUN(+1)
            (3060507, 0.20), # Spec-LightTG(+1)
            (3060403, 0.10), # BlockShldrTD(+3)
            (3060406, 0.10), # BlockShldrGUN(+3)
            (3060409, 0.10), # BlockShldrTG(+3)
            (3060502, 0.04), # Spec-LightTD(+2)
            (3060505, 0.03), # Spec-LightGUN(+2)
            (3060508, 0.03)  # Spec-LightTG(+2)
        ],

        BOX_MINI_BOT: [
            (3011607, 0.10),    # BeholderCRT(+3)
            (3011604, 0.10),    # BeholderCRT(+2)
            (3011605, 0.10),    # BeholderMIS(+2)
            (3011606, 0.10),    # BeholderBST(+2)
            (3011609, 0.10),    # BeholderBST(+3)
            (3011608, 0.10),    # BeholderMIS(+3)
            (3011702, 0.075),   # LittleroidMIS(+1)
            (3011701, 0.065),   # LittleroidCRT(+1)
            (3011601, 0.065),   # BeholderCRT(+1)
            (3011603, 0.065),   # BeholderBST(+1)
            (3011602, 0.065),   # BeholderMIS(+1)
            (3011703, 0.065)    # LittleroidBST(+1)
        ],

        BOX_HEAD: [
            (1010701, 0.60),  # fireroadCRT(+1) — SwordcasterMIS(+1) — MinusboltSP(+1)
            (1010702, 0.30),  # fireroadCRT(+2) — SwordcasterMIS(+2) — MinusboltSP(+2)
            (1010703, 0.10)   # fireroadCRT(+3) — SwordcasterMIS(+3) — MinusboltSP(+3)
        ],

        BOX_BODY: [
            (1020701, 0.60),  # fireroadTA(+1) — SwordcasterBST(+1) — MinusboltMX(+1)
            (1020702, 0.30),  # fireroadTA(+2) — SwordcasterBST(+2) — MinusboltMX(+2)
            (1020703, 0.10)   # fireroadTA(+3) — SwordcasterBST(+3) — MinusboltMX(+3)
        ],

        BOX_ARMS: [
            (1030701, 0.60),  # fireroadTD(+1) — SwordcasterGUN(+1) — MinusboltTG(+1)
            (1030702, 0.30),  # fireroadTD(+2) — SwordcasterGUN(+2) — MinusboltTG(+2)
            (1030703, 0.10)   # fireroadTD(+3) — SwordcasterGUN(+3) — MinusboltTG(+3)
        ]
    },

    # [Lv58]Destroy-all2
    23: {
        BOX_GUN: [
            (3021603, 0.60), # WhiteBlazer(+3)
            (3021701, 0.30), # AuraBlazer(+1)
            (3021602, 0.10)  # WhiteBlazer(+2)
        ],

        BOX_SHIELD: [
            (3050404, 0.15), # TowershieldGUN(+1)
            (3050407, 0.15), # TowershieldTG(+1)
            (3050401, 0.15), # TowershieldTD(+1)
            (3050408, 0.10), # TowershieldTG(+2)
            (3050402, 0.10), # TowershieldTD(+2)
            (3050405, 0.10), # TowershieldGUN(+2)
            (3050406, 0.05), # TowershieldGUN(+3)
            (3050303, 0.04), # HeavyshieldTD(+3)
            (3050403, 0.04), # TowershieldTD(+3)
            (3050309, 0.04), # HeavyshieldTG(+3)
            (3050306, 0.04), # HeavyshieldGUN(+3)
            (3050409, 0.04)  # TowershieldTG(+3)
        ],

        BOX_EF: [
            (3031604, 0.20),    # SparkCRT(+2)
            (3031605, 0.20),    # SparkMIS(+2)
            (3031606, 0.20),    # SparkBST(+2)
            (3031601, 0.075),   # SparkCRT(+1)
            (3031602, 0.075),   # SparkMIS(+1)
            (3031603, 0.075),   # SparkBST(+1)
            (3031607, 0.075),   # SparkCRT(+3)
            (3031608, 0.075),   # SparkMIS(+3)
            (3031609, 0.075)    # SparkBST(+3)
        ],

        BOX_SHOULDER: [
            (3060504, 0.15), # Spec-LightGUN(+1)
            (3060507, 0.15), # Spec-LightTG(+1)
            (3060501, 0.15), # Spec-LightTD(+1)
            (3060508, 0.10), # Spec-LightTG(+2)
            (3060502, 0.10), # Spec-LightTD(+2)
            (3060505, 0.10), # Spec-LightGUN(+2)
            (3060506, 0.05), # Spec-LightGUN(+3)
            (3060403, 0.04), # BlockShldrTD(+3)
            (3060503, 0.04), # Spec-LightTD(+3)
            (3060409, 0.04), # BlockShldrTG(+3)
            (3060406, 0.04), # BlockShldrGUN(+3)
            (3060509, 0.04)  # Spec-LightTG(+3)
        ],

        BOX_MINI_BOT: [
            (3011607, 0.20),    # BeholderCRT(+3)
            (3011608, 0.20),    # BeholderMIS(+3)
            (3011609, 0.20),    # BeholderBST(+3)
            (3011604, 0.075),   # BeholderCRT(+2)
            (3011605, 0.065),   # BeholderMIS(+2)
            (3011606, 0.065),   # BeholderBST(+2)
            (3011701, 0.065),   # LittleroidCRT(+1)
            (3011702, 0.065),   # LittleroidMIS(+1)
            (3011703, 0.065)    # LittleroidBST(+1)
        ],

        BOX_HEAD: [
            (1010701, 0.60),  # fireroadCRT(+1) — SwordcasterMIS(+1) — MinusboltSP(+1)
            (1010702, 0.30),  # fireroadCRT(+2) — SwordcasterMIS(+2) — MinusboltSP(+2)
            (1010703, 0.10),  # fireroadCRT(+3) — SwordcasterMIS(+3) — MinusboltSP(+3)
        ],

        BOX_BODY: [
            (1020701, 0.60),  # fireroadTA(+1) — SwordcasterBST(+1) — MinusboltMX(+1)
            (1020702, 0.30),  # fireroadTA(+2) — SwordcasterBST(+2) — MinusboltMX(+2)
            (1020703, 0.10)   # fireroadTA(+3) — SwordcasterBST(+3) — MinusboltMX(+3)
        ],

        BOX_ARMS: [
            (1030701, 0.60),  # fireroadTD(+1) — SwordcasterGUN(+1) — MinusboltTG(+1)
            (1030702, 0.30),  # fireroadTD(+2) — SwordcasterGUN(+2) — MinusboltTG(+2)
            (1030703, 0.10)   # fireroadTD(+3) — SwordcasterGUN(+3) — MinusboltTG(+3)
        ]
    },

    # [Lv60]Escape-From-MECA
    24: {
        BOX_GUN: [
            (3021701, 0.60), # AuraBlazer(+1)
            (3021603, 0.40)  # WhiteBlazer(+3)
        ],

        BOX_SHIELD: [
            (3050402, 0.20), # TowershieldTD(+2)
            (3050405, 0.20), # TowershieldGUN(+2)
            (3050408, 0.20), # TowershieldTG(+2)
            (3050401, 0.08), # TowershieldTD(+1)
            (3050403, 0.06), # TowershieldTD(+3)
            (3050404, 0.07), # TowershieldGUN(+1)
            (3050406, 0.06), # TowershieldGUN(+3)
            (3050407, 0.07), # TowershieldTG(+1)
            (3050409, 0.06)  # TowershieldTG(+3)
        ],

        BOX_EF: [
            (3031607, 0.10),    # SparkCRT(+3)
            (3031604, 0.10),    # SparkCRT(+2)
            (3031605, 0.10),    # SparkMIS(+2)
            (3031606, 0.10),    # SparkBST(+2)
            (3031609, 0.10),    # SparkBST(+3)
            (3031608, 0.10),    # SparkMIS(+3)
            (3031702, 0.075),   # CrimsonfieldMIS(+1)
            (3031701, 0.065),   # CrimsonfieldCRT(+1)
            (3031601, 0.065),   # SparkCRT(+1)
            (3031603, 0.065),   # SparkBST(+1)
            (3031602, 0.065),   # SparkMIS(+1)
            (3031703, 0.065)    # CrimsonfieldBST(+1)
        ],

        BOX_SHOULDER: [
            (3060502, 0.20), # Spec-LightTD(+2)
            (3060505, 0.20), # Spec-LightGUN(+2)
            (3060508, 0.20), # Spec-LightTG(+2)
            (3060501, 0.08), # Spec-LightTD(+1)
            (3060503, 0.06), # Spec-LightTD(+3)
            (3060504, 0.07), # Spec-LightGUN(+1)
            (3060506, 0.06), # Spec-LightGUN(+3)
            (3060507, 0.07), # Spec-LightTG(+1)
            (3060509, 0.06)  # Spec-LightTG(+3)
        ],

        BOX_MINI_BOT: [
            (3011701, 0.125),   # LittleroidCRT(+1)
            (3011703, 0.125),   # LittleroidBST(+1)
            (3011702, 0.125),   # LittleroidMIS(+1)
            (3011607, 0.10),    # BeholderCRT(+3)
            (3011608, 0.10),    # BeholderMIS(+3)
            (3011609, 0.10),    # BeholderBST(+3)
            (3011705, 0.0625),  # LittleroidMIS(+2)
            (3011704, 0.0625),  # LittleroidCRT(+2)
            (3011604, 0.05),    # BeholderCRT(+2)
            (3011606, 0.05),    # BeholderBST(+2)
            (3011605, 0.05),    # BeholderMIS(+2)
            (3011706, 0.05)     # LittleroidBST(+2)
        ],

        BOX_HEAD: [
            (1010701, 0.60),  # fireroadCRT(+1) — SwordcasterMIS(+1) — MinusboltSP(+1)
            (1010702, 0.30),  # fireroadCRT(+2) — SwordcasterMIS(+2) — MinusboltSP(+2)
            (1010703, 0.10)   # fireroadCRT(+3) — SwordcasterMIS(+3) — MinusboltSP(+3)
        ],

        BOX_BODY: [
            (1020701, 0.60),  # fireroadTA(+1) — SwordcasterBST(+1) — MinusboltMX(+1)
            (1020702, 0.30),  # fireroadTA(+2) — SwordcasterBST(+2) — MinusboltMX(+2)
            (1020703, 0.10)   # fireroadTA(+3) — SwordcasterBST(+3) — MinusboltMX(+3)
        ],

        BOX_ARMS: [
            (1030701, 0.60),  # fireroadTD(+1) — SwordcasterGUN(+1) — MinusboltTG(+1)
            (1030702, 0.30),  # fireroadTD(+2) — SwordcasterGUN(+2) — MinusboltTG(+2)
            (1030703, 0.10)   # fireroadTD(+3) — SwordcasterGUN(+3) — MinusboltTG(+3)
        ]
    },

    # [Lv61]Ship Takeover
    25: {
        BOX_GUN: [
            (3021701, 0.60),    # AuraBlazer(+1)
            (3021603, 0.30),    # WhiteBlazer(+3)
            (3021702, 0.10)     # AuraBlazer(+2)
        ],

        BOX_SHIELD: [
            (3050402, 0.20), # TowershieldTD(+2)
            (3050405, 0.20), # TowershieldGUN(+2)
            (3050408, 0.20), # TowershieldTG(+2)
            (3050403, 0.10), # TowershieldTD(+3)
            (3050406, 0.10), # TowershieldGUN(+3)
            (3050409, 0.10), # TowershieldTG(+3)
            (3050401, 0.04), # TowershieldTD(+1)
            (3050404, 0.03), # TowershieldGUN(+1)
            (3050407, 0.03)  # TowershieldTG(+1)
        ],

        BOX_EF: [
            (3031607, 0.15),  # SparkCRT(+3)
            (3031608, 0.15),  # SparkMIS(+3)
            (3031609, 0.15),  # SparkBST(+3)
            (3031604, 0.15),  # SparkCRT(+2)
            (3031605, 0.15),  # SparkMIS(+2)
            (3031606, 0.15),  # SparkBST(+2)
            (3031701, 0.04),  # CrimsonfieldCRT(+1)
            (3031702, 0.03),  # CrimsonfieldMIS(+1)
            (3031703, 0.03)   # CrimsonfieldBST(+1)
        ],

        BOX_SHOULDER: [
            (3060502, 0.20), # Spec-LightTD(+2)
            (3060505, 0.20), # Spec-LightGUN(+2)
            (3060508, 0.20), # Spec-LightTG(+2)
            (3060503, 0.10), # Spec-LightTD(+3)
            (3060506, 0.10), # Spec-LightGUN(+3)
            (3060509, 0.10), # Spec-LightTG(+3)
            (3060501, 0.04), # Spec-LightTD(+1)
            (3060504, 0.03), # Spec-LightGUN(+1)
            (3060507, 0.03)  # Spec-LightTG(+1)
        ],

        BOX_MINI_BOT: [
            (3011701, 0.19), # LittleroidCRT(+1)
            (3011702, 0.19), # LittleroidMIS(+1)
            (3011703, 0.19), # LittleroidBST(+1)
            (3011607, 0.08), # BeholderCRT(+3)
            (3011608, 0.07), # BeholderMIS(+3)
            (3011609, 0.07), # BeholderBST(+3)
            (3011704, 0.07), # LittleroidCRT(+2)
            (3011705, 0.07), # LittleroidMIS(+2)
            (3011706, 0.07)  # LittleroidBST(+2)
        ],

        BOX_HEAD: [
            (1010701, 0.60),  # fireroadCRT(+1) — SwordcasterMIS(+1) — MinusboltSP(+1)
            (1010702, 0.30),  # fireroadCRT(+2) — SwordcasterMIS(+2) — MinusboltSP(+2)
            (1010703, 0.10)   # fireroadCRT(+3) — SwordcasterMIS(+3) — MinusboltSP(+3)
        ],

        BOX_BODY: [
            (1020701, 0.60),  # fireroadTA(+1) — SwordcasterBST(+1) — MinusboltMX(+1)
            (1020702, 0.30),  # fireroadTA(+2) — SwordcasterBST(+2) — MinusboltMX(+2)
            (1020703, 0.10)   # fireroadTA(+3) — SwordcasterBST(+3) — MinusboltMX(+3)
        ],

        BOX_ARMS: [
            (1030701, 0.60),  # fireroadTD(+1) — SwordcasterGUN(+1) — MinusboltTG(+1)
            (1030702, 0.30),  # fireroadTD(+2) — SwordcasterGUN(+2) — MinusboltTG(+2)
            (1030703, 0.10)   # fireroadTD(+3) — SwordcasterGUN(+3) — MinusboltTG(+3)
        ]
    },

    # [Lv63]MeraMountin
    26: {
        BOX_GUN: [
            (3021701, 0.40), # AuraBlazer(+1)
            (3021702, 0.30), # AuraBlazer(+2)
            (3021603, 0.15), # WhiteBlazer(+3)
            (3021801, 0.15)  # HeavyLaunch(+1)
        ],

        BOX_SHIELD: [
            (3050403, 0.20), # TowershieldTD(+3)
            (3050406, 0.20), # TowershieldGUN(+3)
            (3050409, 0.20), # TowershieldTG(+3)
            (3050402, 0.10), # TowershieldTD(+2)
            (3050405, 0.10), # TowershieldGUN(+2)
            (3050408, 0.10), # TowershieldTG(+2)
            (3050501, 0.04), # ScutumTD(+1)
            (3050504, 0.03), # ScutumGUN(+1)
            (3050507, 0.03)  # ScutumTG(+1)
        ],

        BOX_EF: [
            (3031607, 0.15),  # SparkCRT(+3)
            (3031608, 0.15),  # SparkMIS(+3)
            (3031609, 0.15),  # SparkBST(+3)
            (3031701, 0.15),  # CrimsonfieldCRT(+1)
            (3031702, 0.15),  # CrimsonfieldMIS(+1)
            (3031703, 0.15),  # CrimsonfieldBST(+1)
            (3031604, 0.04),  # SparkCRT(+2)
            (3031605, 0.03),  # SparkMIS(+2)
            (3031606, 0.03)   # SparkBST(+2)
        ],

        BOX_SHOULDER: [
            (3060503, 0.20), # Spec-LightTD(+3)
            (3060506, 0.20), # Spec-LightGUN(+3)
            (3060509, 0.20), # Spec-LightTG(+3)
            (3060502, 0.10), # Spec-LightTD(+2)
            (3060505, 0.10), # Spec-LightGUN(+2)
            (3060508, 0.10), # Spec-LightTG(+2)
            (3060601, 0.04), # ShldrBladeTD(+1)
            (3060604, 0.03), # ShldrBladeGUN(+1)
            (3060607, 0.03)  # ShldrBladeTG(+1)
        ],

        BOX_MINI_BOT: [
            (3011701, 0.15), # LittleroidCRT(+1)
            (3011702, 0.15), # LittleroidMIS(+1)
            (3011703, 0.15), # LittleroidBST(+1)
            (3011704, 0.15), # LittleroidCRT(+2)
            (3011705, 0.15), # LittleroidMIS(+2)
            (3011706, 0.15), # LittleroidBST(+2)
            (3011707, 0.04), # LittleroidCRT(+3)
            (3011708, 0.03), # LittleroidMIS(+3)
            (3011709, 0.03)  # LittleroidBST(+3)
        ],

        BOX_HEAD: [
            (1010701, 0.60),  # fireroadCRT(+1) — SwordcasterMIS(+1) — MinusboltSP(+1)
            (1010702, 0.30),  # fireroadCRT(+2) — SwordcasterMIS(+2) — MinusboltSP(+2)
            (1010703, 0.10)   # fireroadCRT(+3) — SwordcasterMIS(+3) — MinusboltSP(+3)
        ],

        BOX_BODY: [
            (1020701, 0.60),  # fireroadTA(+1) — SwordcasterBST(+1) — MinusboltMX(+1)
            (1020702, 0.30),  # fireroadTA(+2) — SwordcasterBST(+2) — MinusboltMX(+2)
            (1020703, 0.10)   # fireroadTA(+3) — SwordcasterBST(+3) — MinusboltMX(+3)
        ],

        BOX_ARMS: [
            (1030701, 0.60),  # fireroadTD(+1) — SwordcasterGUN(+1) — MinusboltTG(+1)
            (1030702, 0.30),  # fireroadTD(+2) — SwordcasterGUN(+2) — MinusboltTG(+2)
            (1030703, 0.10)   # fireroadTD(+3) — SwordcasterGUN(+3) — MinusboltTG(+3)
        ]
    },

    # [Lv66]MeraMountin2
    27: {
        BOX_GUN: [
            (3021702, 0.40), # AuraBlazer(+2)
            (3021801, 0.30), # HeavyLaunch(+1)
            (3021701, 0.15), # AuraBlazer(+1)
            (3021703, 0.15)  # AuraBlazer(+3)
        ],

        BOX_SHIELD: [
            (3050501, 0.20), # ScutumTD(+1)
            (3050504, 0.20), # ScutumGUN(+1)
            (3050507, 0.20), # ScutumTG(+1)
            (3050403, 0.10), # TowershieldTD(+3)
            (3050406, 0.10), # TowershieldGUN(+3)
            (3050409, 0.10), # TowershieldTG(+3)
            (3050502, 0.04), # ScutumTD(+2)
            (3050505, 0.03), # ScutumGUN(+2)
            (3050508, 0.03)  # ScutumTG(+2)
        ],

        BOX_EF: [
            (3031701, 0.20),  # CrimsonfieldCRT(+1)
            (3031702, 0.20),  # CrimsonfieldMIS(+1)
            (3031703, 0.20),  # CrimsonfieldBST(+1)
            (3031704, 0.10),  # CrimsonfieldCRT(+2)
            (3031705, 0.10),  # CrimsonfieldMIS(+2)
            (3031706, 0.10),  # CrimsonfieldBST(+2)
            (3031607, 0.04),  # SparkCRT(+3)
            (3031608, 0.03),  # SparkMIS(+3)
            (3031609, 0.03)   # SparkBST(+3)
        ],

        BOX_SHOULDER: [
            (3060601, 0.20), # ShldrBladeTD(+1)
            (3060604, 0.20), # ShldrBladeGUN(+1)
            (3060607, 0.20), # ShldrBladeTG(+1)
            (3060503, 0.10), # Spec-LightTD(+3)
            (3060506, 0.10), # Spec-LightGUN(+3)
            (3060509, 0.10), # Spec-LightTG(+3)
            (3060602, 0.04), # ShldrBladeTD(+2)
            (3060605, 0.03), # ShldrBladeGUN(+2)
            (3060608, 0.03)  # ShldrBladeTG(+2)
        ],

        BOX_MINI_BOT: [
            (3011704, 0.15),    # LittleroidCRT(+2)
            (3011705, 0.15),    # LittleroidMIS(+2)
            (3011706, 0.15),    # LittleroidBST(+2)
            (3011707, 0.15),    # LittleroidCRT(+3)
            (3011708, 0.15),    # LittleroidMIS(+3)
            (3011709, 0.15),    # LittleroidBST(+3)
            (3011701, 0.04),    # LittleroidCRT(+1)
            (3011702, 0.03),    # LittleroidMIS(+1)
            (3011703, 0.03)     # LittleroidBST(+1)
        ],

        BOX_HEAD: [
            (1010701, 0.60),  # fireroadCRT(+1) — SwordcasterMIS(+1) — MinusboltSP(+1)
            (1010702, 0.30),  # fireroadCRT(+2) — SwordcasterMIS(+2) — MinusboltSP(+2)
            (1010703, 0.10)   # fireroadCRT(+3) — SwordcasterMIS(+3) — MinusboltSP(+3)
        ],

        BOX_BODY: [
            (1020701, 0.60),  # fireroadTA(+1) — SwordcasterBST(+1) — MinusboltMX(+1)
            (1020702, 0.30),  # fireroadTA(+2) — SwordcasterBST(+2) — MinusboltMX(+2)
            (1020703, 0.10)   # fireroadTA(+3) — SwordcasterBST(+3) — MinusboltMX(+3)
        ],

        BOX_ARMS: [
            (1030701, 0.60),  # fireroadTD(+1) — SwordcasterGUN(+1) — MinusboltTG(+1)
            (1030702, 0.30),  # fireroadTD(+2) — SwordcasterGUN(+2) — MinusboltTG(+2)
            (1030703, 0.10)   # fireroadTD(+3) — SwordcasterGUN(+3) — MinusboltTG(+3)
        ]
    },

    # [Lv68]MeraMountin3
    28: {
        BOX_GUN: [
            (3021801, 0.60), # HeavyLaunch(+1)
            (3021702, 0.40)  # AuraBlazer(+2)
        ],

        BOX_SHIELD: [
            (3050501, 0.20), # ScutumTD(+1)
            (3050501, 0.20), # ScutumGUN(+1)
            (3050501, 0.20), # ScutumTG(+1)
            (3050501, 0.10), # ScutumTD(+2)
            (3050501, 0.10), # ScutumGUN(+2)
            (3050501, 0.10), # ScutumTG(+2)
            (3050501, 0.04), # TowershieldTD(+3)
            (3050501, 0.03), # TowershieldGUN(+3)
            (3050501, 0.03)  # TowershieldTG(+3)
        ],

        BOX_EF: [
            (3031704, 0.20),  # CrimsonfieldCRT(+2)
            (3031705, 0.20),  # CrimsonfieldMIS(+2)
            (3031706, 0.20),  # CrimsonfieldBST(+2)
            (3031701, 0.14),  # CrimsonfieldCRT(+1)
            (3031702, 0.13),  # CrimsonfieldMIS(+1)
            (3031703, 0.13)   # CrimsonfieldBST(+1)
        ],

        BOX_SHOULDER: [
            (3060601, 0.20), # ShldrBladeTD(+1)
            (3060604, 0.20), # ShldrBladeGUN(+1)
            (3060607, 0.20), # ShldrBladeTG(+1)
            (3060602, 0.10), # ShldrBladeTD(+2)
            (3060605, 0.10), # ShldrBladeGUN(+2)
            (3060608, 0.10), # ShldrBladeTG(+2)
            (3060503, 0.04), # Spec-LightTD(+3)
            (3060506, 0.03), # Spec-LightGUN(+3)
            (3060509, 0.03)  # Spec-LightTG(+3)
        ],

        BOX_MINI_BOT: [
            (3011707, 0.20),    # LittleroidCRT(+3)
            (3011708, 0.20),    # LittleroidMIS(+3)
            (3011709, 0.20),    # LittleroidBST(+3)
            (3011704, 0.14),    # LittleroidCRT(+2)
            (3011705, 0.13),    # LittleroidMIS(+2)
            (3011706, 0.13)     # LittleroidBST(+2)
        ],

        BOX_HEAD: [
            (1010701, 0.60),  # fireroadCRT(+1) — SwordcasterMIS(+1) — MinusboltSP(+1)
            (1010702, 0.30),  # fireroadCRT(+2) — SwordcasterMIS(+2) — MinusboltSP(+2)
            (1010703, 0.10)   # fireroadCRT(+3) — SwordcasterMIS(+3) — MinusboltSP(+3)
        ],

        BOX_BODY: [
            (1020701, 0.60),  # fireroadTA(+1) — SwordcasterBST(+1) — MinusboltMX(+1)
            (1020702, 0.30),  # fireroadTA(+2) — SwordcasterBST(+2) — MinusboltMX(+2)
            (1020703, 0.10)   # fireroadTA(+3) — SwordcasterBST(+3) — MinusboltMX(+3)
        ],

        BOX_ARMS: [
            (1030701, 0.60),  # fireroadTD(+1) — SwordcasterGUN(+1) — MinusboltTG(+1)
            (1030702, 0.30),  # fireroadTD(+2) — SwordcasterGUN(+2) — MinusboltTG(+2)
            (1030703, 0.10)   # fireroadTD(+3) — SwordcasterGUN(+3) — MinusboltTG(+3)
        ]
    },

    # [Lv70]MeraMountin4
    29: {
        BOX_GUN: [
            (3021801, 0.60), # HeavyLaunch(+1)
            (3021702, 0.40)  # AuraBlazer(+2)
        ],

        BOX_SHIELD: [
            (3050502, 0.20),  # ScutumTD(+2)
            (3050505, 0.20),  # ScutumGUN(+2)
            (3050508, 0.20),  # ScutumTG(+2)
            (3050501, 0.14),  # ScutumTD(+1)
            (3050504, 0.13),  # ScutumGUN(+1)
            (3050507, 0.13)   # ScutumTG(+1)
        ],

        BOX_EF: [
            (3031704, 0.20),  # CrimsonfieldCRT(+2)
            (3031705, 0.20),  # CrimsonfieldMIS(+2)
            (3031706, 0.20),  # CrimsonfieldBST(+2)
            (3031701, 0.14),  # CrimsonfieldCRT(+1)
            (3031702, 0.13),  # CrimsonfieldMIS(+1)
            (3031703, 0.13)   # CrimsonfieldBST(+1)
        ],

        BOX_SHOULDER: [
            (3060602, 0.20),  # ShldrBladeTD(+2)
            (3060605, 0.20),  # ShldrBladeGUN(+2)
            (3060608, 0.20),  # ShldrBladeTG(+2)
            (3060601, 0.14),  # ShldrBladeTD(+1)
            (3060604, 0.13),  # ShldrBladeGUN(+1)
            (3060607, 0.13)   # ShldrBladeTG(+1)
        ],

        BOX_MINI_BOT: [
            (3011707, 0.20),    # LittleroidCRT(+3)
            (3011708, 0.20),    # LittleroidMIS(+3)
            (3011709, 0.20),    # LittleroidBST(+3)
            (3011704, 0.14),    # LittleroidCRT(+2)
            (3011705, 0.13),    # LittleroidMIS(+2)
            (3011706, 0.13)     # LittleroidBST(+2)
        ],

        BOX_HEAD: [
            (1010701, 0.60),  # fireroadCRT(+1) — SwordcasterMIS(+1) — MinusboltSP(+1)
            (1010702, 0.30),  # fireroadCRT(+2) — SwordcasterMIS(+2) — MinusboltSP(+2)
            (1010703, 0.10)   # fireroadCRT(+3) — SwordcasterMIS(+3) — MinusboltSP(+3)
        ],

        BOX_BODY: [
            (1020701, 0.60),  # fireroadTA(+1) — SwordcasterBST(+1) — MinusboltMX(+1)
            (1020702, 0.30),  # fireroadTA(+2) — SwordcasterBST(+2) — MinusboltMX(+2)
            (1020703, 0.10)   # fireroadTA(+3) — SwordcasterBST(+3) — MinusboltMX(+3)
        ],

        BOX_ARMS: [
            (1030701, 0.60),  # fireroadTD(+1) — SwordcasterGUN(+1) — MinusboltTG(+1)
            (1030702, 0.30),  # fireroadTD(+2) — SwordcasterGUN(+2) — MinusboltTG(+2)
            (1030703, 0.10)   # fireroadTD(+3) — SwordcasterGUN(+3) — MinusboltTG(+3)
        ]
    },

    # [Lv08]The-Fallen(Elite)
    30: {
        BOX_GUN: [
            (3021202, 0.40), # smartGun(+2)
            (3021103, 0.30), # smartGun(+2)
            (3021102, 0.20), # smartGun(+2)
            (3021201, 0.10)  # smartGun(+2)
        ],

        BOX_EF: [
            (3031101, 0.20),   # S-TornadoCRT(+1)
            (3031102, 0.20),   # S-TornadoMIS(+1)
            (3031103, 0.20),   # S-TornadoBST(+1)
            (3031107, 0.20),   # S-TornadoCRT(+3)
            (3031108, 0.20),   # S-TornadoMIS(+3)
            (3031109, 0.20),   # S-TornadoBST(+3)
            (3031104, 0.04),   # S-TornadoCRT(+2)
            (3031105, 0.03),   # S-TornadoMIS(+2)
            (3031106, 0.03)    # S-TornadoBST(+2)
        ],

        BOX_MINI_BOT: [
            (3011104, 0.20),    # BipadCRT(+3)
            (3011105, 0.20),    # BipadMIS(+3)
            (3011106, 0.20),    # BipadBST(+3)
            (3011201, 0.20),    # BipadCRT(+2)
            (3011202, 0.20),    # BipadMIS(+2)
            (3011203, 0.20),    # BipadBST(+2)
            (3011107, 0.04),    # BisliderCRT(+1)
            (3011108, 0.03),    # BisliderMIS(+1)
            (3011109, 0.03)     # BisliderBST(+1)
        ],

        BOX_HEAD: [
            (1010201, 0.60),  # SpikeyCRT(+1) — Lea-ClawMIS(+1) — TweezerHeadSP(+1)
            (1010202, 0.30),  # SpikeyCRT(+2) — Lea-ClawMIS(+2) — TweezerHeadSP(+2)
            (1010203, 0.10)   # SpikeyCRT(+3) — Lea-ClawMIS(+3) — TweezerHeadSP(+3)
        ],

        BOX_BODY: [
            (1020201, 0.60),  # SpikeyTA(+1) — Lea-ClawBST(+1) — TweezerHeadMX(+1)
            (1020202, 0.30),  # SpikeyTA(+2) — Lea-ClawBST(+2) — TweezerHeadMX(+2)
            (1020203, 0.10)   # SpikeyTA(+3) — Lea-ClawBST(+3) — TweezerHeadMX(+3)
        ],

        BOX_ARMS: [
            (1030201, 0.60),  # SpikeyTD(+1) — Lea-ClawGUN(+1) — TweezerHeadTG(+1)
            (1030202, 0.30),  # SpikeyTD(+2) — Lea-ClawGUN(+2) — TweezerHeadTG(+2)
            (1030203, 0.10)   # SpikeyTD(+3) — Lea-ClawGUN(+3) — TweezerHeadTG(+3)
        ]
    },

    # [Lv18]Lava-Field(Elite)
    31: {
        BOX_GUN: [
            (3021202, 0.60),  # smartGun(+2)
            (3021301, 0.30),  # FableShooter(+1)
            (3021203, 0.10)   # smartGun(+3)
        ],

        BOX_SHIELD: [
            (3051103, 0.20),  # AegisTD(+3)
            (3051106, 0.20),  # AegisGUN(+3)
            (3051109, 0.20),  # AegisTG(+3)
            (3051102, 0.10),  # AegisTD(+2)
            (3051105, 0.10),  # AegisGUN(+2)
            (3051108, 0.10),  # AegisTG(+2)
            (3051101, 0.04),  # AegisTD(+1)
            (3051104, 0.03),  # AegisGUN(+1)
            (3051107, 0.03)   # AegisTG(+1)
        ],

        BOX_EF: [
            (3031201, 0.125), # BlueCloudCRT(+1)
            (3031202, 0.125), # BlueCloudMIS(+1)
            (3031203, 0.125), # BlueCloudBST(+1)
            (3031207, 0.125), # BlueCloudCRT(+3)
            (3031208, 0.125), # BlueCloudMIS(+3)
            (3031209, 0.125), # BlueCloudBST(+3)
            (3031204, 0.09),  # BlueCloudCRT(+2)
            (3031205, 0.08),  # BlueCloudMIS(+2)
            (3031206, 0.08)   # BlueCloudBST(+2)
        ],

        BOX_SHOULDER: [
            (3060103, 0.20),  # ShoulderGrdTD(+3)
            (3060106, 0.20),  # ShoulderGrdGUN(+3)
            (3060109, 0.20),  # ShoulderGrdTG(+3)
            (3060102, 0.10),  # ShoulderGrdTD(+2)
            (3060105, 0.10),  # ShoulderGrdGUN(+2)
            (3060108, 0.10),  # ShoulderGrdTG(+2)
            (3060101, 0.04),  # ShoulderGrdTD(+1)
            (3060104, 0.03),  # ShoulderGrdGUN(+1)
            (3060107, 0.03)   # ShoulderGrdTG(+1)
        ],

        BOX_MINI_BOT: [
            (3011204, 0.20),    # BisliderCRT(+2)
            (3011205, 0.20),    # BisliderMIS(+2)
            (3011206, 0.20),    # BisliderBST(+2)
            (3011301, 0.20),    # TrilbiteCRT(+1)
            (3011302, 0.20),    # TrilbiteMIS(+1)
            (3011303, 0.20),    # TrilbiteBST(+1)
            (3011207, 0.04),    # BisliderCRT(+3)
            (3011208, 0.03),    # BisliderMIS(+3)
            (3011209, 0.03)     # BisliderBST(+3)
        ],

        BOX_HEAD: [
            (1010301, 0.60),  # StonehazardCRT(+1) — Seven-PearceMIS(+1) — ChestBusterSP(+1)
            (1010302, 0.30),  # StonehazardCRT(+2) — Seven-PearceMIS(+2) — ChestBusterSP(+2)
            (1010303, 0.10)   # StonehazardCRT(+3) — Seven-PearceMIS(+3) — ChestBusterSP(+3)
        ],

        BOX_BODY: [
            (1020301, 0.60),  # StonehazardTA(+1) — Seven-PearceBST(+1) — ChestBusterMX(+1)
            (1020302, 0.30),  # StonehazardTA(+2) — Seven-PearceBST(+2) — ChestBusterMX(+2)
            (1020303, 0.10)   # StonehazardTA(+3) — Seven-PearceBST(+3) — ChestBusterMX(+3)
        ],

        BOX_ARMS: [
            (1030301, 0.60),  # StonehazardTD(+1) — Seven-PearceGUN(+1) — ChestBusterTG(+1)
            (1030302, 0.30),  # StonehazardTD(+2) — Seven-PearceGUN(+2) — ChestBusterTG(+2)
            (1030303, 0.10)   # StonehazardTD(+3) — Seven-PearceGUN(+3) — ChestBusterTG(+3)
        ]
    },

    # [Lv28]The-Pirate(Elite)
    32: {
        BOX_GUN: [
            (3021402, 0.40),  # PaletteGun(+2)
            (3021303, 0.30),  # FableShooter(+3)
            (3021302, 0.20),  # FableShooter(+2)
            (3021401, 0.10)   # PaletteGun(+1)
        ],

        BOX_SHIELD: [
            (3051103, 0.10),  # AegisTD(+3)
            (3050106, 0.10),  # HonorshieldGUN(+3)
            (3050109, 0.10),  # HonorshieldTG(+3)
            (3050103, 0.10),  # HonorshieldTD(+3)
            (3051109, 0.10),  # AegisTG(+3)
            (3051106, 0.10),  # AegisGUN(+3)
            (3050102, 0.09),  # HonorshieldTD(+2)
            (3050105, 0.08),  # HonorshieldGUN(+2)
            (3050108, 0.08),  # HonorshieldTG(+2)
            (3050101, 0.05),  # HonorshieldTD(+1)
            (3050107, 0.05),  # HonorshieldTG(+1)
            (3050104, 0.05)   # HonorshieldGUN(+1)
        ],

        BOX_EF: [
            (3031301, 0.125),  # CirclerCRT(+2)
            (3031302, 0.125),  # CirclerMIS(+2)
            (3031303, 0.125),  # CirclerBST(+2)
            (3031307, 0.125),  # CirclerCRT(+1)
            (3031308, 0.125),  # CirclerMIS(+1)
            (3031309, 0.125),  # CirclerBST(+1)
            (3031304, 0.09),   # CirclerCRT(+3)
            (3031305, 0.08),   # CirclerMIS(+3)
            (3031306, 0.08)    # CirclerBST(+3)
        ],

        BOX_SHOULDER: [
            (3060103, 0.10),  # ShoulderGrdTD(+3)
            (3060206, 0.10),  # HeavyShldrGUN(+3)
            (3060209, 0.10),  # HeavyShldrTG(+3)
            (3060203, 0.10),  # HeavyShldrTD(+3)
            (3060109, 0.10),  # ShoulderGrdTG(+3)
            (3060106, 0.10),  # ShoulderGrdGUN(+3)
            (3060202, 0.09),  # HeavyShldrTD(+2)
            (3060205, 0.08),  # HeavyShldrGUN(+2)
            (3060208, 0.08),  # HeavyShldrTG(+2)
            (3060201, 0.05),  # HeavyShldrTD(+1)
            (3060207, 0.05),  # HeavyShldrTG(+1)
            (3060204, 0.05)   # HeavyShldrGUN(+1)
        ],

        BOX_MINI_BOT: [
            (3011304, 0.20),    # TrilbiteCRT(+2)
            (3011305, 0.20),    # TrilbiteMIS(+2)
            (3011306, 0.20),    # TrilbiteBST(+2)
            (3011401, 0.20),    # MinisatCRT(+1)
            (3011402, 0.20),    # MinisatMIS(+1)
            (3011403, 0.20),    # MinisatBST(+1)
            (3011307, 0.04),    # TrilbiteCRT(+3)
            (3011308, 0.03),    # TrilbiteMIS(+3)
            (3011309, 0.03)     # TrilbiteBST(+3)
        ],

        BOX_HEAD: [
            (1010401, 0.60),  # CrashcannonCRT(+1) — CresentJetMIS(+1) — DuskrunnerSP(+1)
            (1010402, 0.30),  # CrashcannonCRT(+2) — CresentJetMIS(+2) — DuskrunnerSP(+2)
            (1010403, 0.10)   # CrashcannonCRT(+3) — CresentJetMIS(+3) — DuskrunnerSP(+3)
        ],

        BOX_BODY: [
            (1020401, 0.60),  # CrashcannonTA(+1) — CresentJetBST(+1) — DuskrunnerMX(+1)
            (1020402, 0.30),  # CrashcannonTA(+2) — CresentJetBST(+2) — DuskrunnerMX(+2)
            (1020403, 0.10)   # CrashcannonTA(+3) — CresentJetBST(+3) — DuskrunnerMX(+3)
        ],

        BOX_ARMS: [
            (1030401, 0.60),  # CrashcannonTD(+1) — CresentJetGUN(+1) — DuskrunnerTG(+1)
            (1030402, 0.30),  # CrashcannonTD(+2) — CresentJetGUN(+2) — DuskrunnerTG(+2)
            (1030403, 0.10)   # CrashcannonTD(+3) — CresentJetGUN(+3) — DuskrunnerTG(+3)
        ]
    },

    # [Lv38]Evil-Port(Elite)
    33: {
        BOX_GUN: [
            (3021402, 0.60),  # PaletteGun(+2)
            (3021501, 0.30),  # LightningGun(+1)
            (3021403, 0.10)   # PaletteGun(+3)
        ],

        BOX_SHIELD: [
            (3050103, 0.10),  # HonorshieldTD(+3)
            (3050206, 0.10),  # BucklerShldGUN(+3)
            (3050209, 0.10),  # BucklerShldTG(+3)
            (3050203, 0.10),  # BucklerShldTD(+3)
            (3050109, 0.10),  # HonorshieldTG(+3)
            (3050106, 0.10),  # HonorshieldGUN(+3)
            (3050202, 0.09),  # BucklerShldTD(+2)
            (3050205, 0.08),  # BucklerShldGUN(+2)
            (3050208, 0.08),  # BucklerShldTG(+2)
            (3050201, 0.05),  # BucklerShldTD(+1)
            (3050207, 0.05),  # BucklerShldTG(+1)
            (3050204, 0.05)   # BucklerShldGUN(+1)
        ],

        BOX_EF: [
            (3031401, 0.125),   # T-BeaconCRT(+1)
            (3031402, 0.125),   # T-BeaconMIS(+1)
            (3031403, 0.125),   # T-BeaconBST(+1)
            (3031407, 0.125),   # T-BeaconCRT(+3)
            (3031408, 0.125),   # T-BeaconMIS(+3)
            (3031409, 0.125),   # T-BeaconBST(+3)
            (3031404, 0.09),    # T-BeaconCRT(+2)
            (3031405, 0.08),    # T-BeaconMIS(+2)
            (3031406, 0.08)     # T-BeaconBST(+2)
        ],

        BOX_SHOULDER: [
            (3060203, 0.10),  # HeavyShldrTD(+3)
            (3060306, 0.10),  # SoftShldrGUN(+3)
            (3060309, 0.10),  # SoftShldrTG(+3)
            (3060303, 0.10),  # SoftShldrTD(+3)
            (3060209, 0.10),  # HeavyShldrTG(+3)
            (3060206, 0.10),  # HeavyShldrGUN(+3)
            (3060302, 0.09),  # SoftShldrTD(+2)
            (3060305, 0.08),  # SoftShldrGUN(+2)
            (3060308, 0.08),  # SoftShldrTG(+2)
            (3060301, 0.05),  # SoftShldrTD(+1)
            (3060307, 0.05),  # SoftShldrTG(+1)
            (3060304, 0.05)   # SoftShldrGUN(+1)
        ],

        BOX_MINI_BOT: [
            (3011404, 0.20),    # MinisatCRT(+2)
            (3011405, 0.20),    # MinisatMIS(+2)
            (3011406, 0.20),    # MinisatBST(+2)
            (3011501, 0.20),    # BabytankCRT(+1)
            (3011502, 0.20),    # BabytankMIS(+1)
            (3011503, 0.20),    # BabytankBST(+1)
            (3011407, 0.04),    # MinisatCRT(+3)
            (3011408, 0.03),    # MinisatMIS(+3)
            (3011409, 0.03)     # MinisatBST(+3)
        ],

        BOX_HEAD: [
            (1010501, 0.60),  # LycaonLaunchCRT(+1) — BladeShooterMIS(+1) — SticleSP(+1)
            (1010502, 0.30),  # LycaonLaunchCRT(+2) — BladeShooterMIS(+2) — SticleSP(+2)
            (1010503, 0.10)   # LycaonLaunchCRT(+3) — BladeShooterMIS(+3) — SticleSP(+3)
        ],

        BOX_BODY: [
            (1020501, 0.60),  # LycaonLaunchTA(+1) — BladeShooterBST(+1) — SticleMX(+1)
            (1020502, 0.30),  # LycaonLaunchTA(+2) — BladeShooterBST(+2) — SticleMX(+2)
            (1020503, 0.10)  # LycaonLaunchTA(+3) — BladeShooterBST(+3) — SticleMX(+3)
        ],

        BOX_ARMS: [
            (1030501, 0.60),  # LycaonLaunchTD(+1) — BladeShooterGUN(+1) — SticleTG(+1)
            (1030502, 0.30),  # LycaonLaunchTD(+2) — BladeShooterGUN(+2) — SticleTG(+2)
            (1030503, 0.10)   # LycaonLaunchTD(+3) — BladeShooterGUN(+3) — SticleTG(+3)
        ]
    },

    # [Lv48]Bloodway(Elite)
    34: {
        BOX_GUN: [
            (3021602, 0.40),  # WhiteBlazer(+2)
            (3021503, 0.30),  # LightningGun(+3)
            (3021502, 0.20),  # LightningGun(+2)
            (3021601, 0.10)   # WhiteBlazer(+1)
        ],

        BOX_SHIELD: [
            (3050203, 0.10),  # BucklerShldTD(+3)
            (3050306, 0.10),  # HeavyshieldGUN(+3)
            (3050309, 0.10),  # HeavyshieldTG(+3)
            (3050303, 0.10),  # HeavyshieldTD(+3)
            (3050209, 0.10),  # BucklerShldTG(+3)
            (3050206, 0.10),  # BucklerShldGUN(+3)
            (3050302, 0.09),  # HeavyshieldTD(+2)
            (3050305, 0.08),  # HeavyshieldGUN(+2)
            (3050308, 0.08),  # HeavyshieldTG(+2)
            (3050301, 0.05),  # HeavyshieldTD(+1)
            (3050307, 0.05),  # HeavyshieldTG(+1)
            (3050304, 0.05)   # HeavyshieldGUN(+1)
        ],

        BOX_EF: [
            (3031501, 0.125), # SoundEnergyCRT(+1)
            (3031502, 0.125), # SoundEnergyMIS(+1)
            (3031503, 0.125), # SoundEnergyBST(+1)
            (3031507, 0.125), # SoundEnergyCRT(+3)
            (3031508, 0.125), # SoundEnergyMIS(+3)
            (3031509, 0.125), # SoundEnergyBST(+3)
            (3031504, 0.09),  # SoundEnergyCRT(+2)
            (3031505, 0.08),  # SoundEnergyMIS(+2)
            (3031506, 0.08)   # SoundEnergyBST(+2)
        ],

        BOX_SHOULDER: [
            (3060303, 0.10),  # SoftShldrTD(+3)
            (3060406, 0.10),  # BlockShldrGUN(+3)
            (3060409, 0.10),  # BlockShldrTG(+3)
            (3060403, 0.10),  # BlockShldrTD(+3)
            (3060309, 0.10),  # SoftShldrTG(+3)
            (3060306, 0.10),  # SoftShldrGUN(+3)
            (3060402, 0.09),  # BlockShldrTD(+2)
            (3060405, 0.08),  # BlockShldrGUN(+2)
            (3060408, 0.08),  # BlockShldrTG(+2)
            (3060401, 0.05),  # BlockShldrTD(+1)
            (3060407, 0.05),  # BlockShldrTG(+1)
            (3060404, 0.05)   # BlockShldrGUN(+1)
        ],

        BOX_MINI_BOT: [
            (3011504, 0.20),    # BabytankCRT(+2)
            (3011505, 0.20),    # BabytankMIS(+2)
            (3011506, 0.20),    # BabytankBST(+2)
            (3011601, 0.20),    # BeholderCRT(+1)
            (3011602, 0.20),    # BeholderMIS(+1)
            (3011603, 0.20),    # BeholderBST(+1)
            (3011507, 0.04),    # BabytankCRT(+3)
            (3011508, 0.03),    # BabytankMIS(+3)
            (3011509, 0.03)     # BabytankBST(+3)
        ],

        BOX_HEAD: [
            (1010601, 0.60),  # HyperDrillCRT(+1) — LandsliderMIS(+1) — SpikeHazardSP(+1)
            (1010602, 0.30),  # HyperDrillCRT(+2) — LandsliderMIS(+2) — SpikeHazardSP(+2)
            (1010603, 0.10)   # HyperDrillCRT(+3) — LandsliderMIS(+3) — SpikeHazardSP(+3)
        ],

        BOX_BODY: [
            (1020601, 0.60),  # HyperDrillTA(+1) — LandsliderBST(+1) — SpikeHazardMX(+1)
            (1020602, 0.30),  # HyperDrillTA(+2) — LandsliderBST(+2) — SpikeHazardMX(+2)
            (1020603, 0.10)   # HyperDrillTA(+3) — LandsliderBST(+3) — SpikeHazardMX(+3)
        ],

        BOX_ARMS: [
            (1030601, 0.60),  # HyperDrillTD(+1) — LandsliderGUN(+1) — SpikeHazardTG(+1)
            (1030602, 0.30),  # HyperDrillTD(+2) — LandsliderGUN(+2) — SpikeHazardTG(+2)
            (1030603, 0.10)   # HyperDrillTD(+3) — LandsliderGUN(+3) — SpikeHazardTG(+3)
        ]
    }
}