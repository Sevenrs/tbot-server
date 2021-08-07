from GameServer.Controllers.data.drops import *

# This table contains the experience points to award per planet level.
# Structure: Level index, easy, medium and hard difficulty awards
PLANET_MAP_TABLE = {
    0: ([100, 150, 200], 7.5, 1),       # [Lv01]Training Camp
    1: ([125, 175, 250], 10.5, 3),      # [Lv03]Base Camp
    2: ([150, 250, 300], 10.5, 6),      # [Lv06]Camp-Spike
    3: ([500, 750, 1000], 15, 8),       # [Lv08]Camp-Spike2
    4: ([250, 300, 500], 18, 10),       # [Lv10]Planet-Alderan
    5: ([250, 430, 640], 19.5, 13),     # [Lv13]Alderan-Entrance
    6: ([540, 780, 1334], 19.5, 16),    # [Lv16]Mine-Alderan
    7: ([540, 780, 1334], 21, 18),      # [Lv18]Mine-Alderan2
    8: ([600, 700, 900], 21, 20),       # [Lv20]Mine-Blaster
    9: ([540, 680, 920], 22.5, 23),     # [Lv23]Lava-Sea1
    10: ([560, 680, 920], 22.5, 26),    # [Lv26]Lava-Sea2
    11: ([700, 800, 1240], 22.5, 28),   # [Lv28]Lava-Sea3
    12: ([740, 850, 1480], 22.5, 30),   # [Lv30]Acurin-Ruins1
    13: ([780, 870, 1500], 22.5, 33),   # [Lv33]Acurin-Ruins2
    14: ([840, 980, 1040], 22.5, 36),   # [Lv36]Planet-Acurin
    15: ([840, 980, 1040], 24, 38),     # [Lv38]Planet-Acurin2
    16: ([980, 1040, 1220], 24, 40),    # [Lv40]Port-Acurin
    17: ([1040, 1220, 1340], 24, 43),   # [Lv43]Escape-Acurin
    18: ([840, 850, 960], 24, 46),      # [Lv46]Planet-MECA
    19: ([840, 850, 960], 24, 48),      # [Lv48]Planet-MECA2
    20: ([780, 830, 920], 24.5, 50),    # [Lv50]Hidden-Archive
    21: ([840, 930, 1020], 25.5, 53),   # [Lv53]Secret-passage
    22: ([950, 1060, 1170], 25.5, 56),  # [Lv56]Destroy-all
    23: ([950, 1060, 1170], 25.5, 58),  # [Lv58]Destroy-all2
    24: ([1288, 1450, 1650], 27, 60),   # [Lv60]Escape-From-MECA
    25: ([1588, 1650, 1889], 27, 63),   # [Lv63]MeraMountin
    26: ([1687, 1890, 1950], 27, 66),   # [Lv66]MeraMountin2
    27: ([1799, 1905, 1980], 27, 68),   # [Lv68]MeraMountin3
    28: ([1900, 2030, 2530], 27, 70),   # [Lv70]MeraMountin4
    29: ([540, 760, 870], 18, 8),       # [Lv08]The-Fallen(Elite)
    30: ([980, 1040, 1230], 36, 18),    # [Lv18]Lava-Field(Elite)
    31: ([1020, 1430, 1560], 45, 28),   # [Lv28]The-Pirate(Elite)
    32: ([1340, 1530, 1800], 45, 38),   # [Lv38]Evil-Port(Elite)
    33: ([1560, 1890, 2050], 48, 48),   # [Lv48]Bloodway(Elite)
}

# This table contains the mob table from which to drops boxes from

# This table contains the mob table from which to increase the canister drop rate
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

    # [Lv63]MeraMountin
    25: [
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
        125,
        121 # Boss
    ],

    # [Lv08]The-Fallen([Elite)
    29: [
        2,
        22,
        27,
        33  # Boss
    ],

    # [Lv18]Lava-Field([Elite)
    30: [
        25,
        33,
        34,
        35,
        52,
        53,
        50 # Boss
    ],

    # [Lv28]The-Pirate([Elite)
    31: [
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
    32: [
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
    33: [
        30,
        37,
        49,
        50,
        61,
        70,
        72,
        89,
        90,
        83 # Boss
    ]
}
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
    33: [
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
    ],

    # [Lv13]Alderan-Entrance
    5: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv16]Mine-Alderan
    6: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv18]Mine-Alderan2
    7: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv20]Mine-Blaster
    8: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv23]Lava-Sea1
    9: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv26]Lava-Sea2
    10: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv28]Lava-Sea3
    11: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv30]Acurin-Ruins1
    12: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv33]Acurin-Ruins2
    13: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv36]Planet-Acurin
    14: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv38]Planet-Acurin2
    15: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv40]Port-Acurin
    16: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv43]Escape-Acurin
    17: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv46]Planet-MECA
    18: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv48]Planet-MECA2
    19: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv50]Hidden-Archive
    20: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv53]Secret-passage
    21: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv56]Destroy-all
    22: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv58]Destroy-all2
    23: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv60]Escape-From-MECA
    24: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv63]MeraMountin
    25: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv66]MeraMountin2
    26: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv68]MeraMountin3
    27: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv70]MeraMountin4
    28: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv08]The-Fallen(Elite)
    29: [
        (BOX_GUN, 0.15)
    ],

    # [Lv18]Lava-Field(Elite)
    30: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv28]The-Pirate(Elite)
    31: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv38]Evil-Port(Elite)
    32: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ],

    # [Lv48]Bloodway(Elite)
    33: [
        (BOX_GUN, 0.15),
        (BOX_SHIELD, 0.15)
    ]
}

PLANET_DROPS = {

    #[Lv01]Training Camp
    0: {
        BOX_GUN: [
            (3021101, 0.60), # HydraGun(+1)
            (3021102, 0.25), # HydraGun(+2)
            (3021103, 0.15)  # HydraGun(+3)
        ]
    },

    # [Lv03]Base Camp
    1: {
        BOX_GUN: [
            (3021101, 0.20), # HydraGun(+1)
            (3021102, 0.70), # HydraGun(+2)
            (3021103, 0.10)  # HydraGun(+3)
        ]
    },

    # [Lv06]Camp-Spike
    2: {
        BOX_GUN: [
            (3021101, 0.10), # HydraGun(+1)
            (3021102, 0.50), # HydraGun(+2)
            (3021103, 0.20), # HydraGun(+3)
            (3021201, 0.20)  # smartGun(+1)
        ]
    },

    # [Lv08]Camp-Spike2
    3: {
        BOX_GUN: [
            (3021102, 0.30), # HydraGun(+2)
            (3021103, 0.20), # HydraGun(+3)
            (3021201, 0.40), # smartGun(+1)
            (3021202, 0.10)  # smartGun(+2)
        ]
    },

    # [Lv10]Planet-Alderan
    4: {
        BOX_GUN: [
            (3021103, 0.40), # HydraGun(+3)
            (3021201, 0.20), # smartGun(+1)
            (3021202, 0.30), # smartGun(+2)
            (3021202, 0.10)  # smartGun(+3)
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
        ]
    },

    # [Lv63]MeraMountin
    25: {
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
        ]
    },

    # [Lv66]MeraMountin2
    26: {
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
        ]
    },

    # [Lv68]MeraMountin3
    27: {
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
        ]
    },

    # [Lv70]MeraMountin4
    28: {
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
        ]
    },

    # [Lv08]The-Fallen(Elite)
    29: {
        BOX_GUN: [
            (3021202, 0.40), # smartGun(+2)
            (3021103, 0.30), # smartGun(+2)
            (3021102, 0.20), # smartGun(+2)
            (3021201, 0.10)  # smartGun(+2)
        ]
    },

    # [Lv18]Lava-Field(Elite)
    30: {
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
        ]
    },

    # [Lv28]The-Pirate(Elite)
    31: {
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
        ]
    },

    # [Lv38]Evil-Port(Elite)
    32: {
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
        ]
    },

    # [Lv48]Bloodway(Elite)
    33: {
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
        ]
    }
}