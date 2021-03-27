CREATE TABLE `guilds` (
	`id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'Incremental guild ID',
	`leader_character_id` INT(11) NULL DEFAULT NULL COMMENT 'Guild master character ID',
	`name` VARCHAR(50) NULL DEFAULT NULL COMMENT 'Guild name' COLLATE 'utf8mb4_unicode_ci',
	`notice` VARCHAR(50) NULL DEFAULT NULL COMMENT 'Guild notice' COLLATE 'utf8mb4_unicode_ci',
	`max_members` INT(11) NULL DEFAULT '10' COMMENT 'Guild maximum members',
	`created` DATETIME NULL DEFAULT NULL COMMENT 'Guild creation date and time',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `leader_character_id` (`leader_character_id`) USING BTREE,
	UNIQUE INDEX `name` (`name`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1;
