--Relational Databases
--Determining which salespeople work at a dealership in California

--STEP 1: what dealerships in California
SELECT *
FROM dealerships
WHERE state = 'CA';

--STEP 2: what salespeople have dealership id in California
SELECT *
FROM salespeople
WHERE dealership_id IN (2,5);

-- A better way
SELECT *
FROM salespeople as s--'left' table
	INNER JOIN dealerships as d --'right' table
	ON s.dealership_id = d.dealership_id --join predicate
WHERE d.state = 'CA'
ORDER BY s.salesperson_id ASC;

--Left outer join example to consider
SELECT *
FROM customers as c
LEFT OUTER JOIN emails as e
	ON e.customer_id = c.customer_id
ORDER BY c.customer_id
LIMIT 1000;

--INNER JOIN inclued salespeople
--that work at dealerships listed in dealerships table

--LEFT OUTER JOIN includes everything from the INNER JOIN plus...
--salespeople with a dealership id NOT found in the dealerships table
--including salespeople with a missing dealership id

--RIGHT OUTER JOIN includes everything from the INNER JOIN plus...
--dealerships without any salesperson assigned to it

--FULL OUTER JOIN includes everything from the INNER JOIN plus..
--salespeople with a dealership id NOT found in the dealerships table
--including salespeople with a missing dealership id
--dealerships without any salesperson assigned to it

--aggregating data, joining databases, filter, join, group by
--construct sql query from promt

--CROSS JOIN (Be careful)
SELECT p1.product_id as pid_1, p1.model as pname_1, 
p2.product_id as pid_2, p2.model as pname_2 --specifying columns that I want
FROM products as p1
	CROSS JOIN products as p2;
