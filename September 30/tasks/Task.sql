CREATE DATABASE UniversityDB;
USE UniversityDB;
-- Students Table
CREATE TABLE Students (
student_id INT PRIMARY KEY,
name VARCHAR(50),
city VARCHAR(50)
);
-- Courses Table
CREATE TABLE Courses (
course_id INT PRIMARY KEY,
course_name VARCHAR(50),
credits INT
);
-- Enrollments Table
CREATE TABLE Enrollments (
enroll_id INT PRIMARY KEY,
student_id INT,
course_id INT,
grade CHAR(2),
FOREIGN KEY (student_id) REFERENCES Students(student_id),
FOREIGN KEY (course_id) REFERENCES Courses(course_id)
);
-- Insert Students
INSERT INTO Students VALUES
(1, 'Rahul', 'Mumbai'),
(2, 'Priya', 'Delhi'),
(3, 'Arjun', 'Bengaluru'),
(4, 'Neha', 'Hyderabad'),
(5, 'Vikram', 'Chennai');
-- Insert Courses
INSERT INTO Courses VALUES
(101, 'Mathematics', 4),
(102, 'Computer Science', 3),
(103, 'Economics', 2),
(104, 'History', 3);
-- Insert Enrollments
INSERT INTO Enrollments VALUES
(1, 1, 101, 'A'),
(2, 1, 102, 'B'),
(3, 2, 103, 'A'),
(4, 3, 101, 'C'),
(5, 4, 102, 'B'),
(6, 5, 104, 'A');

-- 1
Delimiter $$
create procedure getAllStudents()
begin
	select Student_id, name, city
    from students;
end$$
Delimiter ;
call getAllStudents();

-- 2
Delimiter $$
create procedure listAllCourse()
begin
	select course_id, course_name, credits
    from courses;
end$$
Delimiter ;

call listAllCourse();

-- 3 Create a stored procedure to find all students from a given city (take city as input).
Delimiter $$
create procedure getStudentFromCity( in input_city varchar(50) )
begin
	select student_id, name, city
    from students
    where city=input_city;
end$$
Delimiter ;
call getStudentFromCity('Delhi');

-- 4  Create a stored procedure to list students with their enrolled courses.
Delimiter $$
create procedure getStudentfromCourse()
begin
	select   s.student_id, s.name, e.course_id
    from Students s
    join Enrollments e ON s.student_id = e.student_id;
end$$
Delimiter ;
call getStudentfromCourse();

DROP PROCEDURE IF EXISTS getStudentfromCourse;
-- 5
Delimiter $$
create procedure listStudentsfromCourses(in input_course_id int)
begin
	select s.student_id, s.name, e.course_id, e.grade
	from Students s
	join Enrollments e on s.student_id = e.student_id
	where e.course_id = input_course_id;
end$$
Delimiter ;
call listStudentsfromCourses(101);

-- 6 count number of students
Delimiter $$
create procedure countStudentsInCourses()
begin
	select c.course_id, c.course_name, count(e.student_id) as student_count
	from Courses c
	left join Enrollments e on c.course_id = e.course_id
	group by c.course_id, c.course_name;
end$$
Delimiter ;
call countStudentsInCourses();

-- 7 Create a stored procedure to list students with course names and grades.
Delimiter $$
create procedure listStudentCourseGrades()
begin
	select s.student_id, s.name, c.course_name, e.grade
	from Students s
	join Enrollments e on s.student_id = e.student_id
	join Courses c on e.course_id = c.course_id;
end$$
Delimiter ;

call listStudentCourseGrades();

-- 8 Create a stored procedure to show all courses taken by a given student (take student_id as input).

Delimiter $$
create procedure getCoursesByStudent(in input_student_id int)
begin
    select s.student_id, s.name, c.course_id, c.course_name, c.credits, e.grade
    from Students s
    join Enrollments e on s.student_id = e.student_id
    join Courses c on e.course_id = c.course_id
    where s.student_id = input_student_id;
end$$
Delimiter ;

call getCoursesByStudent(1);

-- 9 Create a stored procedure to show average grade per course.
DELIMITER $$
CREATE PROCEDURE GetAverageGrades()
BEGIN
SELECT c.course_name, CASE ROUND(AVG(CASE e.grade
            WHEN 'A' THEN 4
            WHEN 'B' THEN 3
            WHEN 'C' THEN 2
            WHEN 'D' THEN 1
            END))
            WHEN 4 THEN'A'
            WHEN 3 THEN'B'
            WHEN 2 THEN'C'
            WHEN 1 THEN'D'
            END AS AverageGrade
FROM Courses c
JOIN Enrollments e ON c.course_id=e.course_id
GROUP BY c.course_name;
END$$
DELIMITER ;

CALL GetAverageGrades();





