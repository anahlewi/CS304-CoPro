-- Daphka Alius
-- Anah Lewi
-- Miranda Hardy

-- This file sets up a 'database' for the CoPro web application. The database
-- consists of tables: users, courses, groups, groupsForPset, enrollment.

-- Specify the C9 Database
use c9;


-- Drop any existing tables if necessary
drop table if exists groupForPset;
drop table if exists groups;
drop table if exists enrollment;
drop table if exists psets;
drop table if exists courses;
drop table if exists users;


-- Defining Tables
create table if not exists users(
	username varchar(30),
	bnumber varchar(9) NOT NULL,
	name varchar(60),
	password varchar(60),
	email varchar(30),
	phone varchar(12),
	userType enum('Student', 'Instructor') NOT NULL,
	resHall varchar(30) NULL,
	availability set('Monday Morning 8-12', 'Monday Afternoon 12-5', 
	'Monday Night 7-11', 'Tuesday Morning 8-12', 'Tuesday Afternoon 12-5', 
	'Tuesday Night 7-11', 'Wednesday Morning 8-12', 'Wednesday Afternoon 12-5', 
	'Wednesday Night 7-11', 'Thursday Morning 8-12', 'Thursday Afternoon 12-5', 
	'Thursday Night 7-11', 'Friday Morning 8-12', 'Friday Afternoon 12-5', 
	'Friday Night 7-11', 'Saturday Morning 8-12', 'Saturday Afternoon 12-5', 
	'Saturday Night 7-11', 'Sunday Morning 8-12', 'Sunday Afternoon 12-5', 
	'Sunday Night 7-11') NULL,
	primary key (bnumber));
	-- ENGINE = InnoDB;


create table if not exists courses(
	courseNum int,
	courseName varchar(60),
	instructor varchar(9),
	semester varchar(7), 
	foreign key (instructor) references users(bnumber),
	primary key (courseNum));
-- 	-- ENGINE	= InnoDB;

create table if not exists psets(
	pid int NOT NULL,
	psetTitle varchar(60),
	dueDate date,
	maxSize int,
	courseNum int, 
	foreign key (courseNum) references courses(courseNum) on delete cascade,
	primary key (pid))
	ENGINE = InnoDB;
	
	
create table if not exists groups(
	groupNum int NOT NULL,
	pid int,
	courseNum int,
	foreign key (pid) references psets(pid),
	foreign key (courseNum) references courses(courseNum) on delete cascade,
	primary key (groupNum))
	ENGINE	= InnoDB;


create table if not exists groupForPset(
	groupNum int,
	bnumber varchar(9),
	foreign key (groupNum) references groups(groupNum) on delete cascade,
	foreign key (bnumber) references users(bnumber))
	ENGINE	= InnoDB;
	
create table if not exists enrollment(
	courseNum int,
	bnumber varchar(9),
	foreign key(courseNum)  references courses(courseNum) on delete cascade,
	foreign key(bnumber) references users(bnumber),
	primary key (bnumber, courseNum))
	ENGINE	= InnoDB;
