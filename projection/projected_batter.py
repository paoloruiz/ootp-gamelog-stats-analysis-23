from dataclasses import dataclass
from typing import Callable, List
from analysis.stolen_bases import StolenBasesFormulas
from cards.card_player import CardPlayer
from analysis.find_top_team_players import TeamBreakdown
from individual_league.determine_linear_weights import LinearWeightsFormulas
from individual_league.league_stats import LeagueStats

@dataclass
class ProjectedBatter:
    card_player: CardPlayer
    position: int
    walks_vl: float
    walks_vr: float
    strikeouts_vl: float
    strikeouts_vr: float
    homeruns_vl: float
    homeruns_vr: float
    singles_vl: float
    singles_vr: float
    doubles_vl: float
    doubles_vr: float
    triples_vl: float
    triples_vr: float
    sba_vl: float
    sba_vr: float
    steals_vl: float
    steals_vr: float
    ubr_vl: float
    ubr_vr: float
    wsb_vl: float
    wsb_vr: float
    fielding_runs: float
    woba_vl: float
    woba_vr: float
    wraa_vl: float
    wraa_vr: float
    war_vl: float
    war_vr: float
    war_ovr: float

def __get_walk_rate__(
    batter: CardPlayer,
    throws: str,
    team_breakdown: TeamBreakdown,
    bb_analysis: Callable[[str, str, List[float], List[float]], float]
):
    r_starting = team_breakdown.pitch_stat_nums[throws]["R"][batter.bats]["ctl"]
    l_starting = team_breakdown.pitch_stat_nums[throws]["L"][batter.bats]["ctl"]

    r_bb_low = r_starting["low"][0] / r_starting["low"][1] if r_starting["low"][1] > 0 else 0
    r_bb_high = r_starting["high"][0] / r_starting["high"][1] if r_starting["high"][1] > 0 else 0
    r_bb_super = r_starting["super"][0] / r_starting["super"][1] if r_starting["super"][1] > 0 else 0

    l_bb_low = l_starting["low"][0] / l_starting["low"][1] if l_starting["low"][1] > 0 else 0
    l_bb_high = l_starting["high"][0] / l_starting["high"][1] if l_starting["high"][1] > 0 else 0
    l_bb_super = l_starting["super"][0] / l_starting["super"][1] if l_starting["super"][1] > 0 else 0

    tot_count = r_starting["low"][1] + r_starting["high"][1] + r_starting["super"][1] + l_starting["low"][1] + l_starting["high"][1] + l_starting["super"][1]

    stat = batter.eye_vl if throws == "L" else batter.eye_vr
    walks_vl_r_low = bb_analysis(throws, batter.bats, [stat, 1], [r_bb_low, team_breakdown.get_cabi()]) * r_starting["low"][1] / tot_count
    walks_vl_r_high = bb_analysis(throws, batter.bats, [stat, 1], [r_bb_high, team_breakdown.get_cabi()]) * r_starting["high"][1] / tot_count
    walks_vl_r_super = bb_analysis(throws, batter.bats, [stat, 1], [r_bb_super, team_breakdown.get_cabi()]) * r_starting["super"][1] / tot_count

    walks_vl_l_low = bb_analysis(throws, batter.bats, [stat, 1], [l_bb_low, team_breakdown.get_cabi()]) * l_starting["low"][1] / tot_count
    walks_vl_l_high = bb_analysis(throws, batter.bats, [stat, 1], [l_bb_high, team_breakdown.get_cabi()]) * l_starting["high"][1] / tot_count
    walks_vl_l_super = bb_analysis(throws, batter.bats, [stat, 1], [l_bb_super, team_breakdown.get_cabi()]) * l_starting["super"][1] / tot_count

    return walks_vl_r_low + walks_vl_r_high + walks_vl_r_super + walks_vl_l_low + walks_vl_l_high + walks_vl_l_super

def __get_homerun_rate__(
    batter: CardPlayer,
    throws: str,
    team_breakdown: TeamBreakdown,
    hr_analysis: Callable[[str, str, List[float], List[float]], float]
):
    r_starting = team_breakdown.pitch_stat_nums[throws]["R"][batter.bats]["mov"]
    l_starting = team_breakdown.pitch_stat_nums[throws]["L"][batter.bats]["mov"]

    r_hr_low = r_starting["low"][0] / r_starting["low"][1] if r_starting["low"][1] > 0 else 0
    r_hr_high = r_starting["high"][0] / r_starting["high"][1] if r_starting["high"][1] > 0 else 0
    r_hr_super = r_starting["super"][0] / r_starting["super"][1] if r_starting["super"][1] > 0 else 0

    l_hr_low = l_starting["low"][0] / l_starting["low"][1] if l_starting["low"][1] > 0 else 0
    l_hr_high = l_starting["high"][0] / l_starting["high"][1] if l_starting["high"][1] > 0 else 0
    l_hr_super = l_starting["super"][0] / l_starting["super"][1] if l_starting["super"][1] > 0 else 0

    tot_count = r_starting["low"][1] + r_starting["high"][1] + r_starting["super"][1] + l_starting["low"][1] + l_starting["high"][1] + l_starting["super"][1]

    stat = batter.pow_vl if throws == "L" else batter.pow_vr
    homeruns_vl_r_low = hr_analysis(throws, batter.bats, [stat, 1], [r_hr_low, team_breakdown.get_cabi()]) * r_starting["low"][1] / tot_count
    homeruns_vl_r_high = hr_analysis(throws, batter.bats, [stat, 1], [r_hr_high, team_breakdown.get_cabi()]) * r_starting["high"][1] / tot_count
    homeruns_vl_r_super = hr_analysis(throws, batter.bats, [stat, 1], [r_hr_super, team_breakdown.get_cabi()]) * r_starting["super"][1] / tot_count

    homeruns_vl_l_low = hr_analysis(throws, batter.bats, [stat, 1], [l_hr_low, team_breakdown.get_cabi()]) * l_starting["low"][1] / tot_count
    homeruns_vl_l_high = hr_analysis(throws, batter.bats, [stat, 1], [l_hr_high, team_breakdown.get_cabi()]) * l_starting["high"][1] / tot_count
    homeruns_vl_l_super = hr_analysis(throws, batter.bats, [stat, 1], [l_hr_super, team_breakdown.get_cabi()]) * l_starting["super"][1] / tot_count

    return homeruns_vl_r_low + homeruns_vl_r_high + homeruns_vl_r_super + homeruns_vl_l_low + homeruns_vl_l_high + homeruns_vl_l_super

def __get_strikeout_rate__(
    batter: CardPlayer,
    throws: str,
    team_breakdown: TeamBreakdown,
    so_analysis: Callable[[str, str, List[float], List[float]], float]
):
    r_starting = team_breakdown.pitch_stat_nums[throws]["R"][batter.bats]["stu"]
    l_starting = team_breakdown.pitch_stat_nums[throws]["L"][batter.bats]["stu"]

    r_so_low = r_starting["low"][0] / r_starting["low"][1] if r_starting["low"][1] > 0 else 0
    r_so_high = r_starting["high"][0] / r_starting["high"][1] if r_starting["high"][1] > 0 else 0
    r_so_super = r_starting["super"][0] / r_starting["super"][1] if r_starting["super"][1] > 0 else 0

    l_so_low = l_starting["low"][0] / l_starting["low"][1] if l_starting["low"][1] > 0 else 0
    l_so_high = l_starting["high"][0] / l_starting["high"][1] if l_starting["high"][1] > 0 else 0
    l_so_super = l_starting["super"][0] / l_starting["super"][1] if l_starting["super"][1] > 0 else 0

    tot_count = r_starting["low"][1] + r_starting["high"][1] + r_starting["super"][1] + l_starting["low"][1] + l_starting["high"][1] + l_starting["super"][1]

    stat = batter.avk_vl if throws == "L" else batter.avk_vr
    strikeouts_vl_r_low = so_analysis(throws, batter.bats, [stat, 1], [r_so_low, team_breakdown.get_cabi()]) * r_starting["low"][1] / tot_count
    strikeouts_vl_r_high = so_analysis(throws, batter.bats, [stat, 1], [r_so_high, team_breakdown.get_cabi()]) * r_starting["high"][1] / tot_count
    strikeouts_vl_r_super = so_analysis(throws, batter.bats, [stat, 1], [r_so_super, team_breakdown.get_cabi()]) * r_starting["super"][1] / tot_count

    strikeouts_vl_l_low = so_analysis(throws, batter.bats, [stat, 1], [l_so_low, team_breakdown.get_cabi()]) * l_starting["low"][1] / tot_count
    strikeouts_vl_l_high = so_analysis(throws, batter.bats, [stat, 1], [l_so_high, team_breakdown.get_cabi()]) * l_starting["high"][1] / tot_count
    strikeouts_vl_l_super = so_analysis(throws, batter.bats, [stat, 1], [l_so_super, team_breakdown.get_cabi()]) * l_starting["super"][1] / tot_count

    return strikeouts_vl_r_low + strikeouts_vl_r_high + strikeouts_vl_r_super + strikeouts_vl_l_low + strikeouts_vl_l_high + strikeouts_vl_l_super


def __project_batter__(
    batter: CardPlayer,
    team_breakdown: TeamBreakdown,
    lwm: LinearWeightsFormulas,
    position: int,
    league_stats: LeagueStats,
    hr_analysis: Callable[[str, str, List[float], List[float]], float],
    bb_analysis: Callable[[str, str, List[float], List[float]], float],
    so_analysis: Callable[[str, str, List[float], List[float]], float],
    h_analysis: Callable[[str, str, List[float], List[float]], float],
    xbh_analysis: Callable[[str, str, List[float], List[float]], float],
    def_analysis: Callable[[CardPlayer, int], float],
    triple_analysis: Callable[[float], float],
    stolen_base_formulas: StolenBasesFormulas
) -> ProjectedBatter:
    pa = 720
    gs = 162

    walks_vl = pa * __get_walk_rate__(batter, "L", team_breakdown, bb_analysis)
    walks_vr = pa * __get_walk_rate__(batter, "R", team_breakdown, bb_analysis)

    homeruns_vl = pa * __get_homerun_rate__(batter, "L", team_breakdown, hr_analysis)
    homeruns_vr = pa * __get_homerun_rate__(batter, "R", team_breakdown, hr_analysis)

    strikeouts_vl = pa * __get_strikeout_rate__(batter, "L", team_breakdown, so_analysis)
    strikeouts_vr = pa * __get_strikeout_rate__(batter, "R", team_breakdown, so_analysis)

    l_starting_vl_pct = team_breakdown.pitch_nums["L"]["L"] / (team_breakdown.pitch_nums["L"]["L"] + team_breakdown.pitch_nums["L"]["R"])
    r_starting_vl_pct = team_breakdown.pitch_nums["R"]["L"] / (team_breakdown.pitch_nums["R"]["L"] + team_breakdown.pitch_nums["R"]["R"])

    hits_vl = pa * (min(0.28, h_analysis("L", batter.bats, [batter.babip_vl, 1], [2, team_breakdown.get_cabi()])) * l_starting_vl_pct + 
        min(0.28, (h_analysis("R", batter.bats, [batter.babip_vr, 1], [2, team_breakdown.get_cabi()]))) * (1 - l_starting_vl_pct))
    hits_vr = pa * (min(0.28, h_analysis("L", batter.bats, [batter.babip_vl, 1], [2, team_breakdown.get_cabi()])) * r_starting_vl_pct + 
        min(0.28, h_analysis("R", batter.bats, [batter.babip_vr, 1], [2, team_breakdown.get_cabi()])) * (1 - r_starting_vl_pct))

    xbh_vl = hits_vl * (xbh_analysis("L", batter.bats, [batter.gap_vl], [0]) * l_starting_vl_pct + xbh_analysis("R", batter.bats, [batter.gap_vr], [0]) * (1 - l_starting_vl_pct))
    xbh_vr = hits_vr * (xbh_analysis("L", batter.bats, [batter.gap_vl], [0]) * r_starting_vl_pct + xbh_analysis("R", batter.bats, [batter.gap_vr], [0]) * (1 - r_starting_vl_pct))

    singles_vl = hits_vl - xbh_vl
    singles_vr = hits_vr - xbh_vr

    triples_vl = xbh_vl * triple_analysis([batter.speed])
    triples_vr = xbh_vr * triple_analysis([batter.speed])

    doubles_vl = xbh_vl - triples_vl
    doubles_vr = xbh_vr - triples_vr

    sba_vl = stolen_base_formulas.get_stolen_base_attempt_per_1b(batter.speed) * (singles_vl + walks_vl)
    sba_vr = stolen_base_formulas.get_stolen_base_attempt_per_1b(batter.speed) * (singles_vr + walks_vr)

    successful_steals_vl = stolen_base_formulas.get_successful_steal_rate(batter.steal) * (sba_vl)
    successful_steals_vr = stolen_base_formulas.get_successful_steal_rate(batter.steal) * (sba_vr)

    caught_stealing_vl = sba_vl - successful_steals_vl
    caught_stealing_vr = sba_vr - successful_steals_vr

    wsb_vl = lwm.wsb_from_steal_stats(successful_steals_vl, caught_stealing_vl, singles_vl, walks_vl, 2)
    wsb_vr = lwm.wsb_from_steal_stats(successful_steals_vr, caught_stealing_vr, singles_vr, walks_vr, 2)

    ubr_vl = lwm.ubr_per_chance_from_baserunning(batter.baserunning) * (singles_vl + doubles_vl + triples_vl)
    ubr_vr = lwm.ubr_per_chance_from_baserunning(batter.baserunning) * (singles_vr + doubles_vr + triples_vr)

    woba_vl = lwm.woba_mult_by_pa_from_hits(walks_vl, 2, singles_vl, doubles_vl, triples_vl, homeruns_vl) / pa
    woba_vr = lwm.woba_mult_by_pa_from_hits(walks_vr, 2, singles_vr, doubles_vr, triples_vr, homeruns_vr) / pa

    wraa_vl = lwm.woba_to_wraa_per_pa(woba_vl) * pa
    wraa_vr = lwm.woba_to_wraa_per_pa(woba_vr) * pa

    # TODO catcher framing runs
    fielding_runs = league_stats.get_runs_per_out() * def_analysis(batter, position)

    war_vl = (wraa_vl + wsb_vl + ubr_vl + fielding_runs) / lwm.runs_per_win
    war_vr = (wraa_vr + wsb_vr + ubr_vr + fielding_runs) / lwm.runs_per_win

    war_ovr = (team_breakdown.vl_starts * war_vl + team_breakdown.vr_starts * war_vr) / (team_breakdown.vl_starts + team_breakdown.vr_starts)

    return ProjectedBatter(
        card_player=batter,
        position=position,
        walks_vl=walks_vl,
        walks_vr=walks_vr,
        strikeouts_vl=strikeouts_vl,
        strikeouts_vr=strikeouts_vr,
        homeruns_vl=homeruns_vl,
        homeruns_vr=homeruns_vr,
        singles_vl=singles_vl,
        singles_vr=singles_vr,
        doubles_vl=doubles_vl,
        doubles_vr=doubles_vr,
        triples_vl=triples_vl,
        triples_vr=triples_vr,
        sba_vl=sba_vl,
        sba_vr=sba_vr,
        steals_vl=successful_steals_vl,
        steals_vr=successful_steals_vr,
        ubr_vl=ubr_vl,
        ubr_vr=ubr_vr,
        wsb_vl=wsb_vl,
        wsb_vr=wsb_vr,
        fielding_runs=fielding_runs,
        woba_vl=woba_vl,
        woba_vr=woba_vr,
        wraa_vl=wraa_vl,
        wraa_vr=wraa_vr,
        war_vl=war_vl,
        war_vr=war_vr,
        war_ovr=war_ovr
    )


def project_batters(
    batters: List[CardPlayer],
    team_breakdown: TeamBreakdown,
    lwm: LinearWeightsFormulas,
    league_stats: LeagueStats,
    hr_analysis: Callable[[str, str, List[float], List[float]], float],
    bb_analysis: Callable[[str, str, List[float], List[float]], float],
    so_analysis: Callable[[str, str, List[float], List[float]], float],
    h_analysis: Callable[[str, str, List[float], List[float]], float],
    xbh_analysis: Callable[[str, str, List[float], List[float]], float],
    def_analysis: Callable[[CardPlayer, int], float],
    triple_analysis: Callable[[float], float],
    stolen_base_formulas: StolenBasesFormulas
) -> List[ProjectedBatter]:
    projected_batters: List[ProjectedBatter] = []
    for batter in batters:
        positions = [0]
        if batter.defensec:
            positions.append(2)
        if batter.defense1b:
            positions.append(3)
        if batter.defense2b:
            positions.append(4)
        if batter.defense3b:
            positions.append(5)
        if batter.defensess:
            positions.append(6)
        if batter.defenself:
            positions.append(7)
        if batter.defensecf:
            positions.append(8)
        if batter.defenserf:
            positions.append(9)

        for position in positions:
            projected_batters.append(__project_batter__(
                batter=batter,
                team_breakdown=team_breakdown,
                lwm=lwm,
                position=position,
                league_stats=league_stats,
                hr_analysis=hr_analysis,
                bb_analysis=bb_analysis,
                so_analysis=so_analysis,
                h_analysis=h_analysis,
                xbh_analysis=xbh_analysis,
                def_analysis=def_analysis,
                triple_analysis=triple_analysis,
                stolen_base_formulas=stolen_base_formulas
            ))
    return projected_batters