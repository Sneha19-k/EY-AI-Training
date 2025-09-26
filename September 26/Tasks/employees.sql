create database office;
create table employees(
	id int auto_increment primary key,
    name VARCHAR(50) not null,
    age int,
    department varchar(50),
    salary decimal(10,2)
);

insert into employees(name,age,department,salary)
values('Rahul',21,'tech consulting',150000.00);

insert into employees(name,age,department,salary)
values('Priya', 23,'assurance',90000),
('Arjun', 23,'data science',78000);
select * from employees;
update employees
set salary=92000
where id=2;

delete from employees where id=2;
select * from employees;
 