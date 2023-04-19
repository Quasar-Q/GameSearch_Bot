import json
from fake_useragent import UserAgent
import asyncio
import aiohttp

user = UserAgent()
HEADERS = {"Accept": "application/json, text/javascript, */*; q=0.01",
           "User-Agent": user.random,
           "X-CSRF-TOKEN": "CHECK YOUR CSRFTOKEN on site and PASTE",
           "X-Requested-With": "XMLHttpRequest"
           }
COOKIES = {
    "Cookie": "CHECK YOUR COOKIE on site and PASTE"

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
