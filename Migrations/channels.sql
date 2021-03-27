CREATE TABLE `channels` (
	`id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'Incremental channel ID',
	`world` INT(11) NULL DEFAULT NULL COMMENT 'World index',
	`name` VARCHAR(12) NULL DEFAULT NULL COMMENT 'Channel name' COLLATE 'utf8mb4_unicode_ci',
	`min_level` INT(11) NULL DEFAULT '1' COMMENT 'Minimum level',
	`max_level` INT(11) NULL DEFAULT '70' COMMENT 'Maxmimum level',
	`population` INT(11) NULL DEFAULT '0' COMMENT 'Amount of online clients',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1;