AllarmiDROP TABLE Commesse;


-- Creazione Tabella Commesse
CREATE TABLE `Commesse` (
	`ID_Commessa` INT NOT NULL,
	`Nome` VARCHAR(200) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	PRIMARY KEY (`ID_Commessa`) USING BTREE
)
COLLATE='utf8mb4_0900_ai_ci'
;


INSERT INTO Commesse(Nome) VALUES ('Bosal'), ('Orangina'), ('Tonno Callipo');

SELECT * FROM Commesse;

TRUNCATE Commesse;

DESCRIBE Commesse;


-- Creazione Tabella Allarmi
CREATE TABLE `Allarmi` (
	`ID_Allarme` INT NOT NULL AUTO_INCREMENT, 
	`ID_Commessa` INT NOT NULL,
	`Data_Ora` DATETIME NOT NULL,
	`Tipo` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Macchina` VARCHAR(200) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Valore` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Codice` VARCHAR(60) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Descrizione` VARCHAR(200) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	PRIMARY KEY (`ID_Allarme`) USING BTREE,
	INDEX `FK__Commessa` (`ID_Commessa`) USING BTREE,
	CONSTRAINT `FK_Allarmi_Commessa` FOREIGN KEY (`ID_Commessa`) REFERENCES `Commesse` (`ID_Commessa`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COLLATE='utf8mb4_0900_ai_ci'
;


SELECT * FROM Allarmi;

TRUNCATE Allarmi;


-- Creazione Tabella Micromissioni
CREATE TABLE `MicroMissioni` (
	`ID_Micromissione` INT NOT NULL AUTO_INCREMENT,
	`ID_Commessa` INT NOT NULL,
	`Data_Ora_Tx` DATETIME NOT NULL,
	`Macchina` VARCHAR(100) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Tipo` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Risultato` VARCHAR(50) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Data_Ora_Rx` DATETIME NOT NULL,
	`Quota_Finale_Teorica` INT NOT NULL,
	`PLC` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`UDC` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Cella` VARCHAR(50) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Quota_Finale_Effettiva` INT NOT NULL,
	`Inizio` INT NOT NULL,
	`Fine` INT NOT NULL,
	`Quota_Inizio` INT NOT NULL,
	`Data_Ora_Inizio` DATETIME NOT NULL,
	`Distanza` INT NOT NULL,
	`Durata` TIME NOT NULL,
	`Direzione` VARCHAR(20) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Stato_logico` VARCHAR(20) NOT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Indice_Micromissione` INT NOT NULL,
	`Numero_Micromissioni` INT NOT NULL,
	`Note` VARCHAR(100) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`Livello_Batteria_Tx` INT NOT NULL DEFAULT '0',
	`Livello_Batteria_Rx` INT NOT NULL DEFAULT '0',
	`Valore_encoder_Tx` INT NOT NULL,
	`Peso_UDC` INT NOT NULL,
	PRIMARY KEY (`ID_Micromissione`) USING BTREE,
	INDEX `FK__Commessa` (`ID_Commessa`) USING BTREE,
	CONSTRAINT `FK_MicroMissioni_Commessa` FOREIGN KEY (`ID_Commessa`) REFERENCES `Commesse` (`ID_Commessa`) ON UPDATE NO ACTION ON DELETE NO ACTION
)
COLLATE='utf8mb4_0900_ai_ci'
;

INSERT INTO Associazioni(`Tipo_Macchina`, `Tipo_Allarme`, `Allarme`) VALUES ('Satellite', 'Warning', '(24) OK quota teorica');



-- Test Inserimento nella Tabella Micromissioni
INSERT INTO MicroMissioni (
    `ID_Commessa`, `Macchina`, `Tipo`, `Risultato`, 
    `Data_Ora_Inizio`, `Data_Ora_Tx`, `Data_Ora_Rx`, 
    `Quota_Finale_Teorica`, `Quota_Inizio`, `Quota_Finale_Effettiva`, `Distanza`, 
    `Durata`, `PLC`, `UDC`, `Cella`, `Inizio`, `Fine`, 
    `Direzione`, `Stato_logico`, `Indice_Micromissione`, 
    `Numero_Micromissioni`, `Note`, `Livello_Batteria_Tx`, 
    `Livello_Batteria_Rx`, `Valore_encoder_Tx`, `Peso_UDC`
) VALUES (
    1, 'Shuttle2', '(92) Abilita batteria', '(1) OK',
    
    '2022-05-29 18:07:00', '2022-05-29 18:07:00', '2022-05-29 18:07:00', 
    
    84257, 84254, 80700, 85000,
    
    '00:00:01', 0, NULL, 'Lift2', 3, 0,
	 
	  NULL, 'Unknown', 1, 1, 
	  
    NULL, 99, 99, 84257, 0
);

SELECT COUNT(*) FROM MicroMissioni WHERE ID_Commessa = 1;#13k
SELECT COUNT(*) FROM MicroMissioni WHERE ID_Commessa = 2;#111k
SELECT COUNT(*) FROM MicroMissioni WHERE ID_Commessa = 3;#36k

SELECT * FROM MicroMissioni WHERE ID_Commessa = 2 LIMIT 20;

SELECT DISTINCT Risultato FROM MicroMissioni;

TRUNCATE MicroMissioni;

DELETE FROM MicroMissioni WHERE ID_Commessa = 3;

SELECT DISTINCT 
	Tipo
FROM
	MicroMissioni
WHERE 
	ID_Commessa = 1
ORDER BY
	Tipo ASC;
	
SELECT DISTINCT 
	Tipo
FROM
	MicroMissioni
WHERE 
	ID_Commessa = 2
ORDER BY
	Tipo ASC;

1.0080015610224888e+17



# Test inner join su chiave straniera
SELECT 
	c.ID_Commessa,
	c.Nome,
	m.Macchina
FROM 
	MicroMissioni m
INNER JOIN 
	Commesse c
	ON c.ID_Commessa = m.ID_Commessa
WHERE
	m.ID_Micromissione = 1
	
	
	
SELECT 
	table_name AS tabella,
   ROUND((data_length + index_length) / 1024 / 1024, 2) AS size_mb
FROM 
	information_schema.tables
WHERE 
	table_schema = 'Eurofork'
ORDER BY 
	size_mb DESC;
	
SELECT DISTINCT
	Date(Data_Ora_Inizio)
FROM
	MicroMissioni
WHERE
	ID_Commessa = 2
ORDER BY
	DATE(Data_Ora_Inizio)

-- Date() toglie l'ora
-- Dayofweek() mi restituisce il giorno in numero della settimana Domenica = 1
-- Interval() aggiunge 5 giorni --> 6
-- %7 --> 6 giorni che mancano a lunedì di quella settimana
-- Date() - 6 = trova la data del lunedì inizio settimana
SELECT 
	DATE(Data_Ora_Inizio) - INTERVAL (DAYOFWEEK(Data_Ora_Inizio) + 5) % 7 DAY AS inizio_settimana, 
	COUNT(*) AS numero_di_righe
FROM 
	MicroMissioni m
INNER JOIN
	Commesse c
	ON m.ID_Commessa = c.ID_Commessa
WHERE 
	c.Nome = 'Orangina'
GROUP BY 
	inizio_settimana
HAVING
	inizio_settimana IS NOT NULL
ORDER BY 
	inizio_settimana;
	
	
	
	
	
SELECT DISTINCT 
	Macchina 
FROM
	MicroMissioni
WHERE 
	ID_Commessa = 3
	
	
	
	
	-- Per lo Shuttle4 per la commessa 2 Tonno Callippo
select 
    a.Tipo,
    a.Codice,
    a.Descrizione,
    m.Risultato,
    a.Data_Ora,
    m.Data_Ora_Rx
from    
    Allarmi a
inner join
    MicroMissioni m
    on m.ID_Commessa = a.ID_Commessa
    AND TIMESTAMP(a.Data_Ora) = TIMESTAMP(m.Data_Ora_Rx - INTERVAL SECOND(m.Data_Ora_Rx) SECOND)
where 
    a.ID_Commessa = 2
    and a.Valore = 'ON'
    -- and a.Macchina not in('H1', 'H2')
    and a.Macchina = 'Satellite1'
    and m.Macchina not in('Lift1', 'Lift2')
    and a.Codice != 'DB106.DBX14.0'
    and m.Risultato not in ('(1) OK', '(21) Ok silent warning', '')
    
    
    


	