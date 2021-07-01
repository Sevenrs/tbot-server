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
    10: ([560, 680, 920], 22.5),    # [Lv26]Lava-Sea2
    11: ([700, 800, 1240], 22.5),   # [Lv26]Lava-Sea3
    12: ([740, 850, 1480], 22.5),   # [Lv30]Acurin-Ruins1
    13: ([780, 870, 1500], 22.5),   # [Lv33]Acurin-Ruins2
    14: ([840, 980, 1040], 22.5),   # [Lv36]Planet-Acurin
    15: ([840, 980, 1040], 24),     # [Lv36]Planet-Acurin2
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