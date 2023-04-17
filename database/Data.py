import json, sqlite3

PATHS = ['./steamaccount_game_list.json',
         './steambuy_game_list.json',
         './steampay_game_list.json']

GAME_LIST = []
for path in PATHS:
    with open(path, encoding="utf-8") as file:
        files = file.read()
        games = json.loads(files)
        for game in range(len(games)):
            GAME_LIST.append((game, games[game - 1]["game_name"], games[game - 1]["game_price"],
                              games[game - 1]["game_url"]))


def create_base():
    with sqlite3.connect('games.db') as connection:
        cursor = connection.cursor()
        cursor.execute("CREATE TABLE games(ID,Name,Price,Url)")
        connection.commit()


def add_data():
    with sqlite3.connect('games.db') as connection:
        cursor = connection.cursor()
        add_columns = """INSERT INTO games(ID,Name,Price,Url) VALUES (?,?,?,?);"""
        cursor.executemany(add_columns, GAME_LIST)
        connection.commit()


def delete_data():
    with sqlite3.connect('games.db') as connection:
        cursor = connection.cursor()
        select_query = """SELECT * from games"""
        cursor.execute(select_query)
        delete_query = """DELETE from games where ID=?"""
        count = cursor.fetchall()
        for id in range(len(count) + 1):
            cursor.execute(delete_query, (id,))
        connection.commit()


def main():
    try:
        create_base()
    except Exception:
        print("DB is exists")
    finally:
        delete_data()
        add_data()

if __name__ == "__main__":
    main()
