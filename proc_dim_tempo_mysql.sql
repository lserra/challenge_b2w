-- CRIACAO DA ESTRUTURA DA DIMENSAO TIME

CREATE TABLE b2w.dim_time (
  SK_TIME int NOT NULL AUTO_INCREMENT,
  'DATE' date NOT NULL,
  DAY int(11) NOT NULL,
  MONTH int(11) NOT NULL,
  YEAR int(11) NOT NULL,
  WEEK int(11) NOT NULL,
  WEEKDAY int(11) NOT NULL,
  EVENT varchar(20) NOT NULL,
  PRIMARY KEY (SK_TIME),
  INDEX idx_dim_time ('DATE')
) ENGINE=MyISAM DEFAULT CHARSET=utf8;

-- CRIACAO DA PROCEDURE DE CARGA

USE b2w;

DROP PROCEDURE IF EXISTS load_dim_time;

DELIMITER $$

CREATE PROCEDURE load_dim_time()
BEGIN
  DECLARE di DATE;
  DECLARE df DATE;

  DELETE FROM b2w.dim_time;
   
  SELECT '2015-01-01' INTO di;
  SELECT '2015-12-31' INTO df;
    
  WHILE (di <= df) DO
   
    INSERT INTO b2w.dim_time (
          DATE,
          DAY,
          MONTH,
          YEAR,
          WEEK,
          WEEKDAY,
          EVENT)
    SELECT 
            (di) as 'DATE',
            RIGHT(CONCAT('0',DAY(di)),2) as 'DAY',
            MONTH(di) as 'MONTH',
            YEAR(di) as 'YEAR',            
            WEEK(di) as 'WEEK',
            WEEKDAY(di) as 'WEEKDAY',
            'NO EVENT' as EVENT;
   
    SET di = DATE_ADD(di, INTERVAL 1 DAY);
   
  END WHILE;

END$$

DELIMITER ;