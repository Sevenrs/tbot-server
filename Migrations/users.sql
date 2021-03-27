CREATE TABLE `users` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT 'Incremental User ID',
	`username` VARCHAR(12) NULL DEFAULT NULL COMMENT 'Username for account' COLLATE 'utf8mb4_unicode_ci',
	`password` VARCHAR(60) NULL DEFAULT NULL COMMENT 'Hashed and salted password' COLLATE 'utf8mb4_unicode_ci',
	`banned` INT(1) NOT NULL DEFAULT '0' COMMENT 'Whether or not this user has been banned',
	`active_bot_slot` INT(1) NOT NULL DEFAULT '0' COMMENT 'Number of the active character slot',
	`cash` INT(1) NOT NULL DEFAULT '0' COMMENT 'The amount of cash points this user owns',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `username` (`username`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1;