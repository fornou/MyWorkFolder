-- --------------------------------------------------------------------------------------------
-- Scheda 1: Generic
-- --------------------------------------------------------------------------------------------

-- Amount of Records in DB for Job Name
-- Mostra il totale di dati presenti in MicroMissioni e Allarmi per ogni Commessa
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

-- Total Amount of Records in DB
-- Mostra il totale di dati presenti in Micromissioni e Allarmi
SELECT 
	'Micromissioni' AS Tabel, 
	COUNT(*) AS Amount_Data_Stored
FROM	
	MicroMissioni
UNION ALL
SELECT 
	'Allarmi' AS Tabel,
	COUNT(*) Amount_Data_Stored
FROM
	Allarmi;
	

-- --------------------------------------------------------------------------------------------
-- Scheda 2: Info Job Order
-- --------------------------------------------------------------------------------------------

-- Data Over Time
-- Mostra la distribuzione dei dati nel tempo
SELECT 
    DATE_FORMAT(lunedi, '%d/%m/%Y') AS lunedi_inizio_settimana,
    COUNT(*) AS numero_risultati
FROM (
    SELECT 
        DATE(t.Data) - INTERVAL (DAYOFWEEK(t.Data) + 5) % 7 DAY AS lunedi
    FROM (
        SELECT ID_Commessa, Data_Ora_Inizio AS Data, 'MicroMissioni' AS Tipo FROM MicroMissioni
        UNION ALL
        SELECT ID_Commessa, Data_Ora AS Data, 'Allarmi' AS Tipo FROM Allarmi
    ) AS t
    INNER JOIN Commesse ON t.ID_Commessa = Commesse.ID_Commessa
    WHERE Commesse.Nome = {{Commessa}}
      AND t.Tipo = {{Table}}
      AND t.Data IS NOT NULL
) AS sub
GROUP BY lunedi
ORDER BY lunedi ASC;

-- Amount of machines
-- Mostra la quantità di macchine presenti in una commessa in base alla tabella selezionata
SELECT 
   COUNT(DISTINCT(t.Macchina)) AS Number_Machines
FROM (
    SELECT 
        ID_Commessa, 
        Macchina, 
        'MicroMissioni' AS Tipo 
    FROM
        MicroMissioni
    UNION ALL
    SELECT 
        ID_Commessa,
        Macchina,
        'Allarmi' AS Tipo 
    FROM Allarmi
) AS t
INNER JOIN 
    Commesse 
    ON t.ID_Commessa = Commesse.ID_Commessa
WHERE 
    Commesse.Nome = {{Commessa}}
    AND t.Tipo = {{Table}};
    
-- All Machines and levels
SELECT 
    t.Macchina,
    LivelloMacchine.Numero_Macchina,
    LivelloMacchine.Livello
FROM (
    SELECT 
        ID_Commessa, 
        Macchina, 
        'MicroMissioni' AS Tipo 
    FROM
        MicroMissioni
    UNION ALL
    SELECT 
        ID_Commessa,
        Macchina,
        'Allarmi' AS Tipo 
    FROM Allarmi
) AS t
INNER JOIN 
    Commesse 
    ON t.ID_Commessa = Commesse.ID_Commessa
INNER JOIN  
    LivelloMacchine
    ON LivelloMacchine.ID_Commessa = Commesse.ID_Commessa
WHERE 
    Commesse.Nome = {{Commessa}}
    AND t.Tipo = {{Table}}
    AND LivelloMacchine.Macchina = t.Macchina
GROUP BY
    t.Macchina,
    LivelloMacchine.Numero_Macchina,
    LivelloMacchine.Livello
ORDER BY
    LivelloMacchine.Livello;


-- --------------------------------------------------------------------------------------------
-- Scheda 3: Leaving/ Taking with chains
-- --------------------------------------------------------------------------------------------

-- Daily Leaving/ Taking with chains for each result and machine
-- Mostra una tabella con la quantità di missioni giornaliere di presa e consegna con catena per macchina e per risultato
SELECT
    Tipo,
    Date(Data_Ora_inizio) AS Data,
    COUNT(*) AS Quantità,
    Macchina,
    Risultato
FROM
    MicroMissioni
INNER JOIN 
    Commesse
    ON MicroMissioni.ID_Commessa = Commesse.ID_Commessa
WHERE   
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND {{Tipo_Missione}}
    AND {{Risultato}}
GROUP BY
    Data,
    Tipo,
    Macchina,
    Risultato
ORDER BY
    Macchina ASC,
    Tipo ASC,
    Data ASC;

-- Amount of Leaving/ Taking with chains for each result 
-- Mostra il totale di missioni di presa e consegna con catena per risultato
SELECT
  Tipo,
  COUNT(*) AS Quantità,
  Macchina,
  Risultato
FROM 
    MicroMissioni 
INNER JOIN 
    Commesse 
    ON MicroMissioni.ID_Commessa = Commesse.ID_Commessa
WHERE
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND {{Tipo_Missione}}
    AND {{Risultato}}
GROUP BY 
    Tipo,
    Macchina,
    Risultato
ORDER BY 
    Macchina,
    Risultato;

-- Amount of Taking with chains for each result and machine 
-- Mostra il totale di missioni di presa con catena per risultato e macchina
SELECT
  Tipo,
  COUNT(*) AS Quantità,
  Macchina,
  Risultato
FROM 
    MicroMissioni 
INNER JOIN 
    Commesse 
    ON MicroMissioni.ID_Commessa = Commesse.ID_Commessa
WHERE
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND MicroMissioni.Tipo = '(10) Taking with chain'
    AND {{Risultato}}
GROUP BY 
    Tipo,
    Macchina,
    Risultato
ORDER BY
    Macchina,
    Risultato;

-- Amount of Leaving with chains for each result and machine
-- Mostra il totale di missioni di consegna con catena per risultato e macchina
SELECT
  COUNT(*) AS Quantità,
  Macchina,
  Risultato
FROM 
    MicroMissioni 
INNER JOIN 
    Commesse 
    ON MicroMissioni.ID_Commessa = Commesse.ID_Commessa
WHERE
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND MicroMissioni.Tipo = '(20) Leaving with chain'
    AND {{Risultato}}
GROUP BY 
    Macchina,
    Risultato
ORDER BY
    Macchina,
    Risultato;

-- Amount of Leaving/ Taking with chains for each result and machine
-- Mostra il totale di missioni di presa e/o consegna con catena per risultato e macchina
SELECT
  Tipo,
  COUNT(*) AS Quantità,
  Macchina,
  Risultato
FROM 
    MicroMissioni 
INNER JOIN 
    Commesse 
    ON MicroMissioni.ID_Commessa = Commesse.ID_Commessa
WHERE
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND {{Risultato}}
    AND {{Tipo}}
GROUP BY 
    Tipo,
    Macchina,
    Risultato
ORDER BY
    Macchina,
    Risultato;

-- Amount of Leaving/ Taging with chains for each result and machine
-- Mostra il totale di missioni di presa e/o consegna con catena per risultato
SELECT
  Tipo,
  COUNT(*) AS Quantità,
  Macchina,
  CASE 
    WHEN Risultato = '(1) OK' THEN LEFT(Risultato, 4)
    ELSE LEFT(Risultato, 5)
  END AS Code_Risultato
FROM 
    MicroMissioni 
INNER JOIN 
    Commesse 
    ON MicroMissioni.ID_Commessa = Commesse.ID_Commessa
WHERE
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND {{Tipo_Missione}}
    AND {{Risultato}}
GROUP BY 
    Tipo,
    Macchina,
    Code_Risultato;

-- Legend Code & result mission
SELECT
  CASE 
    WHEN Risultato = '(1) OK' THEN LEFT(Risultato, 4)
    ELSE LEFT(Risultato, 5)
  END AS Code_Result,
  
  CASE 
    WHEN Risultato = '(1) OK' THEN SUBSTRING(Risultato, 5) 
    ELSE SUBSTRING(Risultato, 6)
  END AS Result
FROM 
    MicroMissioni 
INNER JOIN 
    Commesse 
    ON MicroMissioni.ID_Commessa = Commesse.ID_Commessa
WHERE
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND {{Tipo_Missione}}
    AND {{Risultato}}
    AND Risultato NOT LIKE ''
GROUP BY 
    Code_Result,
    Result
ORDER BY
    Code_Result ASC;

-- Daily amount of Taking with chains for each machine
-- Mostra la quantità giornaliera di missioni di presa e consegna con catena per macchina
SELECT
    Date(Data_Ora_inizio) AS Data,
    COUNT(*) AS Amount_Of_Taking,
    Macchina
FROM
    MicroMissioni
INNER JOIN 
    Commesse
    ON MicroMissioni.ID_Commessa = Commesse.ID_Commessa
WHERE   
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND MicroMissioni.Tipo = '(10) Taking with chain'
    AND {{Risultato}}
GROUP BY
    Data,
    Macchina
ORDER BY
    Data,
    Macchina;

-- Daily amount of Leaving with chains for each machine
-- Mostra la quantità giornaliera di missioni di consegna con catena per macchina
SELECT
    Tipo,
    Date(Data_Ora_inizio) AS Data,
    COUNT(*) AS Amount_Of_Taking,
    Macchina
FROM
    MicroMissioni
INNER JOIN 
    Commesse
    ON MicroMissioni.ID_Commessa = Commesse.ID_Commessa
WHERE   
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND MicroMissioni.Tipo = '(20) Leaving with chain'
    AND {{Risultato}}
GROUP BY
    Data,
    Tipo,
    Macchina
ORDER BY
    Data ASC,
    Tipo ASC;

-- Daily amount of Leaving/ Taking with chains for each machine
-- Mostra la quantità giornaliera di missioni di presa e/o consegna con catena per macchina
SELECT
    Tipo,
    Date(Data_Ora_inizio) AS Data,
    COUNT(*) AS Quantità,
    Macchina
FROM
    MicroMissioni
INNER JOIN 
    Commesse
    ON MicroMissioni.ID_Commessa = Commesse.ID_Commessa
WHERE   
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND {{Tipo_Missione}}
    AND {{Risultato}}
GROUP BY
    Data,
    Tipo,
    Macchina
ORDER BY
    Data ASC,
    Tipo ASC;

-- Daily amount of Leaving/ Taking with chains for each machine
-- Mostra la quantità giornaliera di missioni di presa e/o consegna con catena per macchina
SELECT
    Tipo,
    DATE_FORMAT(Date(Data_Ora_inizio), '%e/%c/%y') as Data,
    Macchina,
    COUNT(*) AS Quantità
FROM
   MicroMissioni
INNER JOIN 
    Commesse 
    ON Commesse.ID_Commessa = MicroMissioni.ID_Commessa
WHERE   
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND {{Tipo_Missione}}
    AND {{Risultato}}
GROUP BY
  Tipo,
  Data,
  Macchina
ORDER BY
    Tipo ASC,
    Data ASC,
    Macchina ASC;

-- Daily amount of Leaving/ Taking with chains
-- Mostra la quantità giornaliera di missioni di presa e/o consegna con catena
SELECT
    Tipo,
    Date(Data_Ora_inizio) AS Data,
    COUNT(*) AS Quantità
FROM
    MicroMissioni
INNER JOIN 
    Commesse
    ON MicroMissioni.ID_Commessa = Commesse.ID_Commessa
WHERE   
    Commesse.Nome = {{Commessa}}
    AND {{Intervallo_Temporale}}
    AND {{Macchina}}
    AND {{Tipo_Missione}}
    AND {{Risultato}}
GROUP BY
    Data,
    Tipo
ORDER BY
    Data ASC,
    Tipo ASC;

-- --------------------------------------------------------------------------------------------
-- Scheda 4: Km 
-- --------------------------------------------------------------------------------------------

-- Total Km traveled for each machine
-- Mostra il totale di km percorsi per ogni macchina
SELECT 
    Macchina,
    Mm_Percorsi / 1000000 AS Km_Percorsi,
    Numero_Missioni,
    (Mm_Percorsi / 1000)/ Numero_Missioni as Media_Metri_Per_Missione
FROM(
    SELECT
        Macchina,
        SUM(Distanza) AS Mm_Percorsi,
        COUNT(*) AS Numero_Missioni,
        Commesse.Nome
    FROM
        MicroMissioni
    INNER JOIN 
        Commesse
        ON Commesse.ID_Commessa = MicroMissioni.ID_Commessa
    WHERE   
        Commesse.Nome = {{Commessa}}
        AND {{Macchina}}
        AND {{Intervallo_Temporale}}
        AND Risultato like '%OK'
        AND Tipo like '%30%'
    GROUP BY
        Macchina
) AS subquery
    
ORDER BY
    Macchina ASC;

-- --------------------------------------------------------------------------------------------
-- Scheda 5: Results
-- --------------------------------------------------------------------------------------------

