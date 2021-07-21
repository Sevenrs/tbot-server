from GameServer.Controllers.data.drops import *

# This table contains the experience points to award per planet level.
# Structure: Level index, easy, medium and hard difficulty awards
PLANET_MAP_TABLE = {
    0: ([100, 150, 200], 7.5),      # [Lv01]Training Camp
    1: ([125, 175, 250], 10.5),     # [Lv03]Base Camp
    2: ([150, 250, 300], 10.5),     # [Lv06]Camp-Spike
    3: ([500, 750, 1000], 15),      # [Lv08]Camp-Spike2
    4: ([250, 300, 500], 18),       # [Lv10]Planet-Alderan
    5: ([250, 430, 640], 19.5),     # [Lv13]Alderan-Entrance
    6: ([540, 780, 1334], 19.5),    # [Lv16]Mine-Alderan
    7: ([540, 780, 1334], 21),      # [Lv18]Mine-Alderan2
    8: ([600, 700, 900], 21),       # [Lv20]Mine-Blaster
    9: ([540, 680, 920], 22.5),     # [Lv23]Lava-Sea1
    10: ([560, 680, 920], 22.5),    # [Lv28]Lava-Sea2
    11: ([700, 800, 1240], 22.5),   # [Lv26]Lava-Sea3
    12: ([740, 850, 1480], 22.5),   # [Lv30]Acurin-Ruins1
    13: ([780, 870, 1500], 22.5),   # [Lv33]Acurin-Ruins2
    14: ([840, 980, 1040], 22.5),   # [Lv36]Planet-Acurin
    15: ([840, 980, 1040], 24),     # [Lv38]Planet-Acurin2
    16: ([980, 1040, 1220], 24),    # [Lv40]Port-Acurin
    17: ([1040, 1220, 1340], 24),   # [Lv43]Escape-Acurin
    18: ([840, 850, 960], 24),      # [Lv46]Planet-MECA
    19: ([840, 850, 960], 24),      # [Lv48]Planet-MECA2
    20: ([780, 830, 920], 24.5),    # [Lv50]Hidden-Archive
    21: ([840, 930, 1020], 25.5),   # [Lv53]Secret-passage
    22: ([950, 1060, 1170], 25.5),  # [Lv56]Destroy-all
    23: ([950, 1060, 1170], 25.5),  # [Lv58]Destroy-all2
    24: ([1288, 1450, 1650], 27),   # [Lv60]Escape-From-MECA
    25: ([1588, 1650, 1889], 27),   # [Lv63]MeraMountin
    26: ([1687, 1890, 1950], 27),   # [Lv66]MeraMountin2
    27: ([1799, 1905, 1980], 27),   # [Lv68]MeraMountin3
    28: ([1900, 2030, 2530], 27),   # [Lv70]MeraMountin4
    45: ([540, 760, 870], 18),      # [Lv08]The-Fallen([Elite)
    46: ([980, 1040, 1230], 36),    # [Lv18]Lava-Field([Elite)
    47: ([1020, 1430, 1560], 45),   # [Lv28]The-Pirate([Elite)
    48: ([1340, 1530, 1800], 45),   # [Lv38]Evil-Port([Elite)
    49: ([1560, 1890, 2050], 48),   # [Lv48]Bloodway(Elite)
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
        45, # Boss
        47
    ],

    # [Lv18]Mine-Alderan2
    7: [
        24 # Boss
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
        88, # Boss
        95,
        96,
        97
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
        71, # Boss
        76,
        78,
        79,
        77
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
        70, # Boss
        71,
        72,
        78,
        79,
        80
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
        97,  # Boss
        100,
        109,
        110
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
        98, # Boss
        99
    ],

    # [Lv63]MeraMountin
    25: [
        19,
        20,
        21,
        54,
        55,
        77,
        105,
        113, # Boss
        121,
        122,
        123
    ],

    # [Lv66]MeraMountin2
    26: [
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
    27: [
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
    28: [
        43,
        44,
        45,
        46,
        87,
        121, # Boss
        125
    ],

    # [Lv08]The-Fallen([Elite)
    45: [
        2,
        22,
        27,
        33  # Boss
    ],

    # [Lv18]Lava-Field([Elite)
    46: [
        25,
        33,
        34,
        35,
        50, # Boss
        52,
        53
    ],

    # [Lv28]The-Pirate([Elite)
    47: [
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
    48: [
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
    49: [
        30,
        37,
        49,
        50,
        61,
        70,
        72,
        83, # Boss
        89,
        90
    ]
}

# This table contains the mob table from which to increase the canister drop rate
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

    # [Lv63]MeraMountin
    25: [
        75
    ],

    # [Lv66]MeraMountin2
    26: [
        82
    ],

    # [Lv68]MeraMountin3
    27: [
        79
    ],

    # [Lv70]MeraMountin4
    28: [
        88
    ],

    # [Lv48]Bloodway(Elite)
    49: [
        60
    ]

}

PLANET_BOXES = {

    #[Lv01]Training Camp
    0: [
        (BOX_GUN, 0.50)
    ],

    # [Lv03]Base Camp
    1: [
        (BOX_GUN, 0.15)
    ],

    # [Lv06]Camp-Spike
    2: [
        (BOX_GUN, 0.15)
    ],

    # [Lv08]Camp-Spike2
    3: [
        (BOX_GUN, 0.15)
    ],

    # [Lv10]Planet-Alderan
    4: [
        (BOX_GUN, 0.15)
    ]
}

PLANET_DROPS = {

    #[Lv01]Training Camp
    0: {
        BOX_GUN: [
            (3021101, 0.60), # HydraGun(+1)
            (3021102, 0.25), # HydraGun(+2)
            (3021103, 0.15), # HydraGun(+3)
        ]
    },

    # [Lv03]Base Camp
    1: {
        BOX_GUN: [
            (3021101, 0.20),  # HydraGun(+1)
            (3021102, 0.70),  # HydraGun(+2)
            (3021103, 0.10),  # HydraGun(+3)
        ]
    },

    # [Lv06]Camp-Spike
    2: {
        BOX_GUN: [
            (3021101, 0.10),  # HydraGun(+1)
            (3021102, 0.50),  # HydraGun(+2)
            (3021103, 0.20),  # HydraGun(+3)
            (3021201, 0.20)   # smartGun(+1)
        ]
    },

    # [Lv08]Camp-Spike2
    3: {
        BOX_GUN: [
            (3021102, 0.30),  # HydraGun(+2)
            (3021103, 0.20),  # HydraGun(+3)
            (3021201, 0.40),  # smartGun(+1)
            (3021202, 0.10)   # smartGun(+2)
        ]
    },

    # [Lv10]Planet-Alderan
    4: {
        BOX_GUN: [
            (3021103, 0.40),  # HydraGun(+3)
            (3021201, 0.20),  # smartGun(+1)
            (3021202, 0.30),  # smartGun(+2)
            (3021202, 0.10)   # smartGun(+3)
        ]
    }
}