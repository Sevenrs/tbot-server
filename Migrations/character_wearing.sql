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

-- Dumping structure for table bout.character_wearing
CREATE TABLE IF NOT EXISTS `character_wearing` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `character_id` int(11) NOT NULL DEFAULT 0 COMMENT 'Character ID to link this table to',
  `head` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing head',
  `body` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing body',
  `arms` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing arms',
  `mini-bot` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing mini-bot',
  `gun` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing gun',
  `ef` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing E.F field',
  `wing` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing wings',
  `shield` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing shields',
  `shoulder` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing shoulders',
  `flag1` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for the first wearing flag',
  `flag2` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for the secondary wearing flag',
  `passive_skill` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing passive skill',
  `attack_skill` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing attack skill',
  `field_pack` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing field pack',
  `trans_pack` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing transformation pack',
  `merc1` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing primary mercenary',
  `merc2` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing secondary mercenary',
  `coin_head` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing a coin head',
  `coin_minibot` int(11) NOT NULL DEFAULT 0 COMMENT 'Reference to character_items for wearing a coin mini-bot',
  PRIMARY KEY (`id`),
  UNIQUE KEY `character_id` (`character_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dumping data for table bout.character_wearing: ~0 rows (approximately)
/*!40000 ALTER TABLE `character_wearing` DISABLE KEYS */;
/*!40000 ALTER TABLE `character_wearing` ENABLE KEYS */;

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
