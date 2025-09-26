insert into students(name,age,course,marks)
values('Rahul',21,'AI',85);

insert into students(name,age,course,marks)
values('Priya', 23,'ML',90),
('Arjun', 23,'data science',78)
 
select *from Students

select name, marks from students

select * from students where marks=90

update students
set marks=95, course='Advanced AI'
where id=4;
select *from Students
Delete from students where id=3;