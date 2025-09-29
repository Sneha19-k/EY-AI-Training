Delimiter $$
create procedure getOrdersWithCustomers()
begin
	select o.order_id, o.order_date, c.name as customer_name
    from orders o
    join customers c
    on o.customer_id = c.customer_id;
end$$
