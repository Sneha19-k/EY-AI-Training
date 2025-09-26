create database office;
CREATE TABLE employees (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL,
    age INT,
    department VARCHAR(50),
    salary DECIMAL(10 , 2 )
);

insert into employees(name,age,department,salary)
values('Rahul',21,'tech consulting',150000.00);

insert into employees(name,age,department,salary)
values('Priya', 23,'assurance',90000),
('Arjun', 23,'data science',78000);
SELECT 
    *
FROM
    employees;
UPDATE employees 
SET 
    salary = 92000
WHERE
    id = 2;

DELETE FROM employees 
WHERE
    id = 2;
SELECT 
    *
FROM
    employees;
 