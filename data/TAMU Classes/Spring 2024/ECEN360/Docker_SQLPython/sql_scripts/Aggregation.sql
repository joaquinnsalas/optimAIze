--COUNT + DISTINCT
--Question: How many unique states do we have a customer in?
SELECT COUNT(DISTINCT state)
FROM customers;

--How many customers we have in CA...
SELECT *
FROM customers
WHERE state = 'CA';

--* means all fields

SELECT * FROM products;

--Average

SELECT SUM(base_msrp)/COUNT(*) AS base_msrp_avg FROM products;

--Can you tell me how many customers do we have in EACH state?

--First thought: Do 50 different queries for the 50 states

SELECT COUNT(*) FROM customers WHERE state = 'CA'; 
SELECT COUNT(*) FROM customers WHERE state = 'TX'; --And so on

--GROUP BY keyword can help here

SELECT state, COUNT(*) as customer_count
FROM customers
WHERE state IS NOT NULL
GROUP BY state
ORDER BY state;

--Order by customer_count

SELECT state, COUNT(*) as customer_count
FROM customers
WHERE state IS NOT NULL
GROUP BY state
ORDER BY customer_count DESC;

--example of using aggregate functions, group by, and where clause together

SELECT state, COUNT(*)
FROM customers
WHERE gender = 'M'
GROUP BY state
ORDER BY COUNT(*) DESC;

--Exersize 14
--minimum, max, avg and st dev of the price for each PRODUCT TYPE that compant sells 

SELECT product_type, min(base_msrp) as min_price,
		max(base_msrp) as max_price,
		avg(base_msrp) as avg_price,
		stddev(base_msrp) as stdev_price
FROM products
GROUP BY product_type
ORDER BY product_type

