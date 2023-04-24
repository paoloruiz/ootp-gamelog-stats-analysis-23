from typing import Callable, Dict, List, Tuple

from analysis.linear_regression import linear_regress_multi_pos
from cards.card_player import CardPlayer
from game_log.find_fielders_for_play import FielderPlayer, position_to_location_defenses

from game_log.play import BIPEvent, BattingPlay, Play


def __get_def_stat__(p: FielderPlayer) -> List[float]:
    pos_rating = 0
    if p.position == 1:
        pos_rating = p.player.defensep
    elif p.position == 2:
        pos_rating = p.player.defensec
    elif p.position == 3:
        pos_rating = p.player.defense1b
    elif p.position == 4:
        pos_rating = p.player.defense2b
    elif p.position == 5:
        pos_rating = p.player.defense3b
    elif p.position == 6:
        pos_rating = p.player.defensess
    elif p.position == 7:
        pos_rating = p.player.defenself
    elif p.position == 8:
        pos_rating = p.player.defensecf
    elif p.position == 9:
        pos_rating = p.player.defenserf
    if p.position < 7:
        return [p.player.ifrange, p.player.iferr, p.player.turndp, p.player.ifarm, pos_rating]

    return [p.player.ofrange, p.player.oferr, p.player.ofarm, pos_rating]

def __inner_count_fn__(p: BIPEvent) -> float:
    if p.game_outcome == "OUT":
        return 1
    elif p.game_outcome == "DOUBLE_OUT":
        return 2
    elif p.game_outcome == "TRIPLE_OUT":
        return 3

    return 0

def __count_fn__(p: BattingPlay) -> float:
    return __inner_count_fn__(p.bip_event)

def __parse_fielding_loc__(l: str) -> str:
    if l[-1] == "F":
        return l[:-1]
    return l

average_defender = CardPlayer(
    ifarm=50,
    iferr=50,
    ifrange=50,
    turndp=50,
    ofrange=50,
    ofarm=50,
    oferr=50,
    cabi=50,
    carm=50,
    defense1b=50,
    defense2b=50,
    defense3b=50,
    defensec=50,
    defensecf=50,
    defenself=50,
    defensep=50,
    defenserf=50,
    defensess=50,

    # other stuff
    cid="",
    full_title="",
    team="",
    year=0,
    name="test",
    first_name="",
    last_name="",
    position=-1,
    ovr=0,
    bats="",
    throws="",
    con_ovr=0,
    gap_ovr=0,
    pow_ovr=0,
    eye_ovr=0,
    avk_ovr=0,
    babip_ovr=0,
    con_vl=0,
    gap_vl=0,
    pow_vl=0,
    eye_vl=0,
    avk_vl=0,
    babip_vl=0,
    con_vr=0,
    gap_vr=0,
    pow_vr=0,
    eye_vr=0,
    avk_vr=0,
    babip_vr=0,
    gb_hit_type=0,
    fb_hit_type=0,
    batted_ball_type=0,
    stu_ovr=0,
    mov_ovr=0,
    ctl_ovr=0,
    stu_vl=0,
    mov_vl=0,
    ctl_vl=0,
    stu_vr=0,
    mov_vr=0,
    ctl_vr=0,
    gb_type=0,
    velocity=0,
    stamina=0,
    hold=0,
    speed=0,
    steal=0,
    baserunning=0,
    highest_buy_order=0,
    lowest_sell_order=0,
    last_10_price=0
)

def analyze_defense_gamelog_breakdown(all_plays: List[Play]) -> Tuple[Callable[[BattingPlay], float], Callable[[BattingPlay], bool], Callable[[BattingPlay], float], List[str], Callable[[CardPlayer, int], float]]:
    batting_plays: List[BattingPlay] = list(filter(lambda p: p.playtype == "BATTING_PLAY", all_plays))

    filter_fn: Callable[[BattingPlay], bool] = lambda p: p.bip_event != None and p.bip_event.location != "P"
    count_fn: Callable[[BattingPlay], float] = __count_fn__

    potential_fielding_plays = list(filter(filter_fn, batting_plays))

    play_pos_to_plays: Dict[str, List[BIPEvent]] = {}
    for play in potential_fielding_plays:
        loc = __parse_fielding_loc__(play.bip_event.location)
        # TODO maybe do this later
        if loc == "P":
            continue
        if loc not in play_pos_to_plays:
            play_pos_to_plays[loc] = []
        play_pos_to_plays[loc].append(play.bip_event)

    fielding_analysis: Dict[str, Callable[[List[float]], float]] = {}
    fielding_counts: Dict[int, Dict[str, int]] = {}
    tot_fielding_count = 0
    for i in range(2, 10):
        fielding_counts[i] = {}

    for loc in play_pos_to_plays.keys():
        X = []
        y = []
        for bip in play_pos_to_plays[loc]:
            x_p = []
            for fielder in bip.fielder:
                if loc not in fielding_counts[fielder.position]:
                    fielding_counts[fielder.position][loc] = 0
                fielding_counts[fielder.position][loc] += 1
                tot_fielding_count += 1
                x_p.extend(__get_def_stat__(fielder))
            if len(x_p) == 0:
                continue
            X.append(x_p)
            y.append(__inner_count_fn__(bip))

        fielding_analysis[loc] = linear_regress_multi_pos((X, y))

    def analyze(p: BattingPlay) -> float:
        fn = fielding_analysis[__parse_fielding_loc__(p.bip_event.location)]
        x_p = []
        for fielder in p.bip_event.fielder:
            x_p.extend(__get_def_stat__(fielder))
        return fn(x_p)

    avg_defs = {}

    for i in range(2, 10):
        ld = position_to_location_defenses(average_defender, i)
        avg_defs[i] = 0
        for fielding_loc in ld.keys():
            avg_defs[i] += fielding_analysis[fielding_loc](ld[fielding_loc]) * (fielding_counts[i][fielding_loc] / tot_fielding_count) * 26 * 162

    def analyze_fielding(p: CardPlayer, position: int) -> float:
        if position == 0:
            return 0.0
        loc_def = position_to_location_defenses(p, position)

        possible_fielding = list(loc_def.keys())

        outs_above_average = 0
        for fielding_loc in possible_fielding:
            # Outs per location multiplied by # of balls in play per game * number of games
            outs_above_average += fielding_analysis[fielding_loc](loc_def[fielding_loc]) * (fielding_counts[position][fielding_loc] / tot_fielding_count) * 26 * 162
        
        return outs_above_average - avg_defs[position]

    return analyze, filter_fn, count_fn, list(fielding_analysis.keys()), analyze_fielding
