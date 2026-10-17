-- Q5 Cohort retention (delivered, basket_value > 0, deduplicated).
-- Month +k = a delivered order in the calendar month exactly k months after the cohort month.
-- Data ends 2026-06, so unobservable windows return NULL instead of a misleading 0%.

WITH clean_orders AS (
    SELECT DISTINCT
        order_id,
        customer_id,
        CAST(STRFTIME('%Y', order_ts) AS INT) * 12
        + CAST(STRFTIME('%m', order_ts) AS INT) AS month_no
    FROM orders
    WHERE status = 'delivered'
      AND basket_value > 0
),
cohorts AS (
    SELECT customer_id, MIN(month_no) AS cohort_month
    FROM clean_orders
    GROUP BY customer_id
),
retention AS (
    SELECT
        c.customer_id,
        c.cohort_month,
        MAX(o.month_no = c.cohort_month + 1) AS r1,
        MAX(o.month_no = c.cohort_month + 3) AS r3
    FROM cohorts c
    JOIN clean_orders o
        ON c.customer_id = o.customer_id
    GROUP BY c.customer_id, c.cohort_month
)
SELECT
    STRFTIME(
        '%Y-%m',
        DATE('2000-01-01', '+' || (cohort_month - 24000) || ' months')
    ) AS cohort_month,
    COUNT(*) AS cohort_size,
    CASE
        WHEN cohort_month + 1 <= (
            SELECT MAX(month_no) FROM clean_orders
        )
        THEN ROUND(100.0 * SUM(r1) / COUNT(*), 1)
    END AS pct_month_plus_1,
    CASE
        WHEN cohort_month + 3 <= (
            SELECT MAX(month_no) FROM clean_orders
        )
        THEN ROUND(100.0 * SUM(r3) / COUNT(*), 1)
    END AS pct_month_plus_3
FROM retention
GROUP BY cohort_month
ORDER BY cohort_month;

