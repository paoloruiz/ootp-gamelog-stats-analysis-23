from typing import List, Tuple
from bs4 import BeautifulSoup
import re

def __transform_tag__(s: str) -> str:
    if s.startswith("<"):
        return re.sub("\.html\">.+</a> ", ";", s.replace("<a href=\"../players/player_", "").replace(", ", ","))
    
    return re.sub("\.html\">.+</a> ", ";", s.replace("<a href=\"../players/player_", "").replace(", ", ",").strip())[2:]

def __find_lineup_str__(lines: str) -> Tuple[List[str], List[str]]:
    starting_lineup: List[str] = []
    replacements: List[str] = []

    for line in lines:
        l = __transform_tag__(line)
        if line.startswith("<"):
            starting_lineup.append(l)
        else:
            replacements.append(l)
    
    return (starting_lineup, replacements)

def __pos_to_num__(pos: str) -> str:
    if pos == "DH":
        return "0"
    elif pos == "C":
        return "2"
    elif pos == "1B":
        return "3"
    elif pos == "2B":
        return "4"
    elif pos == "3B":
        return "5"
    elif pos == "SS":
        return "6"
    elif pos == "LF":
        return "7"
    elif pos == "CF":
        return "8"
    elif pos == "RF":
        return "9"

    return "-1"

def __format_batter_for_output__(s: str) -> str:
    spl = s.split(";")
    batter_num = spl[0]
    batter_positions = list(map(__pos_to_num__, spl[1].split(",")))

    return batter_num + ";" + ",".join(batter_positions)

def __format_pitcher_for_output__(s: str) -> str:
    return s.split(";")[0]

def __format_output__(starting_lineup: List[str], replacements: List[str], pitchers: List[str]) -> List[str]:
    out = []

    out.append("starting")
    out.extend(map(__format_batter_for_output__, starting_lineup))

    out.append("replacements")
    out.extend(map(__format_batter_for_output__, replacements))

    out.append("pitchers")
    out.extend(map(__format_pitcher_for_output__, pitchers))

    return out

def convert_box_score_html(filename: str):
    with open(filename, "r") as f:
        soup = BeautifulSoup(f.read(), "lxml")

        tables = soup.select("table.data.sortable")

        visit_batter_rows = list(map(lambda p: p.decode_contents(), tables[0].select("td.dl")))
        home_batter_rows = list(map(lambda p: p.decode_contents(), tables[1].select("td.dl")))
        visit_pitcher_rows = list(map(lambda p: p.decode_contents(), tables[2].select("td.dl")))
        home_pitcher_rows = list(map(lambda p: p.decode_contents(), tables[3].select("td.dl")))

        visiting_starters, visiting_replacements = __find_lineup_str__(visit_batter_rows)
        visiting_pitchers = list(map(__transform_tag__, visit_pitcher_rows))
        home_starters, home_replacements = __find_lineup_str__(home_batter_rows)
        home_pitchers = list(map(__transform_tag__, home_pitcher_rows))

        with open(filename.replace(".html", ".visiting.txt"), "w") as g:
            g.write("\n".join(__format_output__(visiting_starters, visiting_replacements, visiting_pitchers)))
        with open(filename.replace(".html", ".home.txt"), "w") as g:
            g.write("\n".join(__format_output__(home_starters, home_replacements, home_pitchers)))
    