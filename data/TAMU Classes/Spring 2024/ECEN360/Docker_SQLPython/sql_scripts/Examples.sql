--list of all customers who have bought a car
--return all customer IDs
--first names
--last names
--valid phone numbers
--of customers who purchased a car

--join? How? customer id
--we need a products table too
--join three tables together

SELECT c.customer_id, c.first_name, c.last_name, c.phone, p.product_type
FROM customers as c
	INNER JOIN sales as s
	ON c.customer_id = s.customer_id
		INNER JOIN products as p
		ON s.product_id = p.product_id
WHERE p.product_type = 'automobile' AND c.phone IS NOT NULL;

