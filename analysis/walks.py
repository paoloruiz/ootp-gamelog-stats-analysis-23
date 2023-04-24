from typing import Callable, List, Tuple
from analysis.batting_play_multi_stat_analysis import batter_v_pitcher_stat_analysis_multi_breakdown, batter_v_pitcher_stat_multi_analysis
from analysis.linear_regression import linear_regress_constraints

from game_log.play import BattingPlay, Play

def __get_x_y__(plays: List[BattingPlay], lam_x: Callable[[BattingPlay], List[float]], lam_y: Callable[[BattingPlay], List[float]]) -> Tuple[List[List[float]], List[float]]:
    x = list(map(lam_x, plays))
    y = list(map(lam_y, plays))

    return (x, y)

def __get_bat_stat__(p: BattingPlay) -> List[float]:
    if p.pitching_player.throws == "L":
        return [p.batting_player.eye_vl, p.times_faced_off]

    return [p.batting_player.eye_vr, p.times_faced_off]

def __get_pit_stat__(p: BattingPlay) -> List[float]:
    if p.batting_player.bats == "L":
        return [p.pitching_player.ctl_vl, p.catcher_player.cabi]
    elif p.batting_player.bats == "R":
        return [p.pitching_player.ctl_vr, p.catcher_player.cabi]

    if p.pitching_player.throws == "L":
        return [p.pitching_player.ctl_vr, p.catcher_player.cabi]

    return [p.pitching_player.ctl_vl, p.catcher_player.cabi]

MIN_CONSTRAINTS = [0, 0, -1, -1]
MAX_CONSTRAINTS = [1, 1, 0, 0]

large_filter = ["SAC_BUNT_DP", "SQUEEZE_BUNT", "BUNT_FOR_HIT", "SAC_BUNT_HIT", "CATCHERS_INTERFERENCE", "SAC_BUNT_OUT", "BUNT_FOR_HIT_OUT", "BALK", "HIT_BY_PITCH", "BUNT_FOR_HIT_DOUBLE_PLAY", "WILD_PITCH", "INTENTIONAL_WALK"]
def analyze_walks_gamelog_large_filter(all_plays: List[Play]) -> Tuple[Callable[[BattingPlay], float], Callable[[BattingPlay], bool], Callable[[BattingPlay], float]]:
    batting_plays: List[BattingPlay] = list(filter(lambda p: p.playtype == "BATTING_PLAY", all_plays))

    filter_fn: Callable[[BattingPlay], bool] = lambda p: p.game_sub_result not in large_filter
    count_fn: Callable[[BattingPlay], float] = lambda p: 1 if "WALK" in p.game_sub_result else 0

    potential_bb_plays = list(filter(filter_fn, batting_plays))

    so_analysis = batter_v_pitcher_stat_multi_analysis(
        plays=potential_bb_plays,
        get_bat_stat=__get_bat_stat__,
        get_pit_stat=__get_pit_stat__,
        get_analysis=lambda plays: linear_regress_constraints(__get_x_y__(plays, lam_x=lambda p: __get_bat_stat__(p) + __get_pit_stat__(p), lam_y=count_fn), min_constraints=MIN_CONSTRAINTS, max_constraints=MAX_CONSTRAINTS),
        attempt_super_split_b=False,
        attempt_super_split_p=False
    )

    return so_analysis, filter_fn, count_fn

def analyze_walks_gamelog_large_filter_breakdown(all_plays: List[Play]) -> Tuple[Callable[[str, str, List[float], List[float]], float], Callable[[BattingPlay], bool], Callable[[BattingPlay], float]]:
    batting_plays: List[BattingPlay] = list(filter(lambda p: p.playtype == "BATTING_PLAY", all_plays))

    filter_fn: Callable[[BattingPlay], bool] = lambda p: p.game_sub_result not in large_filter
    count_fn: Callable[[BattingPlay], float] = lambda p: 1 if "WALK" in p.game_sub_result else 0

    potential_bb_plays = list(filter(filter_fn, batting_plays))

    so_analysis = batter_v_pitcher_stat_analysis_multi_breakdown(
        plays=potential_bb_plays,
        get_bat_stat=__get_bat_stat__,
        get_pit_stat=__get_pit_stat__,
        get_analysis=lambda plays: linear_regress_constraints(__get_x_y__(plays, lam_x=lambda p: __get_bat_stat__(p) + __get_pit_stat__(p), lam_y=count_fn), min_constraints=MIN_CONSTRAINTS, max_constraints=MAX_CONSTRAINTS),
        attempt_super_split_b=False,
        attempt_super_split_p=False
    )

    return so_analysis, filter_fn, count_fn
