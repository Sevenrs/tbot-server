-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               10.5.10-MariaDB - Arch Linux
-- Server OS:                    Linux
-- HeidiSQL Version:             11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for bout
CREATE DATABASE IF NOT EXISTS `bout` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */;
USE `bout`;

-- Dumping structure for table bout.characters
CREATE TABLE IF NOT EXISTS `characters` (
    `id` INT(11) NOT NULL AUTO_INCREMENT,
	`user_id` INT(11) NOT NULL DEFAULT '0',
	`name` VARCHAR(13) NOT NULL COLLATE 'utf8mb4_unicode_ci',
	`position` INT(11) NOT NULL DEFAULT '0',
	`type` INT(11) NOT NULL DEFAULT '1',
	`experience` INT(11) NOT NULL DEFAULT '0',
	`level` INT(11) NOT NULL DEFAULT '1',
	`rank_exp` INT(11) NOT NULL DEFAULT '0',
	`rank` INT(11) NOT NULL DEFAULT '0',
	`health` INT(11) NOT NULL DEFAULT '7840',
	`luck` INT(11) NOT NULL DEFAULT '0',
	`speed` INT(11) NOT NULL DEFAULT '1000',
	`att_min` INT(11) NOT NULL DEFAULT '448',
	`att_max` INT(11) NOT NULL DEFAULT '627',
	`att_trans_min` INT(11) NOT NULL DEFAULT '896',
	`att_trans_max` INT(11) NOT NULL DEFAULT '1254',
	`att_critical` INT(11) NOT NULL DEFAULT '0',
	`att_evade` INT(11) NOT NULL DEFAULT '0',
	`att_ranged` INT(11) NOT NULL DEFAULT '1000',
	`trans_special` INT(11) NOT NULL DEFAULT '0',
	`trans_guage` INT(11) NOT NULL DEFAULT '1000',
	`trans_def` INT(11) NOT NULL DEFAULT '0',
	`trans_att` INT(11) NOT NULL DEFAULT '1000',
	`trans_speed` INT(11) NOT NULL DEFAULT '0',
	`currency_botstract` INT(11) NOT NULL DEFAULT '0',
	`currency_gigas` INT(11) NOT NULL DEFAULT '0',
	PRIMARY KEY (`id`) USING BTREE,
	UNIQUE INDEX `name` (`name`) USING BTREE
)
COLLATE='utf8mb4_unicode_ci' ENGINE=InnoDB;


-- Dumping data for table bout.characters: ~0 rows (approximately)
/*!40000 ALTER TABLE `characters` DISABLE KEYS */;
/*!40000 ALTER TABLE `characters` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
