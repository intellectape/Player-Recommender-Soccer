import sqlite3
import pandas as pd
import sys

database = './data/database2.sqlite'
conn = sqlite3.connect(database)
cur = conn.cursor()

# 1 create table if needed
cur.execute("CREATE TABLE IF NOT EXISTS Player_xy (id INTEGER PRIMARY KEY, x INTEGER, y INTEGER);")
cur.execute("DELETE FROM Player_xy;")

# 2
player_positions = {}
teams = ['home_player_', 'away_player_']

for team in teams:
    for num in ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10", "11"]:
        player_id = team + num
        x = team + "X" + num
        y = team + "Y" + num

        query = "SELECT " + player_id + ", " + x + ", " + y + " FROM Match WHERE " + x + " not null AND " + player_id + " not null;"
        print query
        result = cur.execute(query)


        for row in result:
            if(row[0] not in player_positions):
                player_positions[row[0]] = {}
            if((row[1], row[2]) not in player_positions[row[0]]):
                player_positions[row[0]][(row[1], row[2])] = 1
            else:
                player_positions[row[0]][(row[1], row[2])] += 1

for player in player_positions:
    max = 0
    max_tuple = (0, 0)
    for tuple in player_positions[player]:
        if player_positions[player][tuple] > max:
            max = player_positions[player][tuple]
            max_tuple = tuple
    query = "INSERT INTO Player_xy VALUES (" + str(player) + ", " + str(max_tuple[0]) + ", " + str(max_tuple[1]) + ");"
    cur.execute(query)

conn.commit()
