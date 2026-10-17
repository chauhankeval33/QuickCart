-- Q2a Raw city values and counts (city lives on customers)
SELECT
    city,
    COUNT(*) AS customers
FROM customers
GROUP BY city
ORDER BY customers DESC;
-- Q2b Mapping to five clean city names
SELECT
  CASE LOWER(TRIM(city))
    WHEN 'bengaluru' THEN 'Bengaluru'
    WHEN 'bangalore' THEN 'Bengaluru'
    WHEN 'ahmedabad' THEN 'Ahmedabad'
    WHEN 'pune'      THEN 'Pune'
    WHEN 'surat'     THEN 'Surat'
    WHEN 'jaipur'    THEN 'Jaipur'
  END AS clean_city,
  COUNT(*) AS customers
FROM customers
GROUP BY clean_city
ORDER BY customers DESC;




