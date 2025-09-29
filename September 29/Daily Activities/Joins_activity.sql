create database CompanyDB;
use CompanyDB;

CREATE TABLE Departments (
    dept_id INT AUTO_INCREMENT PRIMARY KEY,
    dept_name VARCHAR(50) NOT NULL
);
CREATE TABLE Employees (
    emp_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50),
    age INT,
    salary DECIMAL(10 , 2 ),
    dept_id INT,
    FOREIGN KEY (dept_id)
        REFERENCES Departments (dept_id)
);
insert into Departments (dept_name) values
	('IT'),
    ('HR'),
    ('Finance'),
    ('Sales');
INSERT INTO Employees (name, age, salary, dept_id) VALUES
('Rahul', 28, 55000, 1),   -- IT
('Priya', 32, 60000, 2),   -- HR
('Arjun', 25, 48000, 3),   -- Finance
('Neha', 30, 70000, 1),    -- IT
('Vikram', 35, 65000, 4);  -- Sales

-- drop foreign key to truncate --
ALTER TABLE Employees DROP FOREIGN KEY employees_ibfk_1;

TRUNCATE TABLE Employees;

TRUNCATE TABLE Departments;

INSERT INTO Departments (dept_name) VALUES
('IT'),         -- id = 1
('HR'),         -- id = 2
('Finance'),    -- id = 3
('Sales'),      -- id = 4
('Marketing');  -- id = 5  

INSERT INTO Employees (name, age, salary, dept_id) VALUES
('Rahul', 28, 55000, 1),   -- IT
('Priya', 32, 60000, 2),   -- HR
('Arjun', 25, 48000, NULL),-- 
('Neha', 30, 70000, 1),    -- IT
('Vikram', 35, 65000, 4);  -- Sales

select e.name, e.salary, d.dept_name
from Employees e
inner join Departments d
on e.dept_id= d.dept_id;

select e.name, e.salary, d.dept_name
from Employees e
left join Departments d
on e.dept_id= d.dept_id;

select e.name, e.salary, d.dept_name
from Employees e
right join Departments d
on e.dept_id= d.dept_id;

-- full join
select e.name, e.salary, d.dept_name
from Employees e
left join Departments d
on e.dept_id= d.dept_id
UNION
select e.name, e.salary, d.dept_name
from Employees e
right join Departments d
on e.dept_id= d.dept_id;





 
