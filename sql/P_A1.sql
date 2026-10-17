SELECT
    (SELECT COUNT(*)
     FROM orders) AS total_rows,

    (SELECT COUNT(DISTINCT order_id)
     FROM orders) AS distinct_order_ids,

    (SELECT COUNT(*)
     FROM (
         SELECT order_id
         FROM orders
         GROUP BY order_id, customer_id, order_ts, basket_value,
                  items_count, discount_amt, distance_km,
                  store_open_orders, is_raining, delivery_minutes,
                  payment_method, status
         HAVING COUNT(*) > 1
     ) AS duplicates) AS fully_duplicated_row_groups,

    (SELECT COALESCE(SUM(duplicate_count - 1), 0)
     FROM (
         SELECT COUNT(*) AS duplicate_count
         FROM orders
         GROUP BY order_id, customer_id, order_ts, basket_value,
                  items_count, discount_amt, distance_km,
                  store_open_orders, is_raining, delivery_minutes,
                  payment_method, status
         HAVING COUNT(*) > 1
     ) AS duplicates) AS surplus_duplicate_rows,

    (SELECT COUNT(*)
     FROM orders
     WHERE basket_value < 0) AS negative_basket_rows,

    (SELECT COUNT(DISTINCT order_id)
     FROM orders
     WHERE basket_value < 0) AS negative_basket_orders;