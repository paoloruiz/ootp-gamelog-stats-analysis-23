from dataclasses import dataclass
from typing import List

from cards.card_player import CardPlayer

@dataclass
class ManOnBase:
    runner: CardPlayer
    base: int

@dataclass
class FielderLayout:
    pitcher: CardPlayer
    catcher: CardPlayer
    first_base: CardPlayer
    second_base: CardPlayer
    third_base: CardPlayer
    shortstop: CardPlayer
    left_field: CardPlayer
    center_field: CardPlayer
    right_field: CardPlayer
    designated_hitter: CardPlayer


# The engine for reading in files and determining who was involved in a play
@dataclass
class GameEngine:
    visiting_team: str
    home_team: str
    visiting_pitcher: CardPlayer
    home_pitcher: CardPlayer
    current_batter: CardPlayer
    men_on_base: List[ManOnBase]
    visiting_fielding_layout: FielderLayout
    home_fielding_layout: FielderLayout
    cur_hitting_team: str
    