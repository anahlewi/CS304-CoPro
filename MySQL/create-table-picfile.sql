use c9;

drop table if exists picfile;

create table picfile (
    bnumber varchar(9) primary key,
    filename varchar(50),
    foreign key (bnumber) references users(bnumber)
    on delete cascade on update cascade
)ENGINE = InnoDB;
describe picfile;
