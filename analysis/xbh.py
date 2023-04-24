from typing import Callable, List, Tuple
from analysis.batting_play_multi_stat_analysis import batter_v_pitcher_stat_analysis_multi_breakdown, batter_v_pitcher_stat_multi_analysis
from analysis.linear_regression import linear_regress_multi

from game_log.play import BattingPlay, Play

def __get_x_y__(plays: List[BattingPlay], lam_x: Callable[[BattingPlay], List[float]], lam_y: Callable[[BattingPlay], List[float]]) -> Tuple[List[List[float]], List[float]]:
    x = list(map(lam_x, plays))
    y = list(map(lam_y, plays))

    return (x, y)

def __get_bat_stat__(p: BattingPlay) -> List[float]:
    if p.pitching_player.throws == "L":
        return [p.batting_player.gap_vl]

    return [p.batting_player.gap_vr]

def __get_pit_stat__(p: BattingPlay) -> List[float]:
    return [0]

allowable_hits = ["DOUBLE", "TRIPLE"]
large_filter = ["WALK", "GITP", "BIP_ERROR", "GIDP", "BIP_OUT", "STRIKEOUT_W_CAUGHT_STEALING", "HOME_RUN", "STIKEOUT", "FIELDERS_CHOICE",
    "SAC_BUNT_DP", "SQUEEZE_BUNT", "BUNT_FOR_HIT", "SAC_BUNT_HIT", "SAC_BUNT_OUT", "BUNT_FOR_HIT_OUT", "BUNT_FOR_HIT_DOUBLE_PLAY", "CATCHERS_INTERFERENCE", "BALK", "HIT_BY_PITCH", "WILD_PITCH", "INTENTIONAL_WALK"]
def analyze_xbh_gamelog_large_filter(all_plays: List[Play]) -> Tuple[Callable[[BattingPlay], float], Callable[[BattingPlay], bool], Callable[[BattingPlay], float]]:
    batting_plays: List[BattingPlay] = list(filter(lambda p: p.playtype == "BATTING_PLAY", all_plays))

    filter_fn: Callable[[BattingPlay], bool] = lambda p: p.game_sub_result not in large_filter
    count_fn: Callable[[BattingPlay], float] = lambda p: 1 if p.game_sub_result in allowable_hits else 0

    potential_bab_plays = list(filter(filter_fn, batting_plays))

    xbh_analysis = batter_v_pitcher_stat_multi_analysis(
        plays=potential_bab_plays,
        get_bat_stat=__get_bat_stat__,
        get_pit_stat=__get_pit_stat__,
        get_analysis=lambda plays: linear_regress_multi(__get_x_y__(plays, lam_x=lambda p: __get_bat_stat__(p) + __get_pit_stat__(p), lam_y=count_fn)),
        attempt_super_split_b=False,
        attempt_super_split_p=True
    )

    return xbh_analysis, filter_fn, count_fn

def analyze_xbh_gamelog_large_filter_breakdown(all_plays: List[Play]) -> Tuple[Callable[[str, str, float, float], float], Callable[[BattingPlay], bool], Callable[[BattingPlay], float]]:
    batting_plays: List[BattingPlay] = list(filter(lambda p: p.playtype == "BATTING_PLAY", all_plays))

    filter_fn: Callable[[BattingPlay], bool] = lambda p: p.game_sub_result not in large_filter
    count_fn: Callable[[BattingPlay], float] = lambda p: 1 if p.game_sub_result in allowable_hits else 0

    potential_bab_plays = list(filter(filter_fn, batting_plays))

    xbh_analysis = batter_v_pitcher_stat_analysis_multi_breakdown(
        plays=potential_bab_plays,
        get_bat_stat=__get_bat_stat__,
        get_pit_stat=__get_pit_stat__,
        get_analysis=lambda plays: linear_regress_multi(__get_x_y__(plays, lam_x=lambda p: __get_bat_stat__(p) + __get_pit_stat__(p), lam_y=count_fn)),
        attempt_super_split_b=False,
        attempt_super_split_p=True
    )

    return xbh_analysis, filter_fn, count_fn
