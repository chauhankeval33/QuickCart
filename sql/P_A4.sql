SELECT *
FROM (
    SELECT
        CASE
            WHEN LOWER(TRIM(c.city)) IN ('bangalore', 'bengaluru')
                THEN 'Bengaluru'
            ELSE UPPER(SUBSTR(TRIM(c.city), 1, 1))
                 || LOWER(SUBSTR(TRIM(c.city), 2))
        END AS clean_city,

        o.customer_id,
        ROUND(SUM(o.basket_value), 2) AS total_spend,
        COUNT(DISTINCT o.order_id) AS total_orders,

        RANK() OVER (
            PARTITION BY
                CASE
                    WHEN LOWER(TRIM(c.city)) IN ('bangalore', 'bengaluru')
                        THEN 'Bengaluru'
                    ELSE UPPER(SUBSTR(TRIM(c.city), 1, 1))
                         || LOWER(SUBSTR(TRIM(c.city), 2))
                END
            ORDER BY SUM(o.basket_value) DESC
        ) AS rnk

    FROM customers c
    JOIN (
        SELECT DISTINCT order_id, customer_id, basket_value
        FROM orders
        WHERE status = 'delivered'
          AND basket_value > 0
    ) o ON c.customer_id = o.customer_id

    GROUP BY clean_city, o.customer_id
)
WHERE rnk <= 3
ORDER BY clean_city, rnk;

