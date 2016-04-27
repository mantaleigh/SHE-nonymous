-- Samantha Voigt
-- last modified: 4/16/16
-- DDL statements to create the tables for the SHE-nonymous project

-- TODO: Make sure that referential integrity works out here
-- TODO: Make sure that deleting a question in the optional_questions table will delete all the answers in the optional answers table... but do we really want to loose all that data?  Or take it upon the SHE user to save the information 

use svoigt_db;

drop table if exists login; 
drop table if exists questions; 
drop table if exists optional_answers; 
drop table if exists optional_questions; 

-- create the login table
-- The ENGINE=InnoDB allows enforcement of foreign key constraints.

create table login(
    login_id varchar(50) not null primary key, 
    passhash char(40) -- for sha1 hash
 );

-- Define the questions table
create table questions( 
    id int not null auto_increment primary key,
    ts timestamp, 
    question text not null, 
    answer text, 
    status enum("not-started", "in-progress", "completed")
);

create table optional_questions(
    opt_id int not null auto_increment primary key, 
    opt_question text, 
    INDEX (opt_id)
    )
    ENGINE = InnoDB;

create table optional_answers(
    opt_id int, 
    opt_ans text, 
    INDEX (opt_id),
    foreign key (opt_id) references optional_questions (opt_id)
    ) 
    ENGINE = InnoDB;
