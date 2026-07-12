-- intermediate_queries.sql
-- Run with sqlite3 or any SQL tool.

-- 4. Customers with no delivered order
SELECT DISTINCT c.customer_id, c.customer_name
FROM customers c
JOIN orders o ON c.customer_id = o.customer_id
WHERE c.customer_id NOT IN (
    SELECT customer_id
    FROM orders
    WHERE status = 'DELIVERED' AND customer_id IS NOT NULL
);


-- 5. Products with more returns
SELECT
    p.product_id,
    p.product_name,
    SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END) AS total_purchased,
    SUM(CASE WHEN oi.quantity < 0 THEN -oi.quantity ELSE 0 END) AS total_returned
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.product_id, p.product_name
HAVING total_returned > total_purchased;


-- 6. Return rate by category
SELECT
    p.category,
    SUM(CASE WHEN oi.quantity < 0 THEN -oi.quantity ELSE 0 END) AS returned_items,
    SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END) AS purchased_items,
    ROUND(
        SUM(CASE WHEN oi.quantity < 0 THEN -oi.quantity ELSE 0 END) * 100.0 /
        NULLIF(SUM(CASE WHEN oi.quantity > 0 THEN oi.quantity ELSE 0 END), 0), 2
    ) AS return_rate_percent
FROM order_items oi
JOIN products p ON oi.product_id = p.product_id
GROUP BY p.category;
