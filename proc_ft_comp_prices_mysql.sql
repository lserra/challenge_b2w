-- POPULA A TABELA dw_ft_comp_prices
-- CRIACAO DA PROCEDURE DE CARGA 

DROP PROCEDURE IF EXISTS load_dw_ft_comp_prices;

DELIMITER $$

CREATE PROCEDURE load_dw_ft_comp_prices()
BEGIN

  DROP TABLE IF EXISTS outliers;

  CREATE TEMPORARY TABLE outliers
  SELECT 
    COMPETITOR, 
    COMPETITOR_PRICE, 
    ROUND(COMPETITOR_PRICE) AS CP,
    CASE 
        WHEN LENGTH(ROUND(COMPETITOR_PRICE)) = 6 THEN 'APAGAR'
        ELSE 'NAO APAGAR'
    END AS STATUS
  FROM ods_comp_prices;

  -- SELECT DISTINCT * FROM outliers WHERE STATUS = 'APAGAR' ORDER BY 1;

  UPDATE ods_comp_prices t1 INNER JOIN (
    SELECT DISTINCT CP FROM outliers WHERE STATUS = 'APAGAR'
    ) t2
    ON t1.COMPETITOR_PRICE = t2.CP
  SET
    t1.COMPETITOR_PRICE = t2.CP/100;

END$$

DELIMITER ;

CALL load_dw_ft_comp_prices;