-- advanced_queries.sql
-- Run with sqlite3 or any SQL tool.

-- 7. Running totals
WITH daily_revenue AS (
    SELECT
        o.region_code,
        DATE(o.order_date) AS order_day,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS daily_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY o.region_code, order_day
)
SELECT
    region_code,
    order_day AS order_date,
    ROUND(daily_revenue, 2) AS daily_revenue,
    ROUND(SUM(daily_revenue) OVER (
        PARTITION BY region_code ORDER BY order_day
        ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS running_total
FROM daily_revenue
ORDER BY region_code, order_date;


-- 8. Rank products
WITH product_revenue AS (
    SELECT
        p.category,
        p.product_name,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS total_revenue
    FROM order_items oi
    JOIN products p ON oi.product_id = p.product_id
    GROUP BY p.category, p.product_name
)
SELECT
    category,
    product_name,
    ROUND(total_revenue, 2) AS total_revenue,
    DENSE_RANK() OVER (PARTITION BY category ORDER BY total_revenue DESC) AS rank_in_category
FROM product_revenue
ORDER BY category, rank_in_category;


-- 9. Order gaps
WITH customer_orders AS (
    SELECT customer_id, order_date
    FROM orders
    WHERE customer_id != 'UNKNOWN'
),
gaps AS (
    SELECT
        customer_id,
        order_date,
        LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) AS previous_order_date
    FROM customer_orders
),
gaps_with_days AS (
    SELECT
        customer_id,
        order_date,
        previous_order_date,
        CASE WHEN previous_order_date IS NOT NULL
            THEN CAST(julianday(order_date) - julianday(previous_order_date) AS INTEGER)
            ELSE NULL
        END AS days_gap
    FROM gaps
),
customer_avg_gap AS (
    SELECT customer_id, AVG(days_gap) AS avg_gap
    FROM gaps_with_days
    WHERE days_gap IS NOT NULL
    GROUP BY customer_id
)
SELECT
    g.customer_id,
    g.order_date,
    g.previous_order_date,
    g.days_gap,
    CASE WHEN a.avg_gap > 30 THEN 'At Risk' ELSE 'Active' END AS risk_flag
FROM gaps_with_days g
JOIN customer_avg_gap a ON g.customer_id = a.customer_id
ORDER BY g.customer_id, g.order_date;


-- 10. Monthly customer buckets
WITH monthly_customer_revenue AS (
    SELECT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS monthly_revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id, order_month
),
categorized AS (
    SELECT
        customer_id,
        order_month,
        monthly_revenue,
        CASE
            WHEN monthly_revenue > 10000 THEN 'High'
            WHEN monthly_revenue >= 5000 THEN 'Medium'
            ELSE 'Low'
        END AS revenue_category
    FROM monthly_customer_revenue
)
SELECT
    order_month,
    revenue_category,
    COUNT(DISTINCT customer_id) AS customer_count
FROM categorized
GROUP BY order_month, revenue_category
ORDER BY order_month, revenue_category;


-- 11. Customer quartiles
WITH customer_value AS (
    SELECT
        o.customer_id,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS total_value
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id
),
ranked AS (
    SELECT
        customer_id,
        total_value,
        NTILE(4) OVER (ORDER BY total_value DESC) AS quartile
    FROM customer_value
)
SELECT
    customer_id,
    ROUND(total_value, 2) AS total_value,
    quartile,
    CASE quartile
        WHEN 1 THEN 'Platinum'
        WHEN 2 THEN 'Gold'
        WHEN 3 THEN 'Silver'
        ELSE 'Bronze'
    END AS quartile_label
FROM ranked
ORDER BY total_value DESC;


-- 12. Year-over-year revenue
WITH monthly_revenue AS (
    SELECT
        CAST(strftime('%Y', o.order_date) AS INTEGER) AS year,
        CAST(strftime('%m', o.order_date) AS INTEGER) AS month,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    GROUP BY year, month
)
SELECT
    curr.year,
    curr.month,
    ROUND(curr.revenue, 2) AS revenue,
    ROUND(prev.revenue, 2) AS prev_year_revenue,
    CASE
        WHEN prev.revenue IS NOT NULL AND prev.revenue != 0
        THEN ROUND((curr.revenue - prev.revenue) * 100.0 / prev.revenue, 2)
        ELSE NULL
    END AS yoy_growth_percent
FROM monthly_revenue curr
LEFT JOIN monthly_revenue prev
    ON curr.month = prev.month AND curr.year = prev.year + 1
ORDER BY curr.year, curr.month;


-- 13. First vs last category
WITH customer_category_orders AS (
    SELECT
        o.customer_id,
        o.order_date,
        p.category,
        FIRST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id ORDER BY o.order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS first_category,
        LAST_VALUE(p.category) OVER (
            PARTITION BY o.customer_id ORDER BY o.order_date
            ROWS BETWEEN UNBOUNDED PRECEDING AND UNBOUNDED FOLLOWING
        ) AS last_category
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    JOIN products p ON oi.product_id = p.product_id
    WHERE o.customer_id != 'UNKNOWN'
)
SELECT DISTINCT
    customer_id,
    first_category,
    last_category,
    CASE WHEN first_category != last_category THEN 'Yes' ELSE 'No' END AS category_shift
FROM customer_category_orders
ORDER BY customer_id;


-- 14. Revenue share by customers
WITH customer_revenue AS (
    SELECT
        o.customer_id,
        SUM(oi.quantity * oi.unit_price * (1 - oi.discount_percent / 100.0)) AS revenue
    FROM orders o
    JOIN order_items oi ON o.order_id = oi.order_id
    WHERE o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id
),
total AS (
    SELECT SUM(revenue) AS grand_total FROM customer_revenue
)
SELECT
    cr.customer_id,
    ROUND(cr.revenue, 2) AS revenue,
    ROUND(SUM(cr.revenue) OVER (
        ORDER BY cr.revenue DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ), 2) AS cumulative_revenue,
    ROUND(SUM(cr.revenue) OVER (
        ORDER BY cr.revenue DESC ROWS BETWEEN UNBOUNDED PRECEDING AND CURRENT ROW
    ) * 100.0 / t.grand_total, 2) AS cumulative_percent
FROM customer_revenue cr, total t
ORDER BY cr.revenue DESC;


-- 15. Cohort retention
WITH customer_cohort AS (
    SELECT
        customer_id,
        strftime('%Y-%m', registration_date) AS cohort_month
    FROM customers
),
customer_order_months AS (
    SELECT
        o.customer_id,
        strftime('%Y-%m', o.order_date) AS order_month
    FROM orders o
    WHERE o.customer_id != 'UNKNOWN'
    GROUP BY o.customer_id, order_month
),
cohort_activity AS (
    SELECT
        cc.cohort_month,
        cc.customer_id,
        com.order_month,
        (CAST(strftime('%Y', com.order_month || '-01') AS INTEGER) * 12 +
         CAST(strftime('%m', com.order_month || '-01') AS INTEGER)) -
        (CAST(strftime('%Y', cc.cohort_month || '-01') AS INTEGER) * 12 +
         CAST(strftime('%m', cc.cohort_month || '-01') AS INTEGER)) AS month_number
    FROM customer_cohort cc
    JOIN customer_order_months com ON cc.customer_id = com.customer_id
),
cohort_size AS (
    SELECT cohort_month, COUNT(DISTINCT customer_id) AS total_customers
    FROM customer_cohort
    GROUP BY cohort_month
)
SELECT
    ca.cohort_month,
    ca.month_number,
    COUNT(DISTINCT ca.customer_id) AS active_customers,
    cs.total_customers,
    ROUND(COUNT(DISTINCT ca.customer_id) * 100.0 / cs.total_customers, 2) AS retention_rate
FROM cohort_activity ca
JOIN cohort_size cs ON ca.cohort_month = cs.cohort_month
WHERE ca.month_number BETWEEN 0 AND 3
GROUP BY ca.cohort_month, ca.month_number
ORDER BY ca.cohort_month, ca.month_number;


-- 16. Frequently bought together
SELECT
    pa.product_name AS product_a,
    pb.product_name AS product_b,
    COUNT(*) AS times_bought_together
FROM order_items oi1
JOIN order_items oi2
    ON oi1.order_id = oi2.order_id
    AND oi1.product_id < oi2.product_id
JOIN products pa ON oi1.product_id = pa.product_id
JOIN products pb ON oi2.product_id = pb.product_id
GROUP BY pa.product_name, pb.product_name
ORDER BY times_bought_together DESC;
