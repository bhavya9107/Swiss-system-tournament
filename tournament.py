#!/usr/bin/env python
#
# tournament.py -- implementation of a Swiss-system tournament
#

import psycopg2
from contextlib import contextmanager


def connect():
    """Connect to the PostgreSQL database.  Returns a database connection."""
    try:
        return psycopg2.connect("dbname=tournament")
    except:
        print("Connection failed")


@contextmanager
def get_cursor():
    """
    Query helper function using context lib. Creates a cursor from a database
    connection object, and performs queries using that cursor.
    """
    DB = connect()
    c = DB.cursor()
    try:
        yield c
    except:
        raise
    else:
        DB.commit()
    finally:
        c.close()
        DB.close()


def deleteMatches():
    """Remove all the match records from the database."""
    with get_cursor() as c:
        c.execute("delete from Matches;")


def deletePlayers():
    """Remove all the player records from the database."""
    with get_cursor() as c:
        c.execute("delete from Players;")


def countPlayers():
    """Returns the number of players currently registered."""
    with get_cursor() as c:
        c.execute("select count(*) from Players;")
        number = c.fetchone()[0]
        return number


def registerPlayer(name):
    """Adds a player to the tournament database.

    The database assigns a unique serial id 
    number for the player.  (This
    should be handled by your SQL database schema, 
    not in your Python code.)

    Args:
      name: the player's full name (need not be unique).
    """
    with get_cursor() as c:
        c.execute("""
            insert into 
            Players (name) 
            VALUES (%s);""", (name,))


def playerStandings():
    """Returns a list of the players and 
    their win records, sorted by wins.

    The first entry in the list should be the 
    player in first place, or a player
    tied for first place if there is currently a tie.

    Returns:
      A list of tuples, each of which 
      contains (id, name, wins, matches):
        id: the player's unique id (assigned by the database)
        name: the player's full name (as registered)
        wins: the number of matches the player has won
        matches: the number of matches the player has played
    """
    with get_cursor() as c:
        c.execute("""select Players.id, Players.name, 
            total_wins.wins, matches_played.matches
            from Players
            left join total_wins on 
            Players.id = total_wins.player
            left join matches_played on 
            Players.id = matches_played.player
            group by Players.id, Players.name, 
            total_wins.wins, matches_played.matches
            order by total_wins.wins desc;""")
        results = c.fetchall()
        return results


def reportMatch(winner, loser):
    """Records the outcome of a single match between two players.

    Args:
      winner:  the id number of the player who won
      loser:  the id number of the player who lost
    """
    with get_cursor() as c:
        c.execute("""insert into Matches (winner,loser) 
            values (%s,%s)""", (int(winner), int(loser),))


def swissPairings():
    """Returns a list of pairs of players 
    for the next round of a match.

    Assuming that there are an even number 
    of players registered, each player
    appears exactly once in the pairings.  
    Each player is paired with another
    player with an equal or nearly-equal 
    win record, that is, a player adjacent
    to him or her in the standings.

    Returns:
      A list of tuples, each of which 
      contains (id1, name1, id2, name2)
        id1: the first player's unique id
        name1: the first player's name
        id2: the second player's unique id
        name2: the second player's name
    """
    results = []
    pairings = []
    with get_cursor() as c:
        results = playerStandings()
        count = len(results)

        for x in range(0, count - 1, 2):
            paired_list = (
                results[x][0], results[x][1], results[x + 1][0], results[x + 1][1])  # noqa
            pairings.append(paired_list)
    return pairings
