from dataclasses import dataclass
from typing import Callable, List
from analysis.pitcher_peripherals import PitchingPlayerFormulas
from cards.card_player import CardPlayer
from analysis.find_top_team_players import TeamBreakdown
from individual_league.determine_linear_weights import LinearWeightsFormulas
from individual_league.pitcher_stats import PitcherStats


def __get_walk_rate__(
    pitcher: CardPlayer,
    throws: str,
    team_breakdown: TeamBreakdown,
    bb_analysis: Callable[[str, str, List[float], List[float]], float]
):
    r_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["R"]["eye"]
    l_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["L"]["eye"]
    s_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["S"]["eye"]

    r_bb_low = r_starting["low"][0] / r_starting["low"][1] if r_starting["low"][1] > 0 else 0
    r_bb_high = r_starting["high"][0] / r_starting["high"][1] if r_starting["high"][1] > 0 else 0
    r_bb_super = r_starting["super"][0] / r_starting["super"][1] if r_starting["super"][1] > 0 else 0

    l_bb_low = l_starting["low"][0] / l_starting["low"][1] if l_starting["low"][1] > 0 else 0
    l_bb_high = l_starting["high"][0] / l_starting["high"][1] if l_starting["high"][1] > 0 else 0
    l_bb_super = l_starting["super"][0] / l_starting["super"][1] if l_starting["super"][1] > 0 else 0

    s_bb_low = s_starting["low"][0] / s_starting["low"][1] if s_starting["low"][1] > 0 else 0
    s_bb_high = s_starting["high"][0] / s_starting["high"][1] if s_starting["high"][1] > 0 else 0
    s_bb_super = s_starting["super"][0] / s_starting["super"][1] if s_starting["super"][1] > 0 else 0

    tot_count = r_starting["low"][1] + r_starting["high"][1] + r_starting["super"][1] + l_starting["low"][1] + l_starting["high"][1] + l_starting["super"][1] + s_starting["low"][1] + s_starting["high"][1] + s_starting["super"][1]

    switch_stat = pitcher.ctl_vl if pitcher.throws == "R" else pitcher.ctl_vr
    walks_vl_r_low = bb_analysis(pitcher.throws, "R", [r_bb_low, 1], [pitcher.ctl_vr, team_breakdown.get_cabi()]) * r_starting["low"][1] / tot_count
    walks_vl_r_high = bb_analysis(pitcher.throws, "R", [r_bb_high, 1], [pitcher.ctl_vr, team_breakdown.get_cabi()]) * r_starting["high"][1] / tot_count
    walks_vl_r_super = bb_analysis(pitcher.throws, "R", [r_bb_super, 1], [pitcher.ctl_vr, team_breakdown.get_cabi()]) * r_starting["super"][1] / tot_count

    walks_vl_l_low = bb_analysis(pitcher.throws, "L", [l_bb_low, 1], [pitcher.ctl_vl, team_breakdown.get_cabi()]) * l_starting["low"][1] / tot_count
    walks_vl_l_high = bb_analysis(pitcher.throws, "L", [l_bb_high, 1], [pitcher.ctl_vl, team_breakdown.get_cabi()]) * l_starting["high"][1] / tot_count
    walks_vl_l_super = bb_analysis(pitcher.throws, "L", [l_bb_super, 1], [pitcher.ctl_vl, team_breakdown.get_cabi()]) * l_starting["super"][1] / tot_count

    walks_vl_s_low = bb_analysis(pitcher.throws, "S", [s_bb_low, 1], [switch_stat, team_breakdown.get_cabi()]) * s_starting["low"][1] / tot_count
    walks_vl_s_high = bb_analysis(pitcher.throws, "S", [s_bb_high, 1], [switch_stat, team_breakdown.get_cabi()]) * s_starting["high"][1] / tot_count
    walks_vl_s_super = bb_analysis(pitcher.throws, "S", [s_bb_super, 1], [switch_stat, team_breakdown.get_cabi()]) * s_starting["super"][1] / tot_count

    return walks_vl_r_low + walks_vl_r_high + walks_vl_r_super + walks_vl_l_low + walks_vl_l_high + walks_vl_l_super + walks_vl_s_low + walks_vl_s_high + walks_vl_s_super

def __get_homerun_rate__(
    pitcher: CardPlayer,
    throws: str,
    team_breakdown: TeamBreakdown,
    hr_analysis: Callable[[str, str, List[float], List[float]], float]
):
    r_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["R"]["pow"]
    l_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["L"]["pow"]
    s_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["S"]["pow"]

    r_hr_low = r_starting["low"][0] / r_starting["low"][1] if r_starting["low"][1] > 0 else 0
    r_hr_high = r_starting["high"][0] / r_starting["high"][1] if r_starting["high"][1] > 0 else 0
    r_hr_super = r_starting["super"][0] / r_starting["super"][1] if r_starting["super"][1] > 0 else 0

    l_hr_low = l_starting["low"][0] / l_starting["low"][1] if l_starting["low"][1] > 0 else 0
    l_hr_high = l_starting["high"][0] / l_starting["high"][1] if l_starting["high"][1] > 0 else 0
    l_hr_super = l_starting["super"][0] / l_starting["super"][1] if l_starting["super"][1] > 0 else 0

    s_hr_low = s_starting["low"][0] / s_starting["low"][1] if s_starting["low"][1] > 0 else 0
    s_hr_high = s_starting["high"][0] / s_starting["high"][1] if s_starting["high"][1] > 0 else 0
    s_hr_super = s_starting["super"][0] / s_starting["super"][1] if s_starting["super"][1] > 0 else 0

    tot_count = r_starting["low"][1] + r_starting["high"][1] + r_starting["super"][1] + l_starting["low"][1] + l_starting["high"][1] + l_starting["super"][1] + s_starting["low"][1] + s_starting["high"][1] + s_starting["super"][1]

    switch_stat = pitcher.mov_vl if pitcher.throws == "R" else pitcher.mov_vr
    homeruns_vl_r_low = hr_analysis(pitcher.throws, "R", [r_hr_low, 1], [pitcher.mov_vr, team_breakdown.get_cabi()]) * r_starting["low"][1] / tot_count
    homeruns_vl_r_high = hr_analysis(pitcher.throws, "R", [r_hr_high, 1], [pitcher.mov_vr, team_breakdown.get_cabi()]) * r_starting["high"][1] / tot_count
    homeruns_vl_r_super = hr_analysis(pitcher.throws, "R", [r_hr_super, 1], [pitcher.mov_vr, team_breakdown.get_cabi()]) * r_starting["super"][1] / tot_count

    homeruns_vl_l_low = hr_analysis(pitcher.throws, "L", [l_hr_low, 1], [pitcher.mov_vl, team_breakdown.get_cabi()]) * l_starting["low"][1] / tot_count
    homeruns_vl_l_high = hr_analysis(pitcher.throws, "L", [l_hr_high, 1], [pitcher.mov_vl, team_breakdown.get_cabi()]) * l_starting["high"][1] / tot_count
    homeruns_vl_l_super = hr_analysis(pitcher.throws, "L", [l_hr_super, 1], [pitcher.mov_vl, team_breakdown.get_cabi()]) * l_starting["super"][1] / tot_count

    homeruns_vl_s_low = hr_analysis(pitcher.throws, "S", [s_hr_low, 1], [switch_stat, team_breakdown.get_cabi()]) * s_starting["low"][1] / tot_count
    homeruns_vl_s_high = hr_analysis(pitcher.throws, "S", [s_hr_high, 1], [switch_stat, team_breakdown.get_cabi()]) * s_starting["high"][1] / tot_count
    homeruns_vl_s_super = hr_analysis(pitcher.throws, "S", [s_hr_super, 1], [switch_stat, team_breakdown.get_cabi()]) * s_starting["super"][1] / tot_count

    return homeruns_vl_r_low + homeruns_vl_r_high + homeruns_vl_r_super + homeruns_vl_l_low + homeruns_vl_l_high + homeruns_vl_l_super + homeruns_vl_s_low + homeruns_vl_s_high + homeruns_vl_s_super

def __get_strikeout_rate__(
    pitcher: CardPlayer,
    throws: str,
    team_breakdown: TeamBreakdown,
    so_analysis: Callable[[str, str, List[float], List[float]], float]
):
    r_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["R"]["avk"]
    l_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["L"]["avk"]
    s_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["S"]["avk"]

    r_k_low = r_starting["low"][0] / r_starting["low"][1] if r_starting["low"][1] > 0 else 0
    r_k_high = r_starting["high"][0] / r_starting["high"][1] if r_starting["high"][1] > 0 else 0
    r_k_super = r_starting["super"][0] / r_starting["super"][1] if r_starting["super"][1] > 0 else 0

    l_k_low = l_starting["low"][0] / l_starting["low"][1] if l_starting["low"][1] > 0 else 0
    l_k_high = l_starting["high"][0] / l_starting["high"][1] if l_starting["high"][1] > 0 else 0
    l_k_super = l_starting["super"][0] / l_starting["super"][1] if l_starting["super"][1] > 0 else 0

    s_k_low = s_starting["low"][0] / s_starting["low"][1] if s_starting["low"][1] > 0 else 0
    s_k_high = s_starting["high"][0] / s_starting["high"][1] if s_starting["high"][1] > 0 else 0
    s_k_super = s_starting["super"][0] / s_starting["super"][1] if s_starting["super"][1] > 0 else 0

    tot_count = r_starting["low"][1] + r_starting["high"][1] + r_starting["super"][1] + l_starting["low"][1] + l_starting["high"][1] + l_starting["super"][1] + s_starting["low"][1] + s_starting["high"][1] + s_starting["super"][1]

    switch_stat = pitcher.stu_vl if pitcher.throws == "R" else pitcher.stu_vr
    strikeouts_vl_r_low = so_analysis(pitcher.throws, "R", [r_k_low, 1], [pitcher.stu_vr, team_breakdown.get_cabi()]) * r_starting["low"][1] / tot_count
    strikeouts_vl_r_high = so_analysis(pitcher.throws, "R", [r_k_high, 1], [pitcher.stu_vr, team_breakdown.get_cabi()]) * r_starting["high"][1] / tot_count
    strikeouts_vl_r_super = so_analysis(pitcher.throws, "R", [r_k_super, 1], [pitcher.stu_vr, team_breakdown.get_cabi()]) * r_starting["super"][1] / tot_count

    strikeouts_vl_l_low = so_analysis(pitcher.throws, "L", [l_k_low, 1], [pitcher.stu_vl, team_breakdown.get_cabi()]) * l_starting["low"][1] / tot_count
    strikeouts_vl_l_high = so_analysis(pitcher.throws, "L", [l_k_high, 1], [pitcher.stu_vl, team_breakdown.get_cabi()]) * l_starting["high"][1] / tot_count
    strikeouts_vl_l_super = so_analysis(pitcher.throws, "L", [l_k_super, 1], [pitcher.stu_vl, team_breakdown.get_cabi()]) * l_starting["super"][1] / tot_count

    strikeouts_vl_s_low = so_analysis(pitcher.throws, "S", [s_k_low, 1], [switch_stat, team_breakdown.get_cabi()]) * s_starting["low"][1] / tot_count
    strikeouts_vl_s_high = so_analysis(pitcher.throws, "S", [s_k_high, 1], [switch_stat, team_breakdown.get_cabi()]) * s_starting["high"][1] / tot_count
    strikeouts_vl_s_super = so_analysis(pitcher.throws, "S", [s_k_super, 1], [switch_stat, team_breakdown.get_cabi()]) * s_starting["super"][1] / tot_count

    return strikeouts_vl_r_low + strikeouts_vl_r_high + strikeouts_vl_r_super + strikeouts_vl_l_low + strikeouts_vl_l_high + strikeouts_vl_l_super + strikeouts_vl_s_low + strikeouts_vl_s_high + strikeouts_vl_s_super

def __get_babip_rate__(
    pitcher: CardPlayer,
    throws: str,
    team_breakdown: TeamBreakdown,
    h_analysis: Callable[[str, str, List[float], List[float]], float]
):
    r_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["R"]["bab"]
    l_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["L"]["bab"]
    s_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["S"]["bab"]

    r_h_low = r_starting["low"][0] / r_starting["low"][1] if r_starting["low"][1] > 0 else 0
    r_h_high = r_starting["high"][0] / r_starting["high"][1] if r_starting["high"][1] > 0 else 0
    r_h_super = r_starting["super"][0] / r_starting["super"][1] if r_starting["super"][1] > 0 else 0

    l_h_low = l_starting["low"][0] / l_starting["low"][1] if l_starting["low"][1] > 0 else 0
    l_h_high = l_starting["high"][0] / l_starting["high"][1] if l_starting["high"][1] > 0 else 0
    l_h_super = l_starting["super"][0] / l_starting["super"][1] if l_starting["super"][1] > 0 else 0

    s_h_low = s_starting["low"][0] / s_starting["low"][1] if s_starting["low"][1] > 0 else 0
    s_h_high = s_starting["high"][0] / s_starting["high"][1] if s_starting["high"][1] > 0 else 0
    s_h_super = s_starting["super"][0] / s_starting["super"][1] if s_starting["super"][1] > 0 else 0

    tot_count = r_starting["low"][1] + r_starting["high"][1] + r_starting["super"][1] + l_starting["low"][1] + l_starting["high"][1] + l_starting["super"][1] + s_starting["low"][1] + s_starting["high"][1] + s_starting["super"][1]

    hits_vl_r_low = h_analysis(pitcher.throws, "R", [r_h_low, 1], [pitcher.gb_type, team_breakdown.get_cabi()]) * r_starting["low"][1] / tot_count
    hits_vl_r_high = h_analysis(pitcher.throws, "R", [r_h_high, 1], [pitcher.gb_type, team_breakdown.get_cabi()]) * r_starting["high"][1] / tot_count
    hits_vl_r_super = h_analysis(pitcher.throws, "R", [r_h_super, 1], [pitcher.gb_type, team_breakdown.get_cabi()]) * r_starting["super"][1] / tot_count

    hits_vl_l_low = h_analysis(pitcher.throws, "L", [l_h_low, 1], [pitcher.gb_type, team_breakdown.get_cabi()]) * l_starting["low"][1] / tot_count
    hits_vl_l_high = h_analysis(pitcher.throws, "L", [l_h_high, 1], [pitcher.gb_type, team_breakdown.get_cabi()]) * l_starting["high"][1] / tot_count
    hits_vl_l_super = h_analysis(pitcher.throws, "L", [l_h_super, 1], [pitcher.gb_type, team_breakdown.get_cabi()]) * l_starting["super"][1] / tot_count

    hits_vl_s_low = h_analysis(pitcher.throws, "S", [s_h_low, 1], [pitcher.gb_type, team_breakdown.get_cabi()]) * s_starting["low"][1] / tot_count
    hits_vl_s_high = h_analysis(pitcher.throws, "S", [s_h_high, 1], [pitcher.gb_type, team_breakdown.get_cabi()]) * s_starting["high"][1] / tot_count
    hits_vl_s_super = h_analysis(pitcher.throws, "S", [s_h_super, 1], [pitcher.gb_type, team_breakdown.get_cabi()]) * s_starting["super"][1] / tot_count

    return hits_vl_r_low + hits_vl_r_high + hits_vl_r_super + hits_vl_l_low + hits_vl_l_high + hits_vl_l_super + hits_vl_s_low + hits_vl_s_high + hits_vl_s_super

def __get_xbh_rate__(
    pitcher: CardPlayer,
    throws: str,
    team_breakdown: TeamBreakdown,
    xbh_analysis: Callable[[str, str, List[float], List[float]], float]
):
    r_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["R"]["bab"]
    l_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["L"]["bab"]
    s_starting = team_breakdown.bat_stat_nums[throws][pitcher.throws]["S"]["bab"]

    r_xbh_low = r_starting["low"][0] / r_starting["low"][1] if r_starting["low"][1] > 0 else 0
    r_xbh_high = r_starting["high"][0] / r_starting["high"][1] if r_starting["high"][1] > 0 else 0
    r_xbh_super = r_starting["super"][0] / r_starting["super"][1] if r_starting["super"][1] > 0 else 0

    l_xbh_low = l_starting["low"][0] / l_starting["low"][1] if l_starting["low"][1] > 0 else 0
    l_xbh_high = l_starting["high"][0] / l_starting["high"][1] if l_starting["high"][1] > 0 else 0
    l_xbh_super = l_starting["super"][0] / l_starting["super"][1] if l_starting["super"][1] > 0 else 0

    s_xbh_low = s_starting["low"][0] / s_starting["low"][1] if s_starting["low"][1] > 0 else 0
    s_xbh_high = s_starting["high"][0] / s_starting["high"][1] if s_starting["high"][1] > 0 else 0
    s_xbh_super = s_starting["super"][0] / s_starting["super"][1] if s_starting["super"][1] > 0 else 0

    tot_count = r_starting["low"][1] + r_starting["high"][1] + r_starting["super"][1] + l_starting["low"][1] + l_starting["high"][1] + l_starting["super"][1] + s_starting["low"][1] + s_starting["high"][1] + s_starting["super"][1]

    xbh_vl_r_low = xbh_analysis(pitcher.throws, "R", [r_xbh_low], [0]) * r_starting["low"][1] / tot_count
    xbh_vl_r_high = xbh_analysis(pitcher.throws, "R", [r_xbh_high], [0]) * r_starting["high"][1] / tot_count
    xbh_vl_r_super = xbh_analysis(pitcher.throws, "R", [r_xbh_super], [0]) * r_starting["super"][1] / tot_count

    xbh_vl_l_low = xbh_analysis(pitcher.throws, "L", [l_xbh_low], [0]) * l_starting["low"][1] / tot_count
    xbh_vl_l_high = xbh_analysis(pitcher.throws, "L", [l_xbh_high], [0]) * l_starting["high"][1] / tot_count
    xbh_vl_l_super = xbh_analysis(pitcher.throws, "L", [l_xbh_super], [0]) * l_starting["super"][1] / tot_count

    xbh_vl_s_low = xbh_analysis(pitcher.throws, "S", [s_xbh_low], [0]) * s_starting["low"][1] / tot_count
    xbh_vl_s_high = xbh_analysis(pitcher.throws, "S", [s_xbh_high], [0]) * s_starting["high"][1] / tot_count
    xbh_vl_s_super = xbh_analysis(pitcher.throws, "S", [s_xbh_super], [0]) * s_starting["super"][1] / tot_count

    return xbh_vl_r_low + xbh_vl_r_high + xbh_vl_r_super + xbh_vl_l_low + xbh_vl_l_high + xbh_vl_l_super + xbh_vl_s_low + xbh_vl_s_high + xbh_vl_s_super

@dataclass
class ProjectedStarter:
    card_player: CardPlayer = None
    bf: float = 0.0
    k_per_9: float = 0.0
    bb_per_9: float = 0.0
    hr_per_9: float = 0.0
    ip_per_g: float = 0.0
    fip: float = 0.0
    war: float = 0.0
    war_with_relief: float = 0.0

@dataclass
class ProjectedReliever:
    card_player: CardPlayer = None
    bf: float = 0.0
    k_per_9_vl: float = 0.0
    k_per_9_vr: float = 0.0
    bb_per_9_vl: float = 0.0
    bb_per_9_vr: float = 0.0
    hr_per_9_vl: float = 0.0
    hr_per_9_vr: float = 0.0
    ip_per_g_vl: float = 0.0
    ip_per_g_vr: float = 0.0
    fip_vl: float = 0.0
    fip_vr: float = 0.0
    war_vl: float = 0.0
    war_vr: float = 0.0
    war_ovr: float = 0.0

era_3_5 = (3.5 / 9.0)
era_5_5 = (5.5 / 9.0)
era_8_5 = (8.5 / 9.0)
era_12_0 = (12.0 / 9.0)

def __get_other_pitchers_run_per_g__(ip_per_game_left):
    if ip_per_game_left < 1:
        return ip_per_game_left / 1.0 * era_3_5

    if ip_per_game_left < 2:
        return (ip_per_game_left - 1) / 1.0 * era_3_5 + era_3_5

    if ip_per_game_left < 4:
        return (ip_per_game_left - 2) * era_8_5 + era_3_5 + era_5_5

    return (ip_per_game_left - 4) * era_12_0 + era_3_5 + era_5_5 + era_8_5 * 2

def __project_starter__(
    pitcher: CardPlayer,
    lwm: LinearWeightsFormulas,
    team_breakdown: TeamBreakdown,
    pitcher_stats: PitcherStats,
    pitching_formulas: PitchingPlayerFormulas,
    hr_analysis: Callable[[str, str, List[float], List[float]], float],
    bb_analysis: Callable[[str, str, List[float], List[float]], float],
    so_analysis: Callable[[str, str, List[float], List[float]], float],
    h_analysis: Callable[[str, str, List[float], List[float]], float],
    xbh_analysis: Callable[[str, str, List[float], List[float]], float],
    triple_analysis: Callable[[float], float]
) -> ProjectedStarter:
    games_played = 30
    bf = pitching_formulas.get_bf_per_game(pitcher.stamina) * games_played

    hbp = pitcher_stats.get_hbp_rate(pitcher) * bf

    homeruns = (bf - hbp) * __get_homerun_rate__(pitcher, pitcher.throws, team_breakdown, hr_analysis)
    strikeouts = (bf - hbp) * __get_strikeout_rate__(pitcher, pitcher.throws, team_breakdown, so_analysis)
    walks = (bf - hbp) * __get_walk_rate__(pitcher, pitcher.throws, team_breakdown, bb_analysis)
    hits_against = (bf - hbp) * __get_babip_rate__(pitcher, pitcher.throws, team_breakdown, h_analysis)
    xbh_against = hits_against * __get_xbh_rate__(pitcher, pitcher.throws, team_breakdown, xbh_analysis)
    triples = xbh_against * triple_analysis([team_breakdown.get_speed(pitcher.throws)])
    singles = hits_against - xbh_against
    doubles = xbh_against - triples

    sba = pitching_formulas.get_stolen_bases_attempted_per_hit(pitcher.hold) * (singles + walks + hbp)
    cs = pitching_formulas.get_caught_stealing_per_steal(pitcher.hold) * sba
    successful_steals = sba - cs

    woba = lwm.woba_mult_by_pa_from_hits(walks, hbp, singles, doubles, triples, homeruns) / bf
    wraa = lwm.woba_to_wraa_per_pa(woba) * bf

    wsb = lwm.wsb_from_steal_stats(successful_steals, cs, singles, walks, hbp)

    gidp = pitching_formulas.get_gidp_per_bip(pitcher.gb_type) * (bf - homeruns - strikeouts - walks - hbp)
    gidp_val = gidp * lwm.run_value_bases_out

    ip = (bf - homeruns - singles - doubles - triples - walks - hbp + cs + gidp) / 3.0

    war = ((wraa + wsb) * -1 + gidp_val) / lwm.runs_per_win
    others_war = __get_other_pitchers_run_per_g__(9.0 - ip / games_played) * games_played / lwm.runs_per_win

    return ProjectedStarter(
        card_player=pitcher,
        bf=bf,
        k_per_9=strikeouts / ip * 9,
        bb_per_9=(walks + hbp) / ip * 9,
        hr_per_9=homeruns / ip * 9,
        ip_per_g=ip / games_played,
        fip=(13 * homeruns + 3 * (walks + hbp) - 2 * strikeouts) / ip + 3.1,
        war=war,
        war_with_relief=war - others_war
    )

def __project_reliever__(
    pitcher: CardPlayer,
    lwm: LinearWeightsFormulas,
    team_breakdown: TeamBreakdown,
    pitcher_stats: PitcherStats,
    pitching_formulas: PitchingPlayerFormulas,
    hr_analysis: Callable[[str, str, List[float], List[float]], float],
    bb_analysis: Callable[[str, str, List[float], List[float]], float],
    so_analysis: Callable[[str, str, List[float], List[float]], float],
    h_analysis: Callable[[str, str, List[float], List[float]], float],
    xbh_analysis: Callable[[str, str, List[float], List[float]], float],
    triple_analysis: Callable[[float], float]
) -> ProjectedReliever:
    games_played = 30
    bf = pitching_formulas.get_bf_per_game(pitcher.stamina) * games_played

    hbp = pitcher_stats.get_hbp_rate(pitcher) * bf

    homeruns_vl = (bf - hbp) * __get_homerun_rate__(pitcher, "L", team_breakdown, hr_analysis)
    homeruns_vr = (bf - hbp) * __get_homerun_rate__(pitcher, "R", team_breakdown, hr_analysis)
    strikeouts_vl = (bf - hbp) * __get_strikeout_rate__(pitcher, "L", team_breakdown, so_analysis)
    strikeouts_vr = (bf - hbp) * __get_strikeout_rate__(pitcher, "R", team_breakdown, so_analysis)
    walks_vl = (bf - hbp) * __get_walk_rate__(pitcher, "L", team_breakdown, bb_analysis)
    walks_vr = (bf - hbp) * __get_walk_rate__(pitcher, "R", team_breakdown, bb_analysis)
    hits_against_vl = (bf - hbp) * __get_babip_rate__(pitcher, "L", team_breakdown, h_analysis)
    hits_against_vr = (bf - hbp) * __get_babip_rate__(pitcher, "R", team_breakdown, h_analysis)
    xbh_against_vl = hits_against_vl * __get_xbh_rate__(pitcher, "L", team_breakdown, xbh_analysis)
    xbh_against_vr = hits_against_vr * __get_xbh_rate__(pitcher, "R", team_breakdown, xbh_analysis)
    triples_vl = xbh_against_vl * triple_analysis([team_breakdown.get_speed(pitcher.throws)])
    triples_vr = xbh_against_vr * triple_analysis([team_breakdown.get_speed(pitcher.throws)])
    singles_vl = hits_against_vl - xbh_against_vl
    singles_vr = hits_against_vr - xbh_against_vr
    doubles_vl = xbh_against_vl - triples_vl
    doubles_vr = xbh_against_vr - triples_vr

    sba_vl = pitching_formulas.get_stolen_bases_attempted_per_hit(pitcher.hold) * (singles_vl + walks_vl + hbp)
    sba_vr = pitching_formulas.get_stolen_bases_attempted_per_hit(pitcher.hold) * (singles_vr + walks_vr + hbp)
    cs_vl = pitching_formulas.get_caught_stealing_per_steal(pitcher.hold) * sba_vl
    cs_vr = pitching_formulas.get_caught_stealing_per_steal(pitcher.hold) * sba_vr
    successful_steals_vl = sba_vl - cs_vl
    successful_steals_vr = sba_vr - cs_vr

    woba_vl = lwm.woba_mult_by_pa_from_hits(walks_vl, hbp, singles_vl, doubles_vl, triples_vl, homeruns_vl) / bf
    woba_vr = lwm.woba_mult_by_pa_from_hits(walks_vr, hbp, singles_vr, doubles_vr, triples_vr, homeruns_vr) / bf
    wraa_vl = lwm.woba_to_wraa_per_pa(woba_vl) * bf
    wraa_vr = lwm.woba_to_wraa_per_pa(woba_vr) * bf

    wsb_vl = lwm.wsb_from_steal_stats(successful_steals_vl, cs_vl, singles_vl, walks_vl, hbp)
    wsb_vr = lwm.wsb_from_steal_stats(successful_steals_vr, cs_vr, singles_vr, walks_vr, hbp)

    gidp_vl = pitching_formulas.get_gidp_per_bip(pitcher.gb_type) * (bf - homeruns_vl - strikeouts_vl - walks_vl - hbp)
    gidp_vr = pitching_formulas.get_gidp_per_bip(pitcher.gb_type) * (bf - homeruns_vr - strikeouts_vr - walks_vr - hbp)
    gidp_val_vl = gidp_vl * lwm.run_value_bases_out
    gidp_val_vr = gidp_vr * lwm.run_value_bases_out

    ip_vl = (bf - homeruns_vl - singles_vl - doubles_vl - triples_vl - walks_vl - hbp + cs_vl + gidp_vl) / 3.0
    ip_vr = (bf - homeruns_vr - singles_vr - doubles_vr - triples_vr - walks_vr - hbp + cs_vr + gidp_vr) / 3.0

    war_vl = ((wraa_vl + wsb_vl) * -1 + gidp_val_vl) / lwm.runs_per_win
    war_vr = ((wraa_vr + wsb_vr) * -1 + gidp_val_vr) / lwm.runs_per_win

    return ProjectedReliever(
        card_player=pitcher,
        bf=bf,
        k_per_9_vl=strikeouts_vl / ip_vl * 9,
        k_per_9_vr=strikeouts_vr / ip_vr * 9,
        bb_per_9_vl=(walks_vl + hbp) / ip_vl * 9,
        bb_per_9_vr=(walks_vr + hbp) / ip_vr * 9,
        hr_per_9_vl=homeruns_vl / ip_vl * 9,
        hr_per_9_vr=homeruns_vr / ip_vr * 9,
        ip_per_g_vl=ip_vl / games_played,
        ip_per_g_vr=ip_vr / games_played,
        fip_vl=(13 * homeruns_vl + 3 * (walks_vl + hbp) - 2 * strikeouts_vl) / ip_vl + 3.1,
        fip_vr=(13 * homeruns_vr + 3 * (walks_vr + hbp) - 2 * strikeouts_vr) / ip_vr + 3.1,
        war_vl=war_vl,
        war_vr=war_vr,
        war_ovr=(team_breakdown.vl_starts * war_vl + team_breakdown.vr_starts * war_vr) / (team_breakdown.vl_starts + team_breakdown.vr_starts)
    )

def project_starters(
    pitchers: List[CardPlayer],
    lwm: LinearWeightsFormulas,
    team_breakdown: TeamBreakdown,
    pitcher_stats: PitcherStats,
    pitching_formulas: PitchingPlayerFormulas,
    hr_analysis: Callable[[str, str, List[float], List[float]], float],
    bb_analysis: Callable[[str, str, List[float], List[float]], float],
    so_analysis: Callable[[str, str, List[float], List[float]], float],
    h_analysis: Callable[[str, str, List[float], List[float]], float],
    xbh_analysis: Callable[[str, str, List[float], List[float]], float],
    triple_analysis: Callable[[float], float]
) -> List[ProjectedStarter]:
    starters: List[ProjectedStarter] = []

    for pitcher in pitchers:
        starters.append(__project_starter__(
            pitcher=pitcher,
            lwm=lwm,
            team_breakdown=team_breakdown,
            pitcher_stats=pitcher_stats,
            pitching_formulas=pitching_formulas,
            hr_analysis=hr_analysis,
            bb_analysis=bb_analysis,
            so_analysis=so_analysis,
            h_analysis=h_analysis,
            xbh_analysis=xbh_analysis,
            triple_analysis=triple_analysis
        ))

    return starters

def project_relievers(
    pitchers: List[CardPlayer],
    lwm: LinearWeightsFormulas,
    team_breakdown: TeamBreakdown,
    pitcher_stats: PitcherStats,
    pitching_formulas: PitchingPlayerFormulas,
    hr_analysis: Callable[[str, str, List[float], List[float]], float],
    bb_analysis: Callable[[str, str, List[float], List[float]], float],
    so_analysis: Callable[[str, str, List[float], List[float]], float],
    h_analysis: Callable[[str, str, List[float], List[float]], float],
    xbh_analysis: Callable[[str, str, List[float], List[float]], float],
    triple_analysis: Callable[[float], float]
) -> List[ProjectedReliever]:
    relievers: List[ProjectedReliever] = []

    for pitcher in pitchers:
        relievers.append(__project_reliever__(
            pitcher=pitcher,
            lwm=lwm,
            team_breakdown=team_breakdown,
            pitcher_stats=pitcher_stats,
            pitching_formulas=pitching_formulas,
            hr_analysis=hr_analysis,
            bb_analysis=bb_analysis,
            so_analysis=so_analysis,
            h_analysis=h_analysis,
            xbh_analysis=xbh_analysis,
            triple_analysis=triple_analysis
        ))

    return relievers