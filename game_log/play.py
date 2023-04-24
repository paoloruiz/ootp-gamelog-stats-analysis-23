from dataclasses import dataclass
from typing import List
from cards.card_player import CardPlayer
from game_log.find_fielders_for_play import FielderPlayer


@dataclass
class Play:
    playtype: str
    cur_inning: int
    cur_team: str

@dataclass
class BIPEvent:
    fielder: List[FielderPlayer]
    batter: CardPlayer
    location: str
    batted_ball_type: int
    game_outcome: str


@dataclass
class BattingPlay(Play):
    pitching_player: CardPlayer
    batting_player: CardPlayer
    catcher_player: CardPlayer
    # How many times the pitcher/batter have faced each other this game
    times_faced_off: int
    baseball_result: str
    game_sub_result: str
    bip_event: BIPEvent

@dataclass
class BaseRunningPlay(Play):
    pitching_player: CardPlayer
    running_player: CardPlayer
    catcher_player: CardPlayer
    result: str
    # where people were on base at start of play
    men_on_base: str
