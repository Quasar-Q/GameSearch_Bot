from Database import Data
import scrapping_scripts.async_steampay_scrap as SP
import scrapping_scripts.async_steambuy_scrap as SB
import scrapping_scripts.async_steamaccount_scrap as SA


def main():
    SB.main()
    SP.main()
    SA.main()
    Data.main()


if __name__ == "__main__":
    main()
