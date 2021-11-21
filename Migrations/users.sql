CREATE TABLE `users` (
	`id` BIGINT(20) NOT NULL AUTO_INCREMENT COMMENT 'Incremental User ID',
	`external_id` BIGINT(20) NULL DEFAULT NULL COMMENT 'tbot.icseon.com uid',
	`cash` INT(1) NOT NULL DEFAULT '0' COMMENT 'The amount of cash points this user owns',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `external_id` (`external_id`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB;