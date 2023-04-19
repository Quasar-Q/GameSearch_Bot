import Data
from scrapping_scripts.async_steambuy_scrap import main as SB
from scrapping_scripts.async_steampay_scrap import main as SP
from scrapping_scripts.async_steamaccount_scrap import main as SA
from schedule import every, repeat, run_pending


@repeat(every().day.at("05:00"))
def main():
    SB()
    SP()
    SA()
    Data.main()


if __name__ == "__main__":
    while True:
        run_pending()

