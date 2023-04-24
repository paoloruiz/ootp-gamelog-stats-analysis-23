from dataclasses import dataclass
from typing import List
from bs4 import BeautifulSoup
import os
from scraping.box_score_converter import convert_box_score_html

from scraping.util.read_url import get_html_from_url_full_req

def __write_game_files__():
    pass


@dataclass
class ScrapeLeague:
    lg_hash: str
    league_url: str
    box_score_url: str
    league_name: str

    def __get_folder__(self) -> str:
        if self.league_name.startswith("T"):
            return "/tournament/"
        return "/league/"

    def fetch_data(self):
        os.makedirs("data" + self.__get_folder__() + self.league_name + "/games/", exist_ok=True)
        os.makedirs("data" + self.__get_folder__() + self.league_name + "/box_scores/", exist_ok=True)
        with open("data" + self.__get_folder__() + self.league_name + "/lg_hash.txt", "w") as f:
            f.write(self.lg_hash)

        for i in range(10000):
            html = get_html_from_url_full_req(self.league_url + "log_" + str(i + 1) + ".txt")
            if html == None:
                break

            soup = BeautifulSoup(html, "lxml")

            game_text = soup.find("p").getText()

            with open("data" + self.__get_folder__() + self.league_name + "/games/" + str(i) + ".txt", "w") as f:
                f.write(game_text)

            box_score_html = get_html_from_url_full_req(self.box_score_url + "game_box_" + str(i + 1) + ".html")
            with  open("data" + self.__get_folder__() + self.league_name + "/box_scores/" + str(i) + ".html", "w", encoding="utf-8") as f:
                f.write(box_score_html.decode("utf-8", errors="ignore"))
            convert_box_score_html("data" + self.__get_folder__() + self.league_name + "/box_scores/" + str(i) + ".html")

def __get_league_url__(lg_name: str) -> str:
    url = "http://35.190.82.228/saved_games/"

    split_lg_name = [lg_name[i:i+3] for i in range(0, len(lg_name), 3)]
    for lg_name_part in split_lg_name:
        url += lg_name_part + "/"

    url += lg_name + ".pt/news/txt/leagues/"
    
    return url


def __get_box_score_url__(lg_name: str) -> str:
    url = "http://35.190.82.228/saved_games/"

    split_lg_name = [lg_name[i:i+3] for i in range(0, len(lg_name), 3)]
    for lg_name_part in split_lg_name:
        url += lg_name_part + "/"

    url += lg_name + ".pt/news/html/box_scores/"
    
    return url

def read_scrape_leagues() -> List[ScrapeLeague]:
    scrape_leagues: List[ScrapeLeague] = []
    with open("leagues_to_scrape.txt", "r") as f:
        for line in f.readlines():
            line_split = line.strip().split(",")
            lg_hash = line_split[0]

            scrape_leagues.append(ScrapeLeague(lg_hash=lg_hash, league_url=__get_league_url__(lg_hash), box_score_url=__get_box_score_url__(lg_hash), league_name=line_split[1]))
    return scrape_leagues