-- Daphka Alius
-- Anah Lewi
-- Miranda Hardy

-- This file set ups a 'database' for the CoPro web application. The database
-- consists of tables: users, courses, groups, groupsForPset, enrollment.

-- Specify the C9 Database
use c9;


-- Drop any existing tables if necessary
drop table if exists users;
drop table if exists courses;
drop table if exists groups;
drop table if exists groupForPset;
drop table if exists enrollment;

-- Defining Tables
create table if not exists users(
	username varchar(30),
	bnumber varchar(9)
	name varchar(60),
	email varchar(30),
	phone varchar(10),
	userType enum('Student', 'Instructor') NOT NULL,
	resHall varchar(30) NULL,
	availability set('Monday Morning 8-12', 'Monday Afternoon 12-5', 
	'Monday Night 7-11', 'Tuesday Morning 8-12', 'Tuesday Afternoon 12-5', 
	'Tuesday Night 7-11', 'Wednesday Morning 8-12', 'Wednesday Afternoon 12-5', 
	'Wednesday Night 7-11', 'Thursday Morning 8-12', 'Thursday Afternoon 12-5', 
	'Thursday Night 7-11', 'Friday Morning 8-12', 'Friday Afternoon 12-5', 
	'Friday Night 7-11', 'Saturday Morning 8-12', 'Saturday Afternoon 12-5', 
	'Saturday Night 7-11', 'Sunday Morning 8-12', 'Sunday Afternoon 12-5', 
	'Sunday Night 7-11',),
	primary key (bnumber))
	ENGINE = InnoDB;

create table if not exists courses(
	courseNum int,
	courseName varchar(60),
	instructor varchar(60),
	semester varchar(7), 
	psetNum int auto_increment,
	psetTitle varchar(30)
	maxSize  int,
	dueDate date,
	foreign key(instructor) references users(name) on delete restrict on update cascade,
	primary key (courseNum))
	ENGINE	= InnoDB;

create table if not exists groups(
	groupNum int auto_increment,
	bnumber int,
	foreign key (bnumber) references users(bnumber) on delete set null on update cascade,
	primary key (groupNum, bnumber))
	ENGINE	= InnoDB;

create table if not exists groupForPset(
	groupNum int,
	psetNum int,
	foreign key (groupNum) references groups(groupNum) on delete cascade on update cascade,
	foreign key (psetNum) references courses(psetNum) on delete cascade on update cascade,
	primary key (groupNum, psetNum))
	ENGINE	= InnoDB;

create table if not exists enrollment(
	BNumber int references users(bnumber) on delete cascade on update cascade,
	courseNum int references courses(courseNum) on delete cascade on update cascade,
	primary key (bnumber, courseNum))
	ENGINE	= InnoDB;
