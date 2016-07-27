#!/usr/bin/env python
# 
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    return psycopg2.connect("dbname=tournament")


DB=connect()
c=DB.cursor()
    for p in Players:
        p.wins=c.execute("select count(*) as num from Matches where p1 = p.id or p2= p.id and player_win=p.id;")
        p.loses=c.execute("select count(*) as num from Matches where p1 = p.id or p2= p.id and player_loses=p.id;")
        p.ties=c.execute("select count(*) as num from Matches where p1 = p.id or p2= p.id and is_tie=True;")
        p.matches_played=c.execute("select count(*) as matches from Matches where p1= p.id or p2=p.id;")


def deleteMatches():
    """Remove all the match records from the database."""
    DB=connect()
    c=DB.cursor()
    c.execute("delete * from Matches;")
    DB.commit()
    DB.close()


def deletePlayers():
    """Remove all the player records from the database."""
    DB=connect()
    c=DB.cursor()
    c.execute("delete * from Players;")
    DB.commit()
    DB.close()


def countPlayers():
    """Returns the number of players currently registered."""
    DB=connect()
    c=DB.cursor()
    n=c.execute("select count(*) as num from Players;")
    DB.close()
    return n


def registerPlayer(name):
    """Adds a player to the tournament database.
  
    The database assigns a unique serial id number for the player.  (This
    should be handled by your SQL database schema, not in your Python code.)
  
    Args:
      name: the player's full name (need not be unique).
    """
    DB=connect()
    c=DB.cursor()
    c.execute("insert into Players(name, wins, loses, ties, matches_played) value(name, 0, 0, 0, 0);")
    DB.commit()
    DB.close()


def playerStandings():
    """Returns a list of the players and their win records, sorted by wins.

    The first entry in the list should be the player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    DB=connect()
    c=DB.cursor()
    results= c.execute("select id, name, wins,matches_played from Players order by wins;")
    return results


def reportMatch(winner, loser,tie):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    DB=connect()
    c=DB.cursor()
    for p in Players:
        if p.id==int(winner):
            p.wins+=1
            p.matches_played+=1
        elif p.id==int(loser):
            p.loses+=1
            p.matches_played+=1
        elif tie==True:
            if p.id==int(Matches.p1) or p.id==int(Matches.p2):
                p.ties+=1
                p.matches_played+=1
    DB.commit()
    DB.close()


def swissPairings():
    """Returns a list of pairs of players for the next round of a match.
  
    Assuming that there are an even number of players registered, each player
    appears exactly once in the pairings.  Each player is paired with another
    player with an equal or nearly-equal win record, that is, a player adjacent
    to him or her in the standings.
  
    Returns:
      A list of tuples, each of which contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    DB=connect()
    c=DB.cursor()
    result=playerStandings()
    c.execute(";")