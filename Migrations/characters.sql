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
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `user_id` int(11) NOT NULL DEFAULT 0,
  `name` varchar(12) COLLATE utf8mb4_unicode_ci NOT NULL,
  `position` int(11) NOT NULL DEFAULT 0,
  `type` int(11) NOT NULL DEFAULT 1,
  `experience` int(11) NOT NULL DEFAULT 0,
  `level` int(11) NOT NULL DEFAULT 1,
  `rank_exp` int(11) NOT NULL DEFAULT 0,
  `rank` int(11) NOT NULL DEFAULT 0,
  `health` int(11) NOT NULL DEFAULT 1000,
  `luck` int(11) NOT NULL DEFAULT 0,
  `speed` int(11) NOT NULL DEFAULT 1000,
  `att_min` int(11) NOT NULL DEFAULT 50,
  `att_max` int(11) NOT NULL DEFAULT 55,
  `att_trans_min` int(11) NOT NULL DEFAULT 110,
  `att_trans_max` int(11) NOT NULL DEFAULT 125,
  `att_critical` int(11) NOT NULL DEFAULT 0,
  `att_evade` int(11) NOT NULL DEFAULT 0,
  `att_ranged` int(11) NOT NULL DEFAULT 1000,
  `trans_special` int(11) NOT NULL DEFAULT 0,
  `trans_guage` int(11) NOT NULL DEFAULT 1000,
  `trans_def` int(11) NOT NULL DEFAULT 0,
  `trans_att` int(11) NOT NULL DEFAULT 0,
  `trans_speed` int(11) NOT NULL DEFAULT 0,
  `currency_botstract` int(11) NOT NULL DEFAULT 0,
  `currency_gigas` int(11) NOT NULL DEFAULT 0,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table bout.characters: ~0 rows (approximately)
/*!40000 ALTER TABLE `characters` DISABLE KEYS */;
/*!40000 ALTER TABLE `characters` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
