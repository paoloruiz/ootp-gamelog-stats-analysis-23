from typing import Callable, List, Tuple
from analysis.linear_regression import linear_regress_constraints

from game_log.play import BattingPlay, Play

allowable_hits = ["DOUBLE", "TRIPLE"]
def analyze_triples_gamelog_large_filter_breakdown(all_plays: List[Play]) -> Tuple[Callable[[float], float], Callable[[BattingPlay], bool], Callable[[BattingPlay], float]]:
    batting_plays: List[BattingPlay] = list(filter(lambda p: p.playtype == "BATTING_PLAY", all_plays))

    filter_fn: Callable[[BattingPlay], bool] = lambda p: p.game_sub_result in allowable_hits
    count_fn: Callable[[BattingPlay], float] = lambda p: 1 if p.game_sub_result == "TRIPLE" else 0

    potential_bab_plays = list(filter(filter_fn, batting_plays))

    X = []
    y = []

    for play in potential_bab_plays:
        X.append([play.batting_player.speed])
        y.append(count_fn(play))


    triple_analysis = linear_regress_constraints((X, y), [0], [1])

    return triple_analysis, filter_fn, count_fn
