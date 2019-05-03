-- Daphka Alius
-- Miranda Hardy
-- Anah Lewi

-- Testing Code
-- This code test inserting information into the tables in the database;
use c9;


-- Users
insert into users(username, password, bnumber, name, email, phone, userType, resHall, 
availability) values ('ngina','password', 'B20814255', 'Ngina Kariuki', 
'ngina@wellesley.edu', '786-317-0000', 'Instructor', 'Tower Court West', NULL);

insert into users(username, password, bnumber, name, email, phone, userType, resHall, 
availability) values ('dalius', 'password1', 'B20800497', 'Daphka Alius', 
'dalius@wellesley.edu', '786-317-0380', 'Student', 'Tower Court West', NULL);

insert into users(username, password, bnumber, name, email, phone, userType, resHall,  
availability) values ('lanah', 'password3', 'B20800000', 'Anah Lewi', 
'alewi@wellesley.edu', '123-456-7890', 'Student', 'Stone Hall', NULL);

insert into users(username, password, bnumber, name, email, phone, userType, resHall, 
availability) values ('mhardy', 'password4', 'B20800001', 'Miranda Hardy', 
'mhardy@wellesley.edu', '098-765-4321', 'Student', 'Tower Court East', NULL);


-- Courses
insert into courses(courseNum, courseName, instructor, semester) 
values ('13587', 'Intro to the Black Experience', 'B20814255', 'FA-2019');

insert into courses(courseNum, courseName, instructor, semester) values
('15568', 'The African American Literary Tradition', 'B20814255', 'FA-2019');

insert into courses(courseNum, courseName, instructor, semester) values
('15572', 'Musical Theater', 'B20814255','SP-2019');

-- PSET
insert into psets(pid, psetTitle,courseNum, dueDate) values('0', 'Crud', '13587', '2019-07-08');

insert into psets(pid, psetTitle, courseNum, dueDate) values ('1', 'P1', '13587', '2019-07-11');
insert into psets(pid, psetTitle, courseNum, dueDate) values ('2', 'P2', '13587', '2019-07-12');
insert into	psets(pid, psetTitle, courseNum, dueDate) values ('3', 'P3', '13587', '2019-07-13');


insert into psets(pid, psetTitle, courseNum, dueDate) values ('4', 'Essay 1', '15572', '2019-08-01');
insert into psets(pid, psetTitle, courseNum, dueDate) values ('5', 'Essay 2', '15572', '2019-08-02');

insert into psets(pid, psetTitle, courseNum, dueDate) values ('6', 'PS01', '15568', '2019-08-03');
insert into psets(pid, psetTitle, courseNum, dueDate) values ('7', 'PS02', '15568', '2019-08-04');
insert into psets(pid, psetTitle, courseNum, dueDate) values ('8','PS03', '15568', '2019-08-05');
insert into psets(pid, psetTitle, courseNum) values('9', 'Homework 01', '15568');


-- Enrollment
insert into enrollment(bnumber, courseNum) values('B20800497', '15572');
insert into enrollment(bnumber, courseNum) values('B20800000', '15572');
insert into enrollment(bnumber, courseNum) values('B20800001', '15572');

insert into enrollment(bnumber, courseNum) values('B20800497', '15568');
insert into enrollment(bnumber, courseNum) values('B20800000', '15568');
insert into enrollment(bnumber, courseNum) values('B20800001', '15568');

insert into enrollment(bnumber, courseNum) values('B20800497', '13587');
insert into enrollment(bnumber, courseNum) values('B20800000', '13587');
insert into enrollment(bnumber, courseNum) values('B20800001', '13587');

-- Groups (Can't test this for some referential integrity problem)
insert into groups(groupNum, pid, courseNum) values 
('16','0', '13587');
insert into groups(groupNum, pid, courseNum) values 
('17','1', '13587');
insert into groups(groupNum, pid, courseNum) values 
('18','2', '13587');

insert into groups(groupNum, pid, courseNum) values 
('19', '6', '15568');
insert into groups(groupNum, pid, courseNum) values 
('20','7', '15568');
insert into groups(groupNum, pid, courseNum) values 
('21','8', '15568');

insert into groups(groupNum, pid, courseNum) values 
('23','4', '15572');
insert into groups(groupNum, pid, courseNum) values 
('24','5', '15572');
insert into groups(groupNum, pid, courseNum) values 
('25','9', '15572');


-- GroupsForPset
insert into groupForPset(groupNum, bnumber) values ('16', 'B20800000');
insert into groupForPset(groupNum, bnumber) values ('16', 'B20800001');
insert into groupForPset(groupNum, bnumber) values ('16', 'B20800497');

insert into groupForPset(groupNum, bnumber) values ('17', 'B20800000');
insert into groupForPset(groupNum, bnumber) values ('17', 'B20800001');
insert into groupForPset(groupNum, bnumber) values ('17', 'B20800497');

insert into groupForPset(groupNum, bnumber) values ('19', 'B20800497');
insert into groupForPset(groupNum, bnumber) values ('19', 'B20800000');
insert into groupForPset(groupNum, bnumber) values ('19', 'B20800001');

insert into groupForPset(groupNum, bnumber) values ('23', 'B20800001');
insert into groupForPset(groupNum, bnumber) values ('23', 'B20800497');
insert into groupForPset(groupNum, bnumber) values ('23', 'B20800000');




-- select pid, psetTitle, dueDate, maxSize, groupNum from psets 
-- inner join 
-- (select groupNum, courseNum, bnumber from groups 
-- inner join groupForPset using (grouPNum)
-- where courseNum = '13587') as table2 using(courseNum) 
-- where bnumber = 'B20800497';