from typing import Callable, List, Tuple

from game_log.play import BattingPlay
from util.breakpoints import HIGH_BREAKPOINT, MID_BREAKPOINT, MIN_PLAYS


def split_throws(plays: List[BattingPlay]) -> Tuple[List[BattingPlay], List[BattingPlay]]:
    lp = list(filter(lambda p: p.pitching_player.throws == "L", plays))
    rp = list(filter(lambda p: p.pitching_player.throws == "R", plays))

    return (lp, rp)

def split_bats(plays: List[BattingPlay]) -> Tuple[List[BattingPlay], List[BattingPlay], List[BattingPlay]]:
    lb = list(filter(lambda p: p.batting_player.bats == "L", plays))
    rb = list(filter(lambda p: p.batting_player.bats == "R", plays))
    sb = list(filter(lambda p: p.batting_player.bats == "S", plays))

    return (lb, rb, sb)

def attempt_split_high_low(plays: List[BattingPlay], lam_x: Callable[[BattingPlay], List[float]]) -> Tuple[List[BattingPlay], List[BattingPlay]]:
    high_plays = list(filter(lambda p: lam_x(p)[0] >= MID_BREAKPOINT, plays))
    low_plays = list(filter(lambda p: lam_x(p)[0] < MID_BREAKPOINT, plays))

    if len(high_plays) < MIN_PLAYS or len(low_plays) < MIN_PLAYS:
        return (None, plays)

    return (high_plays, low_plays)

def attempt_split_super_high_high_low(plays: List[BattingPlay], lam_x: Callable[[BattingPlay], List[float]]) -> Tuple[List[BattingPlay], List[BattingPlay], List[BattingPlay]]:
    super_high_plays = list(filter(lambda p: lam_x(p)[0] >= HIGH_BREAKPOINT, plays))
    high_plays = list(filter(lambda p: lam_x(p)[0] >= MID_BREAKPOINT and lam_x(p)[0] < HIGH_BREAKPOINT, plays))
    low_plays = list(filter(lambda p: lam_x(p)[0] < MID_BREAKPOINT, plays))

    if len(super_high_plays) < MIN_PLAYS:
        h, l = attempt_split_high_low(plays=plays, lam_x=lam_x)
        return (None, h, l)

    return (super_high_plays, high_plays, low_plays)

# To only be called after everything else, this would perform analysis
def __split_pitcher_stat__(
    plays: List[BattingPlay],
    get_pit_stat: Callable[[BattingPlay], List[float]],
    get_analysis: Callable[[List[BattingPlay]], Callable[[List[float]], float]],
    attempt_super_split_p: bool = False
) -> Callable[[List[float]], float]:
    shp, hp, lp = None, None, None
    if attempt_super_split_p:
        shp, hp, lp = attempt_split_super_high_high_low(plays, lam_x=get_pit_stat)
    else:
        hp, lp = attempt_split_high_low(plays, lam_x=get_pit_stat)

    shp_analysis = get_analysis(shp) if shp != None else None
    hp_analysis = get_analysis(hp) if hp != None else None
    lp_analysis = get_analysis(lp) if lp != None else None

    def analyze(b_stat: List[float], p_stat: List[float]) -> float:
        if p_stat[0] >= HIGH_BREAKPOINT and shp_analysis != None:
            return shp_analysis(b_stat + p_stat)
        elif p_stat[0] >= MID_BREAKPOINT and hp_analysis != None:
            return hp_analysis(b_stat + p_stat)
        else:
            return lp_analysis(b_stat + p_stat)

    return analyze

def __split_batter_stat__(
    plays: List[BattingPlay],
    get_bat_stat: Callable[[BattingPlay], List[float]],
    get_pit_stat: Callable[[BattingPlay], List[float]],
    get_analysis: Callable[[List[BattingPlay]], Callable[[List[float]], float]],
    attempt_super_split_b: bool = False,
    attempt_super_split_p: bool = False
) -> Callable[[List[float]], float]:
    shb, hb, lb = None, None, None
    if attempt_super_split_b:
        shb, hb, lb = attempt_split_super_high_high_low(plays, lam_x=get_bat_stat)
    else:
        hb, lb = attempt_split_high_low(plays, lam_x=get_bat_stat)

    shb_analysis = __split_pitcher_stat__(shb, get_pit_stat=get_pit_stat, get_analysis=get_analysis, attempt_super_split_p=attempt_super_split_p) if shb != None else None
    hb_analysis = __split_pitcher_stat__(hb, get_pit_stat=get_pit_stat, get_analysis=get_analysis, attempt_super_split_p=attempt_super_split_p) if hb != None else None
    lb_analysis = __split_pitcher_stat__(lb, get_pit_stat=get_pit_stat, get_analysis=get_analysis, attempt_super_split_p=attempt_super_split_p) if lb != None else None

    def analyze(b_stat: List[float], p_stat: List[float]) -> float:
        if b_stat[0] >= HIGH_BREAKPOINT and shb_analysis != None:
            return shb_analysis(b_stat, p_stat)
        elif b_stat[0] >= MID_BREAKPOINT and hb_analysis != None:
            return hb_analysis(b_stat, p_stat)
        else:
            return lb_analysis(b_stat, p_stat)

    return analyze

def __split_bats__(
    plays: List[BattingPlay],
    get_bat_stat: Callable[[BattingPlay], List[float]],
    get_pit_stat: Callable[[BattingPlay], List[float]],
    get_analysis: Callable[[List[BattingPlay]], Callable[[List[float]], float]],
    attempt_super_split_b: bool = False,
    attempt_super_split_p: bool = False
) -> Callable[[str, List[float], List[float]], float]:
    lb, rb, sb = split_bats(plays)

    lb_analysis = __split_batter_stat__(lb, get_bat_stat=get_bat_stat, get_pit_stat=get_pit_stat, get_analysis=get_analysis, attempt_super_split_b=attempt_super_split_b, attempt_super_split_p=attempt_super_split_p)
    rb_analysis = __split_batter_stat__(rb, get_bat_stat=get_bat_stat, get_pit_stat=get_pit_stat, get_analysis=get_analysis, attempt_super_split_b=attempt_super_split_b, attempt_super_split_p=attempt_super_split_p)
    sb_analysis = __split_batter_stat__(sb, get_bat_stat=get_bat_stat, get_pit_stat=get_pit_stat, get_analysis=get_analysis, attempt_super_split_b=attempt_super_split_b, attempt_super_split_p=attempt_super_split_p)

    def analyze(bats: str, b_stat: List[float], p_stat: List[float]) -> float:
        if bats == "L":
            return lb_analysis(b_stat, p_stat)
        elif bats == "R":
            return rb_analysis(b_stat, p_stat)
        else:
            return sb_analysis(b_stat, p_stat)

    return analyze

def batter_v_pitcher_stat_multi_analysis(
    plays: List[BattingPlay],
    get_bat_stat: Callable[[BattingPlay], List[float]],
    get_pit_stat: Callable[[BattingPlay], List[float]],
    get_analysis: Callable[[List[BattingPlay]], Callable[[List[float]], float]],
    attempt_super_split_b: bool = False,
    attempt_super_split_p: bool = False
) -> Callable[[BattingPlay], float]:
    lp, rp = split_throws(plays)

    lp_analysis = __split_bats__(lp, get_bat_stat=get_bat_stat, get_pit_stat=get_pit_stat, get_analysis=get_analysis, attempt_super_split_b=attempt_super_split_b, attempt_super_split_p=attempt_super_split_p)
    rp_analysis = __split_bats__(rp, get_bat_stat=get_bat_stat, get_pit_stat=get_pit_stat, get_analysis=get_analysis, attempt_super_split_b=attempt_super_split_b, attempt_super_split_p=attempt_super_split_p)

    def analyze(play: BattingPlay) -> float:
        if play.pitching_player.throws == "L":
            return lp_analysis(play.batting_player.bats, get_bat_stat(play), get_pit_stat(play))
        else:
            return rp_analysis(play.batting_player.bats, get_bat_stat(play), get_pit_stat(play))

    return analyze

def batter_v_pitcher_stat_analysis_multi_breakdown(
    plays: List[BattingPlay],
    get_bat_stat: Callable[[BattingPlay], List[float]],
    get_pit_stat: Callable[[BattingPlay], List[float]],
    get_analysis: Callable[[List[BattingPlay]], Callable[[List[float]], float]],
    attempt_super_split_b: bool = False,
    attempt_super_split_p: bool = False
) -> Callable[[str, str, List[float], List[float]], float]:
    lp, rp = split_throws(plays)

    lp_analysis = __split_bats__(lp, get_bat_stat=get_bat_stat, get_pit_stat=get_pit_stat, get_analysis=get_analysis, attempt_super_split_b=attempt_super_split_b, attempt_super_split_p=attempt_super_split_p)
    rp_analysis = __split_bats__(rp, get_bat_stat=get_bat_stat, get_pit_stat=get_pit_stat, get_analysis=get_analysis, attempt_super_split_b=attempt_super_split_b, attempt_super_split_p=attempt_super_split_p)

    def analyze(throws: str, bats: str, b_stat: List[float], p_stat: List[float]) -> float:
        if throws == "L":
            return lp_analysis(bats, b_stat, p_stat)
        else:
            return rp_analysis(bats, b_stat, p_stat)

    return analyze

    