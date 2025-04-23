create database if not exists hanoi_game_db;
use hanoi_game_db;

create table if not exists correct_responses (
	id int auto_increment primary key, 
    player_name varchar(255) not null,
    num_of_disks int not null,
    correct_moves text not null,
    timestamp timestamp default current_timestamp
);

create table if not exists algorithm_times(
	id int auto_increment primary key,
    num_of_disks int not null,
    algorithm varchar(50) not null,
    duration decimal(10, 6) not null,
    timestamp timestamp default current_timestamp
);

select * from correct_responses
 

