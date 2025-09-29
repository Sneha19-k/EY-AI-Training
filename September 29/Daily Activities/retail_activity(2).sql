Delimiter $$
create procedure getAllProducts()
begin
	select product_id, product_name, category, price
    from products;
end$$

Delimiter ;
call getAllProducts();

Delimiter $$
create procedure getOrdersWithCustomer()
begin
	select o.order_id, o.order_date, c.name as customer_name
    from orders o
    join customers c
    on o.customer_id = c.customer_id;
end$$

Delimiter ;
call getOrdersWithCustomer();

DROP PROCEDURE IF EXISTS getOrdersWithCust;

DELIMITER $$
CREATE PROCEDURE GetFullOrderDetails()
BEGIN
    SELECT 
        o.order_id,
        c.name AS customer_name,
        p.product_name,
        od.quantity,
        p.price,
        (od.quantity * p.price) AS total
    FROM Orders o
    JOIN Customers c ON o.customer_id = c.customer_id
    JOIN OrderDetails od ON o.order_id = od.order_id
    JOIN Products p ON od.product_id = p.product_id;
END$$
DELIMITER ;
 
CALL GetFullOrderDetails();


-- dynamic procedures

DELIMITER $$
CREATE PROCEDURE GetCustomerOrders(in cust_id int)
	begin
    select o.order_id,
		   o.order_date,
           p.product_name,
           od.quantity,
           p.price,
           (od.quantity * p.price) as total
	from orders o
    join orderdetails od on o.order_id = od.order_id
    join products p on od.order_id= p.product_id
    where o.customer_id= cust_id;
end$$
DELIMITER ;
call GetCustomerOrders(2);
call GetCustomerOrders(3);

-- DROP PROCEDURE IF EXISTS  GetCustomerOrderss;
DELIMITER $$
 
CREATE PROCEDURE GetMonthlySales(IN month_no INT, IN year_no INT)
BEGIN
    SELECT MONTH(o.order_date) AS month, YEAR(o.order_date) AS year,
           SUM(od.quantity * p.price) AS total_sales
    FROM Orders o
    JOIN OrderDetails od ON o.order_id = od.order_id
    JOIN Products p ON od.product_id = p.product_id
    WHERE MONTH(o.order_date) = month_no AND YEAR(o.order_date) = year_no
    GROUP BY month, year;
END$$
 
DELIMITER ;
CALL GetMonthlySales(9, 2025);

DELIMITER $$
CREATE PROCEDURE GetTopProducts()
BEGIN
    SELECT p.product_name, SUM(od.quantity) AS total_sold,
           SUM(od.quantity * p.price) AS revenue
    FROM OrderDetails od
    JOIN Products p ON od.product_id = p.product_id
    GROUP BY p.product_id, p.product_name
    ORDER BY revenue DESC
    LIMIT 3;
END$$
DELIMITER ;
CALL GetTopProducts();




 




