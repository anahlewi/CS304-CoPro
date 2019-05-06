use c9;

drop table if exists picblob;
create table picblob (
    bnumber varchar(9) primary key,
    image blob,
    foreign key (bnumber) references users(bnumber) 
    on delete cascade on update cascade
);
describe picblob;
