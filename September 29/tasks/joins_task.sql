CREATE database School;
use school;

create table teachers(
	teacher_id int auto_increment primary key,
    name varchar(50),
    subject_id int
);

create table subjects(
	subject_id int auto_increment primary key,
    subject_name varchar(50)
);

INSERT INTO Subjects (subject_name) VALUES
	('Mathematics'),   -- id = 1
	('Science'),       -- id = 2
	('English'),       -- id = 3
	('History'),       -- id = 4
	('Geography');     -- id = 5 (no teacher yet)

INSERT INTO Teachers (name, subject_id) VALUES
	('Rahul Sir', 1),   -- Mathematics
	('Priya Madam', 2), -- Science
	('Arjun Sir', NULL),-- No subject assigned
	('Neha Madam', 3);  -- English
    
select t.name, t.subject_id, s.subject_name
from Teachers t
inner join Subjects s
on t.subject_id= s.subject_id;

select t.name, t.subject_id, s.subject_name
from Teachers t
left join Subjects s
on t.subject_id= s.subject_id;

select t.name, t.subject_id, s.subject_name
from Teachers t
right join Subjects s
on t.subject_id= s.subject_id;

-- full join
select t.name, t.subject_id, s.subject_name
from Teachers t
left join Subjects s
on t.subject_id= s.subject_id 
union
select t.name, t.subject_id, s.subject_name
from Teachers t
right join Subjects s
on t.subject_id= s.subject_id;


 