-- Daphka Alius
-- Miranda Hardy
-- Anah Lewi

-- Testing Code
-- This code test inserting information into the tables in the database;
use c9;
-- Users
-- insert into users(username, password, bnumber, name, email, phone, userType, resHall, 
-- availability) values ('ngina','password', 'B20814255', 'Ngina Kariuki', 
-- 'ngina@wellesley.edu', '786-317-0000', 'Instructor', 'Tower Court West', NULL);

-- insert into users(username, password, bnumber, name, email, phone, userType, resHall, 
-- availability) values ('dalius', 'password1', 'B20800497', 'Daphka Alius', 
-- 'dalius@wellesley.edu', '786-317-0380', 'Student', 'Tower Court West', NULL);

-- insert into users(username, password, bnumber, name, email, phone, userType, resHall,  
-- availability) values ('lanah', 'password3', 'B20800000', 'Anah Lewi', 
-- 'alewi@wellesley.edu', '123-456-7890', 'Student', 'Stone Hall', NULL);

-- insert into users(username, password, bnumber, name, email, phone, userType, resHall, 
-- availability) values ('mhardy', 'password4', 'B20800001', 'Miranda Hardy', 
-- 'mhardy@wellesley.edu', '098-765-4321', 'Student', 'Tower Court East', NULL);


-- insert into courses(courseNum, courseName, instructor, semester) 
-- values ('13587', 'Intro to the Black Experience', 'B20814255', 'FA-2019');

-- insert into courses(courseNum, courseName, instructor, semester) values
-- ('15568', 'The African American Literary Tradition', 'B20814255', 'FA-2019');

-- insert into courses(courseNum, courseName, instructor, semester) values
-- ('15572', 'Musical Theater', 'B20814255','SP-2019');

-- -- PSET
-- insert into psets(psetTitle,courseNum) values('Crud', '13587');

-- -- Groups
-- insert into groups(bnumber) values ('B20800497');
-- insert into groups(bnumber) values ('B20800000');
-- insert into groups(bnumber) values ('B20800001');

-- -- GroupsForPset
-- insert into groups(bnumber) values ('B20800000');

-- insert into enrollment(bnumber, courseNum) values('B20800497', '15772');
-- insert into enrollment(bnumber, courseNum) values('B20800000', '15772');
-- insert into enrollment(bnumber, courseNum) values('B20800001', '15772');

-- insert into enrollment(bnumber, courseNum) values('B20800497', '15568');
-- insert into enrollment(bnumber, courseNum) values('B20800000', '15568');
-- insert into enrollment(bnumber, courseNum) values('B20800001', '15568');

-- insert into enrollment(bnumber, courseNum) values('B20800497', '13587');
-- insert into enrollment(bnumber, courseNum) values('B20800000', '13587');
-- insert into enrollment(bnumber, courseNum) values('B20800001', '13587');


