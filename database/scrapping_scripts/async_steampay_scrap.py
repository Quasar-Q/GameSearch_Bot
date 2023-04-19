import json
from fake_useragent import UserAgent
import asyncio
import aiohttp

user = UserAgent()
HEADERS = {"Accept": "application/json, text/javascript, */*; q=0.01",
           "User-Agent": user.random,
           "X-CSRF-TOKEN": "elGbByZQQDefbajKV4LhAwZfX0rcv5lD1d39Zh3k",
           "X-Requested-With": "XMLHttpRequest"
           }
COOKIES = {
    "Cookie": "XSRF-TOKEN=eyJpdiI6Ing4Nk9jMjlxak51dU9Zb0ZzQ2hValE9PSIsInZhbHVlIjoiQ1hzSExUYmVJYXBKMjg0eDA1NEg4QzRsbndkZGRmQUFPTHBcL2Y2RGFcLzVXMFJVa3ZEZm82YWxGaEFVRWVhalVtUnR6ZGpLT1lxQko5cjVjRk5jRktZQT09IiwibWFjIjoiYTNmYjRkYjAxNmZkYjJmZmQ0YzkyNTYwNGJlNjEyOWFlYmQ4MWMwM2NmYTkxMjcyZDVkMmM0OTk3MDRmMGFkYiJ9; laravel_session=KQHXvX0phf6Ys15RaYaXxZ5ohqKdJX9nj6TXR6mr; tmr_lvid=a81afa3980cb4bdd36d6c432af593b95; tmr_lvidTS=1677238349641; _ga=GA1.2.1575595540.1677238350; _ym_uid=167723835024006340; _ym_d=1677238350; _gid=GA1.2.1325068562.1678446322; _ym_isad=1; _ym_visorc=w; tmr_detect=1%7C1678446422133; _gat_gtag_UA_38248504_1=1"

}
game_list = []


async def get_counts_page():
    url = "https://steampay.com/ajax/catalog?sort=popular&inAvailable=true&page=0&currMaxSumm%5Bwmr%5D=4999&currMaxSumm%5Bwmz%5D=100&currMaxSumm%5Bwme%5D=70&currMaxSumm%5Bwmu%5D=3000&currency=wmr&minPrice=0&maxPrice=&released=false&minDate=&maxDate=&preorder=false&events=false"
    async with aiohttp.ClientSession(headers=HEADERS, cookies=COOKIES) as session:
        responce = await session.get(url=url)
        assert responce.status == 200
        data = await responce.json(content_type=None)
        pages_count = int(data["count"]) // 20

        tasks = []

        for page in range(0, pages_count + 1):
            task = asyncio.create_task(get_jsons(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


async def get_jsons(session, page):
    url = f"https://steampay.com/ajax/catalog?sort=popular&inAvailable=true&page={page}&currMaxSumm%5Bwmr%5D=4999&currMaxSumm%5Bwmz%5D=100&currMaxSumm%5Bwme%5D=70&currMaxSumm%5Bwmu%5D=3000&currency=wmr&minPrice=0&maxPrice=&released=false&minDate=&maxDate=&preorder=false&events=false"
    async with session.get(url=url) as resp:
        assert resp.status == 200
        responce = await resp.json(content_type=None)
        games = responce["products"]
        for game in games:
            try:
                game_url = f'https://steampay.com{game.get("url")}'
            except:
                game_url = "Url not found"
            try:
                game_name = game.get("name")
            except:
                game_name = "Name not found"
            try:
                game_price = game.get("price")
            except:
                game_price = "Price not found"
            game_list.append({
                "game_name": game_name,
                "game_price": f'{game_price.strip(" ₽")} руб.',
                "game_url": game_url,
            })
        print(f'[INFO] Обработано: {page}')


def create_json():
    with open("scrapping_scripts/steampay_game_list.json", "w",
              encoding="utf-8") as file:
        json.dump(game_list, file, indent=4, ensure_ascii=False)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_counts_page())
    create_json()

main()
