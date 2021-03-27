CREATE TABLE `characters` (
	`id` INT(11) NOT NULL AUTO_INCREMENT,
	`user_id` INT(11) NULL DEFAULT '0',
	`name` VARCHAR(12) NULL DEFAULT NULL COLLATE 'utf8mb4_unicode_ci',
	`position` INT(11) NULL DEFAULT '0',
	`type` INT(11) NULL DEFAULT '1',
	`experience` INT(11) NULL DEFAULT '0',
	`level` INT(11) NULL DEFAULT '1',
	`rank_exp` INT(11) NULL DEFAULT '0',
	`rank` INT(11) NULL DEFAULT '0',
	`health` INT(11) NULL DEFAULT '1000',
	`luck` INT(11) NULL DEFAULT '0',
	`speed` INT(11) NULL DEFAULT '1000',
	`att_min` INT(11) NULL DEFAULT '300',
	`att_max` INT(11) NULL DEFAULT '450',
	`att_trans_min` INT(11) NULL DEFAULT '600',
	`att_trans_max` INT(11) NULL DEFAULT '1200',
	`att_critical` INT(11) NULL DEFAULT '0',
	`att_evade` INT(11) NULL DEFAULT '0',
	`att_ranged` INT(11) NULL DEFAULT '0',
	`trans_special` INT(11) NULL DEFAULT '0',
	`trans_guage` INT(11) NULL DEFAULT '1000',
	`trans_def` INT(11) NULL DEFAULT '0',
	`trans_att` INT(11) NULL DEFAULT '0',
	`trans_speed` INT(11) NULL DEFAULT '0',
	`currency_botstract` INT(11) NULL DEFAULT '0',
	`currency_gigas` INT(11) NULL DEFAULT '0',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `name` (`name`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci'
ENGINE=InnoDB
AUTO_INCREMENT=1;