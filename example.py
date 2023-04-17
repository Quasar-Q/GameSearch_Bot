import sqlite3
Name = ('%Hog%',)
with sqlite3.connect('games.db') as connection:
    cursor = connection.cursor()
    cursor.execute("""SELECT * from games where Name LIKE ?""", Name)
    records = cursor.fetchall()
    for game in records:
        print(game[1])
        print(game[2])
        print(game[3])
