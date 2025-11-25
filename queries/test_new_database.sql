CREATE DATABASE eurofork_test;

USE eurofork_test;

CREATE TABLE job_orders( 
id_job_order INT AUTO_INCREMENT,
     name VARCHAR(100),
    nation VARCHAR(100),
    CONSTRAINT pk_job_orders PRIMARY KEY(id_job_order) 
);


CREATE TABLE machines( 
id_machine INT AUTO_INCREMENT,
    id_job_order INT,
    name VARCHAR(100),
    type VARCHAR(100),
    CONSTRAINT pk_machines PRIMARY KEY(id_machine),
    CONSTRAINT fk_job_orders FOREIGN KEY(id_job_order) REFERENCES job_orders(id_job_order) ON DELETE CASCADE ON UPDATE CASCADE 
); 
    
CREATE TABLE micromissions( id_micromission INT AUTO_INCREMENT,
    id_machine INT,
    type VARCHAR(100),
    result VARCHAR(100),
    date_time DATETIME,
    CONSTRAINT pk_micromissions PRIMARY KEY(id_micromission),
    CONSTRAINT fk_machines FOREIGN KEY(id_machine) 
        REFERENCES machines(id_machine) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE 
); 

CREATE TABLE alarms( 
    id_alarm INT AUTO_INCREMENT,
    type VARCHAR(100),
    description VARCHAR(400),
    CONSTRAINT pk_alarms PRIMARY KEY(id_alarm) 
); 

CREATE TABLE micromission_alarms (
    id_micromission_alarm INT AUTO_INCREMENT,
    id_micromission INT,
    id_alarm INT,
    trigger_datetime DATETIME,
    value VARCHAR(10),
    CONSTRAINT pk_micromission_alarms PRIMARY KEY(id_micromission_alarm),
    CONSTRAINT fk_micromission FOREIGN KEY (id_micromission) 
        REFERENCES micromissions(id_micromission) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE,
    CONSTRAINT fk_alarm FOREIGN KEY (id_alarm) 
        REFERENCES alarms(id_alarm) 
        ON DELETE CASCADE 
        ON UPDATE CASCADE 
);

INSERT INTO job_orders (name, nation) VALUES
('SaniFrutta', 'Italy'),
('Jaguar Land Rover', 'United Kingdom'),
('Orangina', 'France');

INSERT INTO machines (id_job_order, name, type) VALUES
(1, 'Shuttle 1', 'Frozen'),
(1, 'Satellite 1', 'Frozen'),
(1, 'Shuttle 2', 'Normal'),
(1, 'Satellite 2', 'Normal'),
(2, 'Shuttle 1', 'Normal'),
(2, 'Satellite 1', 'Normal'),
(3, '7N0101', 'Frozen'),
(3, '7S0101', 'Frozen');

INSERT INTO micromissions (id_machine, type, result, date_time) VALUES
(7, '(10) Taking with chain', '(1) OK', '2025-10-01 08:00:00'),
(7, '(60) Positioning with chains', '(1) OK', '2025-10-01 09:00:00'),
(7, '(30) Move', '(200) Alarm Hardware', '2025-10-02 10:00:00'),
(7, '(30) Move', ' (1) OK', '2025-10-02 10:00:00'),
(8, '(10) Taking', '(1) OK', '2025-10-03 11:00:00'),
(8, '(50) Move out', '(1) OK', '2025-10-04 12:00:00'),
(8, '(30) Move', '(1) OK', '2025-10-04 12:00:00'),
(8, '(20) Leaving', '(1) OK', '2025-10-04 12:00:00'),
(8, '(30) Move', '(1) OK', '2025-10-04 12:00:00'),
(8, '(40) Move in', '(1) OK', '2025-10-04 12:00:00');

INSERT INTO alarms (type, description)
SELECT DISTINCT
   Tipo,
   Descrizione
FROM 
   Eurofork.Allarmi;

INSERT INTO micromission_alarms (id_micromission, id_alarm, trigger_datetime, value) VALUES
-- (3, 7, '2025-10-02 10:00:30', 'ON'),
(3, 7, '2025-10-02 11:00:35', 'OFF');


SELECT * FROM alarms;
SELECT * FROM micromissioni LIMIT 10;

SELECT 
	jo.name AS Order_Job_Name,
	jo.nation AS Order_Job_Nation,
	ma.name AS Machine_Name,
	ma.type AS Machine_Type,
	mi.date_time AS Micromission_Date_Time,
	mi.type AS Micromission_Type,
	mi.result AS Micromission_Result,
	al.type AS Alarm_Type,
	al.description AS Alarm_Description,
	ms.trigger_datetime AS Alarm_Date_Time,
	ms.value AS Alarm_Status
FROM
	machines ma
INNER JOIN
	job_orders jo
	ON ma.id_job_order = jo.id_job_order
INNER JOIN
	micromissions mi
	ON ma.id_machine = mi.id_machine
INNER JOIN
	micromission_alarms ms
	ON mi.id_micromission = ms.id_micromission
INNER JOIN
	alarms al
	ON ms.id_alarm = al.id_alarm
WHERE
	jo.name LIKE 'Orangina';
	
	
	
	
	
	

-- 47367 casi in cui l'orario di trasmissione è uguale a quello di inizio
-- solitamente tutti ok
SELECT *
FROM MicroMissioni
WHERE Data_Ora_TX != Data_Ora_Inizio AND Data_Ora_RX != Data_Ora_Inizio;

SELECT COUNT(*) AS coincidenti
FROM MicroMissioni
WHERE Data_Ora_TX = Data_Ora_Inizio AND Data_Ora_RX != Data_Ora_Inizio;

-- 1039 casi in cui l'orario ricevuto è uguale a quello di inizio
-- principalmente NULL quindi missioni non compiute per errori precedenti
SELECT *
FROM MicroMissioni
WHERE Data_Ora_RX = Data_Ora_Inizio AND Data_Ora_TX != Data_Ora_Inizio AND Data_Ora_TX < Data_Ora_Inizio;

SELECT COUNT(*) AS coincidenti
FROM MicroMissioni
WHERE Data_Ora_RX = Data_Ora_Inizio AND Data_Ora_TX != Data_Ora_Inizio AND Data_Ora_TX < Data_Ora_Inizio;


-- 23 casi in cui l'ora è uguale per tutti e 3 i campi date_time
-- solitamente perchè il risultato non è ok
SELECT *
FROM MicroMissioni
WHERE Data_Ora_RX = Data_Ora_Inizio AND Data_Ora_TX = Data_Ora_Inizio;

SELECT COUNT(*) AS coincidenza_date
FROM MicroMissioni
WHERE Data_Ora_RX = Data_Ora_Inizio AND Data_Ora_TX = Data_Ora_Inizio;

# 0 casi in cui la trasmessa è null
SELECT COUNT(*) FROM MicroMissioni WHERE Data_Ora_TX IS NULL;

SELECT COUNT(*) FROM MicroMissioni WHERE Data_Ora_RX IS NULL;

SELECT COUNT(*) FROM MicroMissioni WHERE Data_Ora_Inizio IS NULL;

SELECT COUNT(*)
FROM MicroMissioni
WHERE Data_Ora_RX IS NULL  OR Data_Ora_TX IS NULL OR Data_Ora_Inizio IS NULL;

SELECT *
FROM MicroMissioni
WHERE Data_Ora_TX > Data_Ora_Inizio;

SELECT COUNT(*)
FROM MicroMissioni
WHERE Data_Ora_RX <= Data_Ora_Inizio;






DELETE FROM Commesse WHERE ID_Commessa = 6;


SELECT * FROM Allarmi WHERE ID_Commessa = 6;


SELECT DISTINCT Risultato FROM  MicroMissioni;

CREATE TABLE LivelloMacchine( 
	id_livello_macchine INT AUTO_INCREMENT,
   ID_Commessa INT,
   Macchina VARCHAR(100),
   Numero_Macchina VARCHAR(100),
   Livello VARCHAR(100),
   CONSTRAINT pk_livello_macchine PRIMARY KEY(id_livello_macchine),
   CONSTRAINT fk_commesse FOREIGN KEY(ID_Commessa) REFERENCES Commesse(ID_Commessa) ON DELETE CASCADE ON UPDATE CASCADE 
); 


INSERT INTO LivelloMacchine (ID_Commessa, Macchina, Numero_Macchina, Livello)
SELECT DISTINCT
	ID_Commessa,
   Macchina,
   LEFT(RIGHT(Macchina, 3), 1),
   RIGHT(Macchina, 1)
FROM 
   Eurofork.MicroMissioni
WHERE
	ID_Commessa = 2
ORDER BY
	Macchina;
	
DELETE FROM LivelloMacchine WHERE ID_Commessa = 2 AND Livello IN (8,9);

DELETE FROM commesse WHERE ID_Commessa = 5;


SELECT COUNT(*) FROM MicroMissioni WHERE ID_Commessa = 1;


SELECT
    table_name,
    column_name,
    referenced_table_name,
    referenced_column_name,
    constraint_name
FROM
    information_schema.key_column_usage
WHERE
    referenced_table_name IS NOT NULL
    AND table_schema = 'eurofork';

