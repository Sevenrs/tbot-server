CREATE TABLE `inbox` (
	`id` INT(11) NOT NULL AUTO_INCREMENT COMMENT 'Incremental message ID',
	`sender_character_id` INT(11) NOT NULL DEFAULT '0' COMMENT 'Character ID of sender',
	`receiver_character_id` INT(11) NOT NULL DEFAULT '0' COMMENT 'Character ID of receiver',
	`message` VARCHAR(90) NULL DEFAULT NULL COMMENT 'Message content' COLLATE 'utf8mb4_unicode_ci',
	`date` DATETIME NULL DEFAULT NULL COMMENT 'Message send date',
	PRIMARY KEY (`id`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1;