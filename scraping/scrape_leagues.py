from typing import List
from scraping.model.scrape_league import ScrapeLeague, read_scrape_leagues


def scrape_all_leagues():
    scrape_leagues: List[ScrapeLeague] = read_scrape_leagues()

    for sl in scrape_leagues:
        print(sl.fetch_data())