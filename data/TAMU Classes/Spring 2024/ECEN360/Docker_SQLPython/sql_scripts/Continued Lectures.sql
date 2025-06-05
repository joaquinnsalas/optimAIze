--Agenda
--finish DISTINCT and DISTINCT ON
SELECT DISTINCT year, product_type
FROM products
ORDER BY year, product_type;

--DISTINCT returns rows that contain a unique combination of values
--accross all fields coming after the DISTINCT keyword.

--What if we want to return rows that are distinct on some fields, but not all
--DISTINCT ON helps us here

--example of DISTINCT ON
--return a list of salespeople with distinct first names
--in the case that two or more salespeople share the same first name, return the one that
--started first
SELECT DISTINCT ON (first_name) *
FROM salespeople
ORDER BY first_name, hire_date ASC;


--Activity 5 (practice with joins)

SELECT *
FROM customers as c
	INNER JOIN sales as s
		ON c.customer_id = s.customer_id
	INNER JOIN products as p
		ON s.product_id = p.product_id
	LEFT JOIN dealerships as d
		ON d.dealership_id = s.dealership_id
WHERE
ORDER BY

--Intro to aggregate functions (more next week)
SELECT COUNT (customer_id)
FROM customers;

--COUNT() counts the number of non-null rows in the specified field(s)

SELECT COUNT (*)
FROM customers;

select year, product_type, avg(base_msrp)
from products
where production_start_date >= '2018-01-01'
group by year, product_type;


--quiz (need to know)
--filtering (WHERE clause, AND/OR keywords, IN/NOT IN keywords)
--joins (INNER JOIN, LEFT/RIGHT/OUTER JOINS, CROSS JOIN)
--aggregation (GROUP BY keyword, HAVING keyword)

