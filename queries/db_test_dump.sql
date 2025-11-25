-- --------------------------------------------------------
-- Host:                         mysql-1b17ab81-fintech2024mattiaforneron.g.aivencloud.com
-- Versione server:              8.0.35 - Source distribution
-- S.O. server:                  Linux
-- HeidiSQL Versione:            12.11.0.7065
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dump della struttura del database eurofork_test
CREATE DATABASE IF NOT EXISTS `eurofork_test` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `eurofork_test`;

-- Dump della struttura di tabella eurofork_test.alarms
CREATE TABLE IF NOT EXISTS `alarms` (
  `id_alarm` int NOT NULL AUTO_INCREMENT,
  `type` varchar(100) DEFAULT NULL,
  `description` varchar(400) DEFAULT NULL,
  PRIMARY KEY (`id_alarm`)
) ENGINE=InnoDB AUTO_INCREMENT=60 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dump dei dati della tabella eurofork_test.alarms: ~59 rows (circa)
INSERT INTO `alarms` (`id_alarm`, `type`, `description`) VALUES
	(1, 'Silent Warning', '#400 -  Missions Move In -  Tolerance correction'),
	(2, 'Silent Warning', '#300 -  Missions Movement -  Tolerance correction'),
	(3, 'Warning', '#306 -  Missions Movement -  Positioning failed'),
	(4, 'Warning', '#6002 - Mission LU Movement - Found overhung sensor'),
	(5, 'Warning', '#300 -  Missions Movement -  Barcode doesn\'t change during movement'),
	(6, 'Silent Warning', '#301 -  Missions Movement -  pump speed activated'),
	(7, 'Alarm', '#1 - Hardware - Safety circuit\'s intervention'),
	(8, 'Alarm', '#1000 -  General -  Safety circuit intervention'),
	(9, 'Alarm', '#1012 -  General -  Emergency From Shuttle'),
	(10, 'Warning', '#6004 - Mission LU Movement - Found the overhung sensor of the opposite side of the movement direction'),
	(11, 'Warning', '#1002 - Mission LU taking - Wrong taking positions, machine not in tolerance'),
	(12, 'Alarm', '#1004 - Mission LU taking - Overhung sensor not found'),
	(13, 'Warning', '#2 - General - LU\'s overhung'),
	(14, 'Warning', '#3001 - Mission Movement - Physical - logical TGLS\'s Incongruency'),
	(15, 'Alarm', '#4 - Hardware - Missing Safety Signal from ground'),
	(16, 'Alarm', '#1009 - Mission LU taking - Shuttle lost Rx sensor from TCS'),
	(17, 'Alarm', '#8 - Hardware - Movidrive\'s fault'),
	(18, 'Alarm', '#20 - General - Switching to manual mode with some hanged missions'),
	(19, 'Alarm', '#2006 -  Hardware -  Traction driver Fault'),
	(20, 'Alarm', '#1001 -  General -  Barcode doesn\'t change during manual movement'),
	(21, 'Warning', '#312 -  Missions Movement -  Expired cruise time'),
	(22, 'Warning', '#1 - General - Satellite\'s overhung'),
	(23, 'Warning', '#313 -  Missions Movement -  Expired ramp time down'),
	(24, 'Silent Warning', '#401 -  Missions Move In -  Machine pump speed activated'),
	(25, 'Warning', '#902 -  Missions Various -  Satellite is not in tolerance'),
	(26, 'Warning', '#6006 - Mission LU Movement - Exceded the max number of correction\'s retryes'),
	(27, 'Warning', '#3 - General - Shuttle Booked'),
	(28, 'Warning', '#500 -  Missions Move Out -  Barcode doesn\'t change during movement'),
	(29, 'Silent Warning', '#501 -  Missions Move Out -  Machine pump speed activated'),
	(30, 'Alarm', '#1007 -  General -  Missing barcode value in manual mode'),
	(31, 'Alarm', '#1005 -  General -  Lost FW rail sensors during manual movement'),
	(32, 'Alarm', '#1006 -  General -  Lost BW rail sensors during manual movement'),
	(33, 'Warning', '#308 -  Missions Movement -  Ghost pallet detected'),
	(34, 'Alarm', '#1003 -  General -  Machine in manual mode with active mission'),
	(35, 'Alarm', '#500 -  Missions Move Out -  Missing barcode value'),
	(36, 'Warning', '#406 -  Missions Move In -  First rail sensors not found'),
	(37, 'Alarm', '#1013 -  General -  Missing barcode value during correction'),
	(38, 'Alarm', '#304 -  Missions Movement -  Missing barcode value'),
	(39, 'Alarm', '#306 -  Missions Movement -  Positioning Lag Error'),
	(40, 'Warning', '#1004 - Mission LU taking - Overhung sensor not found'),
	(41, 'Warning', '#1001 - Mission LU taking - Physical - logical TGLS\'s Incongruency'),
	(42, 'Warning', '#204 -  Missions Leaving -  Wrong leaving position, machine is not in tolerance'),
	(43, 'Alarm', '#12 - Alarm Safe Position not OK (Datamatrix Profinet)'),
	(44, 'Alarm', '#24 - General - Satellite\'s overhung'),
	(45, 'Alarm', '#35 - Left side Light Curtain Receiver not ok'),
	(46, 'Alarm', '#34 - Right side Light Curtain Receiver not ok'),
	(47, 'Alarm', '#27 - General - Missing profiSAFE communication with Satellite'),
	(48, 'Alarm', '#1002 - Mission LU taking - Maximum execution time expired'),
	(49, 'Alarm', '#3 - Hardware - Pressed emergency button on backward side'),
	(50, 'Alarm', '#2 - Hardware - Pressed emergency button on forward side'),
	(51, 'Alarm', '#1011 -  General -  Emergency Button BW'),
	(52, 'Alarm', '#1010 -  General -  Emergency Button FW'),
	(53, 'Alarm', '#2003 -  Hardware -  Satellite\'s battery doesn\'t charge'),
	(54, 'Warning', '#311 -  Missions Movement -  Expired ramp time up'),
	(55, 'Alarm', '#2002 -  Hardware -  Satellite is not beeing charged for too much time'),
	(56, 'Warning', '#203 -  Missions Leaving -  Wrong TGLS, lifter is not high'),
	(57, 'Alarm', '#201 -  Missions Leaving -  Missing barcode value'),
	(58, 'Alarm', '#3004 - Mission Movement - Encoder value out of Bi Bf limits before the beginning of the mission'),
	(59, 'Alarm', '#2007 -  Hardware -  Lifter driver Fault');

-- Dump della struttura di tabella eurofork_test.job_orders
CREATE TABLE IF NOT EXISTS `job_orders` (
  `id_job_order` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) DEFAULT NULL,
  `nation` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_job_order`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dump dei dati della tabella eurofork_test.job_orders: ~3 rows (circa)
INSERT INTO `job_orders` (`id_job_order`, `name`, `nation`) VALUES
	(1, 'SaniFrutta', 'Italy'),
	(2, 'Jaguar Land Rover', 'United Kingdom'),
	(3, 'Orangina', 'France');

-- Dump della struttura di tabella eurofork_test.machines
CREATE TABLE IF NOT EXISTS `machines` (
  `id_machine` int NOT NULL AUTO_INCREMENT,
  `id_job_order` int DEFAULT NULL,
  `name` varchar(100) DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_machine`),
  KEY `fk_job_orders` (`id_job_order`),
  CONSTRAINT `fk_job_orders` FOREIGN KEY (`id_job_order`) REFERENCES `job_orders` (`id_job_order`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dump dei dati della tabella eurofork_test.machines: ~8 rows (circa)
INSERT INTO `machines` (`id_machine`, `id_job_order`, `name`, `type`) VALUES
	(1, 1, 'Shuttle 1', 'Frozen'),
	(2, 1, 'Satellite 1', 'Frozen'),
	(3, 1, 'Shuttle 2', 'Normal'),
	(4, 1, 'Satellite 2', 'Normal'),
	(5, 2, 'Shuttle 1', 'Normal'),
	(6, 2, 'Satellite 1', 'Normal'),
	(7, 3, '7N0101', 'Frozen'),
	(8, 3, '7S0101', 'Frozen');

-- Dump della struttura di tabella eurofork_test.micromissions
CREATE TABLE IF NOT EXISTS `micromissions` (
  `id_micromission` int NOT NULL AUTO_INCREMENT,
  `id_machine` int DEFAULT NULL,
  `type` varchar(100) DEFAULT NULL,
  `result` varchar(100) DEFAULT NULL,
  `date_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id_micromission`),
  KEY `fk_machines` (`id_machine`),
  CONSTRAINT `fk_machines` FOREIGN KEY (`id_machine`) REFERENCES `machines` (`id_machine`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dump dei dati della tabella eurofork_test.micromissions: ~10 rows (circa)
INSERT INTO `micromissions` (`id_micromission`, `id_machine`, `type`, `result`, `date_time`) VALUES
	(1, 7, '(10) Taking with chain', '(1) OK', '2025-10-01 08:00:00'),
	(2, 7, '(60) Positioning with chains', '(1) OK', '2025-10-01 09:00:00'),
	(3, 7, '(30) Move', '(200) Alarm Hardware', '2025-10-02 10:00:00'),
	(4, 7, '(30) Move', ' (1) OK', '2025-10-02 10:00:00'),
	(5, 8, '(10) Taking', '(1) OK', '2025-10-03 11:00:00'),
	(6, 8, '(50) Move out', '(1) OK', '2025-10-04 12:00:00'),
	(7, 8, '(30) Move', '(1) OK', '2025-10-04 12:00:00'),
	(8, 8, '(20) Leaving', '(1) OK', '2025-10-04 12:00:00'),
	(9, 8, '(30) Move', '(1) OK', '2025-10-04 12:00:00'),
	(10, 8, '(40) Move in', '(1) OK', '2025-10-04 12:00:00');

-- Dump della struttura di tabella eurofork_test.micromission_alarms
CREATE TABLE IF NOT EXISTS `micromission_alarms` (
  `id_micromission_alarm` int NOT NULL AUTO_INCREMENT,
  `id_micromission` int DEFAULT NULL,
  `id_alarm` int DEFAULT NULL,
  `trigger_datetime` datetime DEFAULT NULL,
  `value` varchar(10) DEFAULT NULL,
  PRIMARY KEY (`id_micromission_alarm`),
  KEY `fk_micromission` (`id_micromission`),
  KEY `fk_alarm` (`id_alarm`),
  CONSTRAINT `fk_alarm` FOREIGN KEY (`id_alarm`) REFERENCES `alarms` (`id_alarm`) ON DELETE CASCADE ON UPDATE CASCADE,
  CONSTRAINT `fk_micromission` FOREIGN KEY (`id_micromission`) REFERENCES `micromissions` (`id_micromission`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dump dei dati della tabella eurofork_test.micromission_alarms: ~0 rows (circa)
INSERT INTO `micromission_alarms` (`id_micromission_alarm`, `id_micromission`, `id_alarm`, `trigger_datetime`, `value`) VALUES
	(1, 3, 7, '2025-10-02 10:00:30', 'ON'),
	(2, 3, 7, '2025-10-02 11:00:35', 'OFF');

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
