use c9;

drop table if exists users;
create table users(
	username varchar(30),
	bnumber varchar(9)
	name varchar(60),
	email varchar(30),
	phone varchar(10) ,
	userType enum('Student', 'Instructor') NOT NULL, --to be renamed
	resHall varchar(30) NULL,
	availability set('Monday Morning 8-12', 'Monday Afternoon 12-5', 
	'Monday Night 7-11', 'Tuesday Morning 8-12', 'Tuesday Afternoon 12-5', 
	'Tuesday Night 7-11', 'Wednesday Morning 8-12', 'Wednesday Afternoon 12-5', 
	'Wednesday Night 7-11', 'Thursday Morning 8-12', 'Thursday Afternoon 12-5', 
	'Thursday Night 7-11', 'Friday Morning 8-12', 'Friday Afternoon 12-5', 
	'Friday Night 7-11', 'Saturday Morning 8-12', 'Saturday Afternoon 12-5', 
	'Saturday Night 7-11', 'Sunday Morning 8-12', 'Sunday Afternoon 12-5', 
	'Sunday Night 7-11',)
	primary key (bnumber)
);

drop table if exists courses;
create table courses(
	courseNum int,
	courseName varchar(60),
	instructor varchar(60)
	semester varchar(7), --i.e FA-2018
	psetNum int auto_increment,
	psetTitle varchar(30)
	maxSize  int,
	foreign key(instructor) references users(name) on delete cascade on update cascade,
	primary key (courseNum)
);

drop table if exists groups;
create table groups(
	groupNum int auto_increment,
	bnumber int,
	foreign key (bnumber) references users(bnumber) on delete cascade on update cascade,
	primary key (groupNum, bnumber)
);

drop table if exists groupByPset;
create table groupForPset(
	groupNum int,
	psetNum int,
	foreign key (groupNum) references groups(groupNum) on delete cascade on update cascade,
	foreign key (psetNum) references courses(psetNum) on delete cascade on update cascade,
	primary key (groupNum, psetNum)
);

drop table if exists enrollment;
create table enrollment(
	BNumber int references users(bnumber) on delete cascade on update cascade,
	courseNum int references courses(courseNum) on delete cascade on update cascade,
	primary key (bnumber, courseNum)
);


ENGINE = InnoDB;
