### Bout Server
This repository contains the code to the Bout server

## Requirements
1. The following python packages are required: `mysql-connector` and `bcrypt`.
2. The database, run `sudo bash ./run-migrations.sh`

(sidenote, lib32-alsa-plugins lib32-libpulse lib32-openal are required for sound playback through wine32)

The items from the droptable are determined by the following query:
```
SELECT id, item_id, `name`, `level`, ABS(`level` - 61) AS `lvl_difference` FROM game_items WHERE `part_type` = 5 AND ABS(`level` - 61) <= 5 
	AND `name` LIKE '%(+%'ORDER BY ABS(`level` - 61) ASC
```