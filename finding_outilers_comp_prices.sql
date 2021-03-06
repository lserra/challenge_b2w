SELECT 
	COMPETITOR, 
	MIN(COMPETITOR_PRICE), 
	MAX(COMPETITOR_PRICE), 
	ROUND(((MAX(COMPETITOR_PRICE)/(MIN(COMPETITOR_PRICE)/100))-100),2) AS PERC,
	CASE 
		WHEN ROUND(((MAX(COMPETITOR_PRICE)/(MIN(COMPETITOR_PRICE)/100))-100),2) > 100 THEN 'APAGAR'
		ELSE 'NAO APAGAR'
	END AS STATUS
FROM ods_comp_prices
WHERE PROD_ID = 'P6'
GROUP BY COMPETITOR;

SELECT COMPETITOR, MIN(COMPETITOR_PRICE), MAX(COMPETITOR_PRICE)
FROM ods_comp_prices
WHERE PROD_ID = 'P6'
GROUP BY COMPETITOR;    

SELECT COMPETITOR, MIN(COMPETITOR_PRICE), MAX(COMPETITOR_PRICE)
FROM sa_comp_prices
WHERE PROD_ID = 'P6'
GROUP BY COMPETITOR; 

SELECT DISTINCT COMPETITOR, COMPETITOR_PRICE
FROM ods_comp_prices
WHERE PROD_ID = 'P6' AND COMPETITOR = 'C1'
ORDER BY 1, 2;  