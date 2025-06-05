--HAVING clause

--Exersize 14
--minimum, max, avg and st dev of the price for each PRODUCT TYPE that compant sells 

SELECT product_type, min(base_msrp) as min_price,
		max(base_msrp) as max_price,
		avg(base_msrp) as avg_price,
		stddev(base_msrp) as stdev_price
FROM products
GROUP BY product_type
ORDER BY product_type

--return customer count by state, only for states that have 1000 or more customers
SELECT state, COUNT(*) as customer_count
FROM customers
--IF you want a JOIN do it here
WHERE email IS NOT NULL --filtering rows in the FROM table before agg. values
GROUP BY state
HAVING COUNT(*) >= 1000 --filtering rows after aggregate values are computed
ORDER BY customer_count ASC;
--WHERE clause is used to filter rows in the FROM table
--(Not a derived field)
