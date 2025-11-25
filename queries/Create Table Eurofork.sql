-- Dump della struttura del database Eurofork
CREATE DATABASE IF NOT EXISTS `Eurofork` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;
USE `Eurofork`;

-- Dump della struttura di tabella Eurofork.Allarmi
CREATE TABLE IF NOT EXISTS `Allarmi` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `Data_Ora` datetime DEFAULT NULL,
  `Tipo` varchar(150) DEFAULT NULL,
  `Macchina` varchar(150) DEFAULT NULL,
  `Valore` varchar(10) DEFAULT NULL,
  `Codice` varchar(150) DEFAULT NULL,
  `Descrizione` varchar(150) DEFAULT NULL,
  `ID_Commessa` int NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `ix_Allarmi_ID` (`ID`),
  KEY `Allarmi_ibfk_1` (`ID_Commessa`),
  CONSTRAINT `Allarmi_ibfk_1` FOREIGN KEY (`ID_Commessa`) REFERENCES `Commesse` (`ID_Commessa`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=8165 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dump della struttura di tabella Eurofork.Associazioni
CREATE TABLE IF NOT EXISTS `Associazioni` (
  `ID_Associazione` int NOT NULL AUTO_INCREMENT,
  `Tipo_Macchina` varchar(50) DEFAULT NULL,
  `Tipo_Allarme` varchar(50) DEFAULT NULL,
  `Allarme` varchar(150) DEFAULT NULL,
  PRIMARY KEY (`ID_Associazione`)
) ENGINE=InnoDB AUTO_INCREMENT=47 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dump della struttura di tabella Eurofork.Commesse
CREATE TABLE IF NOT EXISTS `Commesse` (
  `ID_Commessa` int NOT NULL AUTO_INCREMENT,
  `Nome` varchar(255) NOT NULL,
  PRIMARY KEY (`ID_Commessa`),
  KEY `ix_Commesse_ID_Commessa` (`ID_Commessa`)
) ENGINE=InnoDB AUTO_INCREMENT=7 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dump della struttura di tabella Eurofork.LivelloMacchine
CREATE TABLE IF NOT EXISTS `LivelloMacchine` (
  `id_livello_macchine` int NOT NULL AUTO_INCREMENT,
  `ID_Commessa` int DEFAULT NULL,
  `Macchina` varchar(100) DEFAULT NULL,
  `Numero_Macchina` varchar(100) DEFAULT NULL,
  `Livello` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`id_livello_macchine`),
  KEY `fk_commesse` (`ID_Commessa`),
  CONSTRAINT `fk_commesse` FOREIGN KEY (`ID_Commessa`) REFERENCES `Commesse` (`ID_Commessa`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=146 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- Dump della struttura di tabella Eurofork.MicroMissioni
CREATE TABLE IF NOT EXISTS `MicroMissioni` (
  `ID_Micromissione` int NOT NULL AUTO_INCREMENT,
  `Data_Ora_Tx` datetime DEFAULT NULL,
  `Macchina` varchar(100) DEFAULT NULL,
  `Tipo` varchar(50) DEFAULT NULL,
  `Risultato` varchar(50) DEFAULT NULL,
  `Data_Ora_Rx` datetime DEFAULT NULL,
  `Quota_Finale_Teorica` int DEFAULT NULL,
  `PLC` varchar(50) DEFAULT NULL,
  `UDC` varchar(50) DEFAULT NULL,
  `Cella` varchar(50) DEFAULT NULL,
  `Quota_Finale_Effettiva` int DEFAULT NULL,
  `Inizio` int DEFAULT NULL,
  `Fine` int DEFAULT NULL,
  `Quota_Inizio` int DEFAULT NULL,
  `Data_Ora_Inizio` datetime DEFAULT NULL,
  `Distanza` int DEFAULT NULL,
  `Durata` time DEFAULT NULL,
  `Direzione` varchar(20) DEFAULT NULL,
  `Stato_logico` varchar(20) DEFAULT NULL,
  `Indice_Micromissione` int DEFAULT NULL,
  `Numero_Micromissioni` int DEFAULT NULL,
  `Note` varchar(100) DEFAULT NULL,
  `Livello_Batteria_Tx` int DEFAULT NULL,
  `Livello_Batteria_Rx` int DEFAULT NULL,
  `Valore_encoder_Tx` int DEFAULT NULL,
  `Peso_UDC` int DEFAULT NULL,
  `ID_Commessa` int NOT NULL,
  PRIMARY KEY (`ID_Micromissione`),
  KEY `MicroMissioni_ibfk_1` (`ID_Commessa`),
  CONSTRAINT `MicroMissioni_ibfk_1` FOREIGN KEY (`ID_Commessa`) REFERENCES `Commesse` (`ID_Commessa`) ON DELETE CASCADE ON UPDATE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=697453 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

