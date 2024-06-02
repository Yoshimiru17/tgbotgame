import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('games8.sql')
cur = conn.cursor()

with conn:
    conn.execute('''
        CREATE TABLE IF NOT EXISTS games (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name VARCHAR(50),
            mark VARCHAR(10),
            link VARCHAR(500),
            genre VARCHAR(50),
            ocenka_redaction VARCHAR(50)
        )
    ''')

ocenka_redaction = ['izumitelno', 'pohvalno', 'prohodnyak', 'musor']
genre = ["action", "add-on", "adventure", "arcade", "cards", "casual", "educational", "fighting", "for-kids", "logic",
         "massively multiplayer", "online", "racing", "rpg", "simulator", "sport", "strategy"]

for g in genre:
    for o in ocenka_redaction:
        p = 1
        while True:
            url = f"https://stopgame.ru/games/{g}/pc/{o}?year_start=2010&p={p}"
            r = requests.get(url)
            soup = BeautifulSoup(r.text, 'lxml')
            games = soup.findAll('a', class_="_card_x0dh1_1")
            next_ = soup.find('a', class_="next")
            if not next_:
                games_links = ["https://stopgame.ru" + nui.get("href") for nui in games]
                games_titles = [nui.get("title") for nui in games]
                games_genre = [g for i in range(len(games_titles))]
                games_ocenka_redaction = [o for i in range(len(games_titles))]
                games_rate = soup.findAll('button', class_='_rating_x0dh1_44')
                ratings = [button.get_text(strip=True) for button in games_rate]
                game_data_list = [(title, mark, link, games_genre[i], games_ocenka_redaction[i]) for
                                  i, (title, link, mark) in enumerate(zip(games_titles, games_links, ratings))]
                conn.executemany("INSERT INTO games (name, mark, link, genre, ocenka_redaction) VALUES (?, ?, ?, ?, ?)",
                                 game_data_list)
                break
            games_links = ["https://stopgame.ru" + nui.get("href") for nui in games]
            games_titles = [nui.get("title") for nui in games]
            games_genre = [g for i in range(len(games_titles))]
            games_ocenka_redaction = [o for i in range(len(games_titles))]
            games_rate = soup.findAll('button', class_='_rating_x0dh1_44')
            ratings = [button.get_text(strip=True) for button in games_rate]
            game_data_list = [(title, mark, link, games_genre[i], games_ocenka_redaction[i]) for i, (title, link, mark) in enumerate(zip(games_titles, games_links, ratings))]
            conn.executemany("INSERT INTO games (name, mark, link, genre, ocenka_redaction) VALUES (?, ?, ?, ?, ?)", game_data_list)
            p += 1

cursor = conn.execute("SELECT * FROM games")  # Выполнить запрос на выборку всех строк из таблицы
table_data = cursor.fetchall()  # Получить все данные из таблицы

for row in table_data:  # Отобразить каждую строку из таблицы
    print(row)
conn.commit()
cur.close()
conn.close()