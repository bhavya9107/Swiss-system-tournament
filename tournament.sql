-- Table definitions for the tournament project.
--
-- Put your SQL 'create table' statements in this file; also 'create view'
-- statements if you choose to use it.
--
-- You can write comments in this file by starting them with two dashes, like
-- these lines here.
----------------------------------------------------------------------------------------------------------------------
-- involve information about each registered player 
create table Players(
	id integer primary key,
	name text ,
	wins integer ,
	loses integer,
	ties integer,
	matches_played integer
)
----------------------------------------------------------------------------------------------------------------------
-- involve record of each match
create table Matches(
	match_id integer primary key,
	p1 integer foreign key(Players.id),
	p2 integer foreign key(Players.id),
	player_win integer foreign key(Players.id),
	player_lose integer foreign key(Players.id),
	is_tie boolean
)
