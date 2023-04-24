from typing import List
from scraping.model.scrape_league import ScrapeLeague, read_box_scores_backup


def scrape_all_leagues():
    scrape_leagues: List[ScrapeLeague] = read_box_scores_backup()

    for sl in scrape_leagues:
        print(sl.fetch_box_score_backup())