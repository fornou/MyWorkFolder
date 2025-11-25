CREATE TABLE `test` (
	`ID` INT NOT NULL AUTO_INCREMENT,
	`Result` VARCHAR(5) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	`N_Package` INT NULL DEFAULT NULL,
	PRIMARY KEY (`ID`) USING BTREE
);

INSERT INTO test (Result, N_Package)
SELECT 
    IF(RAND() < 0.02, 'KO', 'OK') AS Result,  -- 2% KO
    pkg.N_Package
FROM (
    SELECT @row := @row + 1 AS N_Package
    FROM (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) t1,
         (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4 UNION ALL SELECT 5 UNION ALL SELECT 6 UNION ALL SELECT 7 UNION ALL SELECT 8 UNION ALL SELECT 9) t2,
         (SELECT @row := 0) r
    LIMIT 100
) AS pkg
JOIN (
    SELECT 1 FROM (SELECT 0 UNION ALL SELECT 1 UNION ALL SELECT 2 UNION ALL SELECT 3 UNION ALL SELECT 4) t  -- da 2 a 5 missioni
) AS missions
WHERE RAND() < 0.8;  


CREATE TABLE test2 (
   ID INT NOT NULL AUTO_INCREMENT,
	Result VARCHAR(5) NULL DEFAULT NULL COLLATE 'utf8mb4_0900_ai_ci',
	IndexMission INT NULL DEFAULT NULL,
	CountMission INT NULL DEFAULT NULL,
	PRIMARY KEY (`ID`) USING BTREE
);

INSERT INTO test2 (Result, IndexMission, CountMission) VALUES
('OK', 1, 1),
('OK', 1, 1),
('OK', 1, 1),
('OK', 6, 6),
('OK', 5, 6),
('OK', 4, 6),
('OK', 3, 6),
('OK', 2, 6),
('OK', 1, 6),
('OK', 1, 1),
('OK', 1, 1),
('OK', 1, 1),
('OK', 1, 1),
('OK', 6, 6),
('OK', 5, 6),
('OK', 4, 6),
('OK', 3, 6),
('OK', 2, 6),
('OK', 1, 6),
('OK', 1, 1),
('OK', 1, 1),
('OK', 6, 6),
('OK', 5, 6),
('OK', 4, 6),
('OK', 3, 6),
('OK', 2, 6),
('OK', 1, 6),
('OK', 1, 1),
('OK', 6, 6),
('OK', 5, 6),
('OK', 4, 6),
('OK', 3, 6),
('OK', 2, 6),
('OK', 1, 6);


-- Calcolo KPI 
SELECT -- Query finale 6 che mi da il totale di pacchetti, pacchetti con risultato OK, pacchetti con risultato KO e il KPI 
	SUM(amount_package_status.Amount) AS Total_Package,
	SUM(CASE WHEN amount_package_status.StatusPackage = 'OK' THEN amount_package_status.Amount ELSE 0 END) AS Package_OK,
	SUM(CASE WHEN amount_package_status.StatusPackage = 'KO' THEN amount_package_status.Amount ELSE 0 END) Package_KO,
	ROUND(
	  (SUM(CASE WHEN amount_package_status.StatusPackage = 'OK' THEN amount_package_status.Amount ELSE 0 END) * 100.0) /
	  SUM(amount_package_status.Amount), 2
	) AS KPI
FROM(-- Query 5 che mi dice il totale di pacchetti per ogni risultato
	SELECT
		status_package.StatusPackage,
		COUNT(status_package.StatusPackage) AS Amount
	FROM(-- Query 4 che mi dice se il pacchetto è KO o OK  
		SELECT 
			count_result_package.PackageID,
			CASE 
		     WHEN SUM(CASE WHEN Result NOT LIKE '(1)%' AND Result NOT LIKE '(21)%' THEN 1 ELSE 0 END) > 0 THEN 'KO'
		     ELSE 'OK'
		   END AS StatusPackage
		FROM(-- Query 3 che da la quantità per ogni pacchetto missioni e per ogni risultato
			SELECT 
				mission_package.PackageID, 
				mission_package.Result,
				COUNT(*) AS Amount
			FROM(-- Query 2 che raggruppa le micromissioni tramite PackageID(Identificativo del pacchetto di micromissioni)
				SELECT
				    ID,
				    Result,
				    IndexMission,
				    CountMission,
				    @PackageID AS PackageID,
				    @PackageID := IF(IndexMission = 1, @PackageID + 1, @PackageID) AS NextPackageID
				FROM (-- Query 1 che ordina i risultati in ordine di ID_MicroMissione
					SELECT 
					  ID_Micromissione AS ID,
					  Risultato AS Result,
					  Indice_Micromissione AS IndexMission,
					  Numero_Micromissioni AS CountMission
					FROM 
						micromissioni
					WHERE 
						ID_Commessa = 1
					ORDER BY ID
					) AS ordered
				JOIN (SELECT @PackageID := 1) vars
				)AS mission_package	
			GROUP BY 
				mission_package.Result,
				mission_package.PackageID
			) AS count_result_package
		GROUP BY 	
			PackageID
		)AS status_package
	GROUP BY 	
		status_package.StatusPackage
	)AS amount_package_status;
