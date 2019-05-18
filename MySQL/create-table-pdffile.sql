use c9;

drop table if exists pdffile;

create table pdffile (
    courseNum int primary key,
    filename varchar(50),
    foreign key (courseNum) references groups(groupNum)
    on delete cascade on update cascade
)ENGINE = InnoDB;
describe pdffile;


