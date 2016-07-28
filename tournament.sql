-- Table definitions for the tournament project.
----------------------------------------------------------------------------------------------------------------------
-- involve information about each registered player 
create table Players(
	id serial primary key,
	name text
)
----------------------------------------------------------------------------------------------------------------------
-- involve record of each match
create table Matches(
	match_id serial primary key,
	p1 integer references Players(id),
	p2 integer references Players(id),
	player_win integer,
	player_lose integer
)
----------------------------------------------------------------------------------------------------------------------
-- keeps record of each player
create table Records(
	id integer references Players(id),
	wins integer,
	loses integer,
	matches_played integer
)