from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
import asyncio
import aiohttp




USER = UserAgent()
HEADERS = {"User-Agent": USER.random
           }

game_list = []


async def get_games_count():
    url = "https://steam-account.ru/steam_kluchi_kupit/page/17"
    async with aiohttp.ClientSession(headers=HEADERS) as session:
        responce = await session.get(url=url)
        assert responce.status == 200
        soup = BeautifulSoup(await responce.text(), "lxml")
        count = int(soup.find("ul", class_="pagination-inner").find_all("a")[-1].text)

        tasks = []

        for page in range(0, count + 1):
            task = asyncio.create_task(get_data(session, page))
            tasks.append(task)
        await asyncio.gather(*tasks)


async def get_data(session, page):
    url = f"https://steam-account.ru/steam_kluchi_kupit/page/{page}"
    async with session.get(url=url) as responce:
        responce = await responce.text()
        soup = BeautifulSoup(responce, "lxml")
        try:
            games = soup.find("div", class_="row page-content").find_all("div", class_="game-item")
            for game in games:
                try:
                    game_name = game.find("div", class_="game-name").text
                except:
                    game_name = "Name not found"
                try:
                    game_price = game.find("div", class_="price").find("div", class_="price-span simple").text
                except:
                    game_price = "Price not found"
                try:
                    game_url = f'https://steam-account.ru{game.find("a").get("href")}'
                except:
                    game_url = "Url not found"
                game_list.append({"game_name": game_name,
                                  "game_price": game_price,
                                  "game_url": game_url,
                                  })
        except:
            games = 'Games not found'
        print(f'[INFO] Обработано: {page}')


def create_json():
    with open("../database/steamaccount_game_list.json", "w", encoding="utf-8") as f:
        json.dump(game_list, f, indent=4, ensure_ascii=False)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_games_count())
    create_json()


if __name__ == "__main__":
    main()
