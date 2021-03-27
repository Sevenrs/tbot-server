CREATE TABLE `friends` (
	`id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'Incremental friend ID',
	`character_id_1` INT(11) NULL DEFAULT NULL COMMENT 'Character ID #1',
	`character_id_2` INT(11) NULL DEFAULT NULL COMMENT 'Character ID #2',
	`date` DATETIME NULL DEFAULT NULL COMMENT 'Date of creation',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1;