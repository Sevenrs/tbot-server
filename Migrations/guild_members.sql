CREATE TABLE `guild_members` (
	`id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'Incremental guild ID',
	`character_id` INT(11) NOT NULL DEFAULT '0' COMMENT 'Guild member character ID',
	`guild_id` INT(11) NOT NULL DEFAULT '0' COMMENT 'Guild ID this member belongs to',
	`points` INT(11) NOT NULL DEFAULT '0' COMMENT 'Guild points this member has aquired',
	`applying` INT(11) NOT NULL DEFAULT '0' COMMENT 'Application status of member',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `character_id` (`character_id`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1;