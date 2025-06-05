--SELECT query basic anatomy

--This is a skeleton (SELECT, FROM, WHERE)
SELECT --columns we want from the table(s)
FROM --table(s) were pulling data from
WHERE --specifies the rows we want from the table(s)
GROUP BY --aggregating the data to a higher level
ORDER BY --post-processing re-organizing the table
LIMIT --only produce the top X rows

--Simple example: list of customers from Arizona
--start with the skeleton
--* selects ALL of them
SELECT *
FROM customers
WHERE state = 'AZ';
SELECT * FROM customers LIMIT 10;

--ORDER BY
SELECT *
FROM products
ORDER BY production_start_date ASC, product_id DESC --(Ordered by least to greatest)
LIMIT 5; --To reduce RAM
--DESC for descending order (Greatest to smallest)

--What is going on here?
SELECT *
FROM products
WHERE production_end_date IS NOT NULL;

--Excersize 6
--usernames of first 10 female salespeople hired
--ordered from first hired to last hired
SELECT username
FROM salespeople
WHERE (gender = 'Female' AND termination_date IS NULL)
ORDER BY hire_date ASC
LIMIT 10;

--SQL script example
SELECT * FROM emails LIMIT 2;

SELECT * FROM customers LIMIT 2;

SELECT * FROM dealerships LIMIT 2;

SELECT version()