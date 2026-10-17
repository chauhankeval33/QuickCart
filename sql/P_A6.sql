-- Q6 Delivery time by hour of day.
-- Exclusion rule: status <> 'cancelled' (cancelled rows have NULL delivery_minutes), delivery_minutes NOT NULL,
-- and 0 < delivery_minutes <= 120. The 10 values > 120 (392-811 min) are impossible for quick-commerce and sit
-- far outside the rest of the data (max otherwise 71.7). Exact duplicates removed. Refunded orders are kept.
-- Median is computed exactly with window functions (mean of the middle one/two values).
WITH valid AS (
  SELECT DISTINCT order_id, order_ts, delivery_minutes
  FROM orders
  WHERE status <> 'cancelled' AND delivery_minutes IS NOT NULL
    AND delivery_minutes > 0 AND delivery_minutes <= 120
),
ranked AS (
  SELECT CAST(STRFTIME('%H', order_ts) AS INT) AS hr, delivery_minutes,
         ROW_NUMBER() OVER (PARTITION BY STRFTIME('%H', order_ts) ORDER BY delivery_minutes) AS rn,
         COUNT(*)     OVER (PARTITION BY STRFTIME('%H', order_ts)) AS cnt
  FROM valid
)
SELECT hr AS hour_of_day, COUNT(*) AS orders,
       ROUND(AVG(delivery_minutes), 2) AS avg_minutes,
       ROUND(AVG(CASE WHEN rn IN ((cnt + 1) / 2, (cnt + 2) / 2) THEN delivery_minutes END), 2) AS median_minutes
FROM ranked
GROUP BY hr
ORDER BY hr;



