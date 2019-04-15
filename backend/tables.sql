use c9;

drop table if exists user;
csvreate table user(
	username varchar(30),
	password varchar(60),
	BNumber varchar(9)
	name varchar(60),
	email varchar(30)
	phone varchar(10) 
	categoy enum('Student', 'Instructor') NOT NULL --to be renamed
	resHall varchar(30) NULL
	primary key (BNumber)
);


drop table if exists partners;
create table partners(
	BNumber int 
	name varchar(30) 
	assignNum int 
	foreign key (name) references user(name) on delete cascade on update cascade
	foreign key (BNumber) references user(BNumber) on delete cascade on update cascade
	foreign key (assignNum) references courses(assignNum) on delete cascade on update cascade
	primary key (assignNum)
);

drop table if exists courses;
create table courses(
	CRN int,
	instructor varchar(60) references user(name) ON DELETE CASCADE ON UPDATE CASCADE
	assignNum int auto_increment, -- to be determined
	dueDate date,
	pairingStyle enum('Self-Pairing', 'Collaborative')
	primary key (assignNum)
);

ENGINE = InnoDB;