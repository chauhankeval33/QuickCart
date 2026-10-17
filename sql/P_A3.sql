-- Q3 Monthly GMV: delivered, basket_value > 0, exact duplicates removed (SELECT DISTINCT)
SELECT
    SUBSTR(order_ts, 1, 7) AS month,
    ROUND(SUM(basket_value), 2) AS gmv,
    ROUND(
        100.0 * (
            SUM(basket_value) -
            LAG(SUM(basket_value)) OVER (
                ORDER BY SUBSTR(order_ts, 1, 7)
            )
        ) / LAG(SUM(basket_value)) OVER (
            ORDER BY SUBSTR(order_ts, 1, 7)
        ),
        2
    ) AS mom_growth_pct
FROM (
    SELECT DISTINCT order_id, customer_id, order_ts, basket_value
    FROM orders
    WHERE status = 'delivered'
      AND basket_value > 0
) AS clean_orders
GROUP BY SUBSTR(order_ts, 1, 7)
ORDER BY month;


