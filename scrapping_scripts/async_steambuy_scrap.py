import requests
from bs4 import BeautifulSoup
import json
from fake_useragent import UserAgent
import asyncio
import aiohttp

USER = UserAgent()
HEADERS = {"User-Agent": USER.random,
           "X-Requested-With": "XMLHttpRequest",
           "Accept": "application/json, text/javascript, */*; q=0.01"
           }
COOKIE = {
    "Cookie": "__sb3_c=5b00cc250f17e70bbb24364a0c0a3823; WhiteCallback_openedPages=JoaiY.zyUVP; __sbn_uhs=a%3A3%3A%7Bi%3A1338013%3Bi%3A1%3Bi%3A2540394%3Bi%3A1%3Bi%3A2262323%3Bi%3A1%3B%7D; _ym_uid=1675873831579415744; _ym_d=1675873831; _ga=GA1.2.1249122061.1675873831; __s3_huid=11784919; __s3_hses=342ffad45521b5d1831c8037f9dc78b9d68b630f; __f_sub=0.1.0.0.1677238640; __sb_privacy_policy=1; __sbn_c=3b437df78d394d8e71e2c989f8cb76c1.1592126.9c94d3b87f8d5a61e60cbdb1488ac062; WhiteCallback_updateMainPage=JoaiY; PHPSESSID=ab11682aa4b300a8b5941a5550d15405; WhiteCallback_visit=20938423090; WhiteCallback_timeAll=7371; WhiteCallback_timePage=7371; _gid=GA1.2.75767743.1681053998; _ym_isad=1; WhiteCallback_visitorId=11658181775; WhiteSaas_uniqueLead=no; _ym_visorc=w"

}
game_list = []


async def get_offset_c():
    url = "https://steambuy.com/ajax/_get.php?rnd=0.7123840885570593&offset=0&region_free=0&sort=cnt_sell&sortMode=descendant&view=extended&a=getcat&q=&series=&publisher=&izdatel=&currency=wmr&curr=&currMaxSumm%5Bwmr%5D=3000&currMaxSumm%5Bwmz%5D=100&currMaxSumm%5Bwme%5D=70&currMaxSumm%5Bwmu%5D=1000&letter=&limit=0&page=1&minPrice=0&maxPrice=9999&minDate=0&maxDate=0&platforms%5B%5D=windows&deleted=0&no_price_range=0&records=20"
    async with aiohttp.ClientSession(headers=HEADERS, cookies=COOKIE) as session:
        responce = await session.get(url=url)
        assert responce.status == 200
        resp = await responce.json(content_type=None)
        count = int(resp["total"])
        tasks = []
        for page in range(0, (count // 20) + 1):
            task = asyncio.create_task(get_data(session, page))
            tasks.append(task)

        await asyncio.gather(*tasks)


async def get_data(session, page):
    url = f"https://steambuy.com/ajax/_get.php?rnd=0.7123840885570593&offset=0&region_free=0&sort=cnt_sell&sortMode=descendant&view=extended&a=getcat&q=&series=&publisher=&izdatel=&currency=wmr&curr=&currMaxSumm%5Bwmr%5D=3000&currMaxSumm%5Bwmz%5D=100&currMaxSumm%5Bwme%5D=70&currMaxSumm%5Bwmu%5D=1000&letter=&limit=0&page={page}&minPrice=0&maxPrice=9999&minDate=0&maxDate=0&platforms%5B%5D=windows&deleted=0&no_price_range=0&records=20"
    async with session.get(url=url) as responce:
        try:
            resp = await responce.json(content_type=None)
            assert responce.status == 200
            html = resp.get("html")
            with open(f"../scrapping_scripts/async_html/{page}.html", "w",
                      encoding="utf-8") as f:
                f.write(html)
        except:
            resp = "Not found"


def get_offset():
    url = "https://steambuy.com/ajax/_get.php?rnd=0.7123840885570593&offset=0&region_free=0&sort=cnt_sell&sortMode=descendant&view=extended&a=getcat&q=&series=&publisher=&izdatel=&currency=wmr&curr=&currMaxSumm%5Bwmr%5D=3000&currMaxSumm%5Bwmz%5D=100&currMaxSumm%5Bwme%5D=70&currMaxSumm%5Bwmu%5D=1000&letter=&limit=0&page=1&minPrice=0&maxPrice=9999&minDate=0&maxDate=0&platforms%5B%5D=windows&deleted=0&no_price_range=0&records=20"
    responce = requests.get(url=url, headers=HEADERS, cookies=COOKIE)
    data = responce.json()
    offset = data.get("total")
    return int(offset) // 20


def pars_from_html():
    for offset in range(0, get_offset() + 1):
        with open(f"../scrapping_scripts/async_html/{offset}.html",
                  encoding="utf-8") as f:
            src = f.read()
        soup = BeautifulSoup(src, "lxml")
        games = soup.find_all("div", class_="product-item")
        for game in games:
            try:
                game_name = game.find("div", class_="product-item__title").find("a").text
            except:
                game_name = "Name not found"
            try:
                game_url = f'https://steambuy.com{game.find("div", class_="product-item__title").find("a").get("href")}'
            except:
                game_url = "Url not found"
            try:
                game_price = f'{game.find("div", class_="product-item__cost").text.strip(" р")} руб.'
            except:
                game_price = "Price not found"
            game_list.append({"game_name": game_name,
                              "game_price": game_price,
                              "game_url": game_url,
                              })
        print(f'[INFO] Обработано: {offset}')


def create_json():
    with open("../database/steambuy_game_list.json", "w",
              encoding="utf-8") as f:
        json.dump(game_list, f, indent=4, ensure_ascii=False)


def main():
    loop = asyncio.get_event_loop()
    loop.run_until_complete(get_offset_c())
    pars_from_html()
    create_json()


if __name__ == "__main__":
    main()
