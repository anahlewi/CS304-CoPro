use c9;

drop table if exists users;
create table users(
	username varchar(30),
	-- password varchar(60),
	bnumber varchar(9)
	name varchar(60),
	email varchar(30),
	phone varchar(10) ,
	userType enum('Student', 'Instructor') NOT NULL, --to be renamed
	resHall varchar(30) NULL,
	primary key (bnumber)
);


drop table if exists partners;
create table partners(
	bnumber int, 
	name varchar(30), 
	assignNum int, 
	foreign key (name) references users(name) on delete cascade on update cascade,
	foreign key (bnumber) references users(bnumber) on delete cascade on update cascade,
	foreign key (assignNum) references courses(assignNum) on delete cascade on update cascade,
	primary key (assignNum)
);

drop table if exists courses;
create table courses(
	courseNum int,
	courseName varchar(60),
	instructor varchar(60) references users(name) ON DELETE CASCADE ON UPDATE CASCADE
	semester varchar(7) --i.e FA-2018
	-- assignNum int auto_increment, -- to be determined
	-- dueDate date,
	-- pairingStyle enum('Self-Pairing', 'Collaborative')
	-- primary key (courseNum)
);

drop table if exists enrollment;
create table enrollment(
	BNumber int references users(bnumber) on delete cascade on update cascade,
	courseNum int references courses(courseNum) on delete cascade on update cascade,
	primary key (bnumber, courseNum)
	
);


ENGINE = InnoDB;
