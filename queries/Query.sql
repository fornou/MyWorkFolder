-- Query to show the amount of data stored in the DB for each Job and for Micromissions & Alarms
SELECT 
	c.Nome AS Job_Name, 
	'Micromissioni' AS Tabel,
	COUNT(*) AS Amount_Data_For_Job
FROM 
	MicroMissioni m 
INNER JOIN 
	Commesse c 
ON 
	m.ID_Commessa = c.ID_Commessa
GROUP BY 
	m.ID_Commessa
UNION ALL
SELECT 
	c.Nome AS Job_Name, 
	'Allarmi' AS Tabel,
	COUNT(*) AS Amount_Data_For_Job
FROM 
	Allarmi a
INNER JOIN 
	Commesse c 
ON 
	a.ID_Commessa = c.ID_Commessa
GROUP BY 
	a.ID_Commessa;
	
-- Query to show the total amount of data stored in the DB (Micromissions & Alarms)
SELECT 
	'Micromissioni' AS Tabella, 
	COUNT(*) AS Amount_Data_Stored
FROM	
	MicroMissioni
UNION ALL
SELECT 
	'Allarmi' AS Tabella,
	COUNT(*) Amount_Data_Stored
FROM
	Allarmi;
	
-- Different Type of Alarm Description
SELECT
	DISTINCT Descrizione 
FROM
	Allarmi
WHERE
	Tipo LIKE 'Alarm';
	
-- Different Type of Result
SELECT
	DISTINCT Risultato 
FROM
	MicroMissioni;
	
-- Different Type of Result
SELECT
	DISTINCT Risultato 
FROM
	MicroMissioni;
	
	
SELECT DISTINCT Risultato FROM MicroMissioni;






























SELECT 
	Macchina,
	Tipo,
	Risultato,
	Livello_Batteria_Tx,
	Data_Ora_Tx
FROM 
	MicroMissioni
WHERE 
	Tipo LIKE '(92)%'
	AND Livello_Batteria_Tx > 75
	AND Macchina LIKE '%407'
	AND DATE(Data_Ora_Tx) BETWEEN '2025-09-22' AND '2025-09-28';

































	
	
	
	
	
	
	
	
	
	
	
	
	
	
SELECT
	*
FROM
	MicroMissioni
WHERE
	Macchina LIKE '7N0102'
	AND  Risultato NOT LIKE '(1) OK'
AND 
	DATE(Data_Ora_Rx) = '2025-06-02';
	
	
SELECT
	*
FROM
	Allarmi
WHERE 
	Macchina LIKE '7N0102'
AND 
	DATE(Data_Ora) = '2025-06-02'
AND
	Valore LIKE 'ON';
	
	
	
	
	
	
	
	
	
	
-- Different Type of Result	
SELECT
	DISTINCT Allarme 
FROM
	Associazioni
WHERE Tipo_Allarme='Alarm';
	

SELECT
	DISTINCT Allarme 
FROM
	Associazioni;
	
SELECT 
	*
FROM 
	Associazioni
WHERE
	Tipo_Macchina LIKE '7%';
	
SELECT Date(Data_Ora_Tx) FROM MicroMissioni LIMIT 1;
	



SELECT 
	SUM(Conteggio)
FROM(
	SELECT 
		COUNT(*) AS Conteggio,
		Risultato
	FROM 
		MicroMissioni 
	WHERE 
		Macchina LIKE '7N0101' 
		AND Risultato NOT LIKE '(1) OK'
		AND DATE(Data_Ora_Rx) = '2025-06-02'
	GROUP BY 
		Risultato	
)AS Cont_Ris;


DESCRIBE MicroMissioni;

SELECT CONCAT(
    'SELECT ''', COLUMN_NAME, ''' AS colonna, ', COLUMN_NAME, ' AS valore FROM Micromissioni GROUP BY ', COLUMN_NAME, ';'
) AS query_text
FROM INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'Micromissioni'
  AND TABLE_SCHEMA = 'Eurofork';
  
  DESCRIBE Allarmi;


-- Aggiunta associazioni:
-- (213) Invalid encoder value -> Alarm
-- (117) TG down waiting up --> Warning

INSERT INTO 
	Associazioni (Tipo_Macchina, Tipo_Allarme, Allarme)
VALUES
	('7S0','Alarm','(213) Invalid encoder value'),
	('7S0','Warning','(117) TG down waiting up');

	
SELECT
	Data_Ora_Rx,
	DATE(Data_Ora_rx),
	TIMESTAMP(Data_Ora_rx),
	TIMESTAMP(
      Data_Ora_Rx - INTERVAL SECOND(Data_Ora_Rx) SECOND
    )
FROM
	MicroMissioni

WHERE
	DATE(Data_Ora_Rx) = '2025-06-05'
AND
	Risultato != '(1) OK'
LIMIT 1;