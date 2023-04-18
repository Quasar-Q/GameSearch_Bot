import Data
from scrapping_scripts import async_steampay_scrap as SP
from scrapping_scripts import async_steambuy_scrap as SB
from scrapping_scripts import async_steamaccount_scrap as SA
from schedule import every, repeat, run_pending


@repeat(every().day.at("10:00"))
def main():
    SB.main()
    SP.main()
    SA.main()
    Data.main()


if __name__ == "__main__":
    while True:
        run_pending()

