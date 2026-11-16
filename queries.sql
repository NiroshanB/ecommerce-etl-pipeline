-- Revenue by category
SELECT category, COUNT(*) AS orders, ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY category
ORDER BY revenue DESC;

-- Monthly revenue
SELECT strftime('%Y-%m', order_date) AS month,
       COUNT(*) AS orders, ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY month
ORDER BY month;

-- Top 10 products by revenue
SELECT product_id, product_name, COUNT(*) AS orders,
       SUM(quantity) AS units_sold, ROUND(SUM(revenue), 2) AS revenue
FROM orders
GROUP BY product_id, product_name
ORDER BY revenue DESC
LIMIT 10;

-- Repeat-customer rate (share of customers with more than one order)
SELECT
    COUNT(*) AS total_customers,
    SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END) AS repeat_customers,
    ROUND(100.0 * SUM(CASE WHEN order_count > 1 THEN 1 ELSE 0 END)
          / COUNT(*), 1) AS repeat_rate_pct
FROM (
    SELECT customer_id, COUNT(*) AS order_count
    FROM orders
    GROUP BY customer_id
);
