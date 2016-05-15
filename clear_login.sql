-- Samantha Voigt
-- Clears out the login table, to be run at the end of every semester


use svoigt_db;

drop table if exists login; 

create table login(
    login_id varchar(50) not null primary key, 
    passhash char(40) -- for sha1 hash
 );
