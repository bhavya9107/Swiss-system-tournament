--Recreate database and drop previous if exists
create database tournament;
drop database if exists tournament;
\c tournament

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
	winner integer references Players(id),
	loser integer references Players(id)
)
----------------------------------------------------------------------------------------------------------------------
-- keeps record of each player
create view total_wins as
   select Players.id as player, count(Matches.winner) as wins
    from Players left join Matches
    on Players.id = Matches.winner
    group by Players.id, Matches.winner
    order by Players.id

create view total_loses as
   	select Players.id as player, count(Matches.loser) as losses
    from Players left join Matches
    on Players.id = Matches.loser
    group by Players.id, Matches.loser
    order by Players.id
create view matches_played as
    select Players.id as player, count(Matches) as matches
    from Players left join Matches
    on(Players.id=Matches.winner) or(Players.id=Matches.loser)
    group by Players.id
    order by Players.id asc