from dataclasses import dataclass
from typing import Dict, List

from headers.util import safe_float, safe_int, search_with_reasonable_error


@dataclass
class StatsBatter:
    batter_games: int = 0
    batter_games_started: int = 0
    batter_pa: int = 0
    batter_ab: int = 0
    batter_runs_scored: int = 0
    batter_hits: int = 0
    batter_singles: int = 0
    batter_doubles: int = 0
    batter_triples: int = 0
    batter_homeruns: int = 0
    batter_walks: int = 0
    batter_intentional_walks: int = 0
    batter_hit_by_pitch: int = 0
    batter_sac_hits: int = 0
    batter_sac_flies: int = 0
    batter_strikeouts: int = 0
    batter_gidp: int = 0
    batter_woba: float = 0
    batter_babip: float = 0
    batter_wrc: float = 0
    batter_wraa: float = 0
    batter_stolen_bases: int = 0
    batter_caught_stealing: int = 0
    batter_batting_runs: float = 0.0
    batter_weighted_stolen_bases: float = 0.0
    batter_ubr: float = 0.0
    batter_base_running_runs: float = 0.0
    batter_war: float = 0.0

def get_batter_header_indices(headers: List[str]) -> Dict[str, int]:
    header_indices = {}

    header_indices["cid_index"] = search_with_reasonable_error(headers, "CID")
    header_indices["pos_index"] = search_with_reasonable_error(headers, "POS")
    header_indices["bat_games_index"] = search_with_reasonable_error(headers, "G")
    header_indices["bat_games_start_index"] = search_with_reasonable_error(headers, "GS")
    header_indices["bat_pa_index"] = search_with_reasonable_error(headers, "PA")
    header_indices["bat_ab_index"] = search_with_reasonable_error(headers, "AB")
    header_indices["bat_runs_scored_index"] = search_with_reasonable_error(headers, "R")
    header_indices["bat_h_index"] = search_with_reasonable_error(headers, "H")
    header_indices["bat_singles_index"] = search_with_reasonable_error(headers, "1B")
    header_indices["bat_doubles_index"] = search_with_reasonable_error(headers, "2B")
    header_indices["bat_triples_index"] = search_with_reasonable_error(headers, "3B")
    header_indices["bat_homeruns_index"] = search_with_reasonable_error(headers, "HR")
    header_indices["bat_walks_index"] = search_with_reasonable_error(headers, "BB")
    header_indices["bat_intentional_walks_index"] = search_with_reasonable_error(headers, "IBB")
    header_indices["bat_hbp_index"] = search_with_reasonable_error(headers, "HP")
    header_indices["bat_sh_index"] = search_with_reasonable_error(headers, "SH")
    header_indices["bat_sf_index"] = search_with_reasonable_error(headers, "SF")
    header_indices["bat_so_index"] = search_with_reasonable_error(headers, "SO")
    header_indices["bat_gidp_index"] = search_with_reasonable_error(headers, "GIDP")
    header_indices["bat_woba_index"] = search_with_reasonable_error(headers, "wOBA")
    header_indices["bat_babip_index"] = search_with_reasonable_error(headers, "BABIP")
    header_indices["bat_wrc_index"] = search_with_reasonable_error(headers, "wRC")
    header_indices["bat_wraa_index"] = search_with_reasonable_error(headers, "wRAA")
    header_indices["bat_sb_index"] = search_with_reasonable_error(headers, "SB")
    header_indices["bat_cs_index"] = search_with_reasonable_error(headers, "CS")
    header_indices["bat_batr_index"] = search_with_reasonable_error(headers, "BatR")
    header_indices["bat_wsb_index"] = search_with_reasonable_error(headers, "wSB")
    header_indices["bat_ubr_index"] = search_with_reasonable_error(headers, "UBR")
    header_indices["bat_bsr_index"] = search_with_reasonable_error(headers, "BsR")
    header_indices["bat_war_index"] = search_with_reasonable_error(headers, "WAR")

    return header_indices

def new_stats_batter(header_indices: Dict[str, int], play_line: List[str]) -> StatsBatter:
    return StatsBatter(
        batter_games=safe_int(play_line[header_indices["bat_games_index"]]),
        batter_games_started=safe_int(play_line[header_indices["bat_games_start_index"]]),
        batter_pa=safe_int(play_line[header_indices["bat_pa_index"]]),
        batter_ab=safe_int(play_line[header_indices["bat_ab_index"]]),
        batter_runs_scored=safe_int(play_line[header_indices["bat_runs_scored_index"]]),
        batter_hits=safe_int(play_line[header_indices["bat_h_index"]]),
        batter_singles=safe_int(play_line[header_indices["bat_singles_index"]]),
        batter_doubles=safe_int(play_line[header_indices["bat_doubles_index"]]),
        batter_triples=safe_int(play_line[header_indices["bat_triples_index"]]),
        batter_homeruns=safe_int(play_line[header_indices["bat_homeruns_index"]]),
        batter_walks=safe_int(play_line[header_indices["bat_walks_index"]]),
        batter_intentional_walks=safe_int(play_line[header_indices["bat_intentional_walks_index"]]),
        batter_hit_by_pitch=safe_int(play_line[header_indices["bat_hbp_index"]]),
        batter_sac_hits=safe_int(play_line[header_indices["bat_sh_index"]]),
        batter_sac_flies=safe_int(play_line[header_indices["bat_sf_index"]]),
        batter_strikeouts=safe_int(play_line[header_indices["bat_so_index"]]),
        batter_gidp=safe_int(play_line[header_indices["bat_gidp_index"]]),
        batter_woba=safe_float(play_line[header_indices["bat_woba_index"]]),
        batter_babip=safe_float(play_line[header_indices["bat_babip_index"]]),
        batter_wrc=safe_float(play_line[header_indices["bat_wrc_index"]]),
        batter_wraa=safe_float(play_line[header_indices["bat_wraa_index"]]),
        batter_stolen_bases=safe_int(play_line[header_indices["bat_sb_index"]]),
        batter_caught_stealing=safe_int(play_line[header_indices["bat_cs_index"]]),
        batter_batting_runs=safe_float(play_line[header_indices["bat_batr_index"]]),
        batter_weighted_stolen_bases=safe_float(play_line[header_indices["bat_wsb_index"]]),
        batter_ubr=safe_float(play_line[header_indices["bat_ubr_index"]]),
        batter_base_running_runs=safe_float(play_line[header_indices["bat_bsr_index"]]),
        batter_war=safe_float(play_line[header_indices["bat_war_index"]]),
    )

def __weighted_avg__(a_stat, a_weight, b_stat, b_weight):
    return (a_stat * a_weight + b_stat * b_weight) / (a_weight + b_weight) if (a_weight + b_weight) > 0 else 0

def merge_stats_batter(a: StatsBatter, b: StatsBatter) -> StatsBatter:
    if a != None and b == None:
        return a
    elif a == None and b != None:
        return b
    elif a == None and b == None:
        return None
    c = StatsBatter()

    c.batter_games = a.batter_games + b.batter_games
    c.batter_games_started = a.batter_games_started + b.batter_games_started
    c.batter_pa = a.batter_pa + b.batter_pa
    c.batter_ab = a.batter_ab + b.batter_ab
    c.batter_hits = a.batter_hits + b.batter_hits
    c.batter_singles = a.batter_singles + b.batter_singles
    c.batter_doubles = a.batter_doubles + b.batter_doubles
    c.batter_triples = a.batter_triples + b.batter_triples
    c.batter_homeruns = a.batter_homeruns + b.batter_homeruns
    c.batter_walks = a.batter_walks + b.batter_walks
    c.batter_intentional_walks = a.batter_intentional_walks + b.batter_intentional_walks
    c.batter_hit_by_pitch = a.batter_hit_by_pitch + b.batter_hit_by_pitch
    c.batter_sac_hits = a.batter_sac_hits + b.batter_sac_hits
    c.batter_sac_flies = a.batter_sac_flies + b.batter_sac_flies
    c.batter_strikeouts = a.batter_strikeouts + b.batter_strikeouts
    c.batter_gidp = a.batter_gidp + b.batter_gidp
    c.batter_sac_hits = a.batter_sac_hits + b.batter_sac_hits
    c.batter_woba = __weighted_avg__(a.batter_woba, a.batter_pa, b.batter_woba, b.batter_pa)
    c.batter_babip = __weighted_avg__(a.batter_babip, a.batter_pa, b.batter_babip, b.batter_pa)
    c.batter_wrc = a.batter_wrc + b.batter_wrc
    c.batter_wraa = a.batter_wraa + b.batter_wraa
    c.batter_stolen_bases = a.batter_stolen_bases + b.batter_stolen_bases
    c.batter_caught_stealing = a.batter_caught_stealing + b.batter_caught_stealing
    c.batter_batting_runs = a.batter_batting_runs + b.batter_batting_runs
    c.batter_weighted_stolen_bases = a.batter_weighted_stolen_bases + b.batter_weighted_stolen_bases
    c.batter_ubr = a.batter_ubr + b.batter_ubr
    c.batter_base_running_runs = a.batter_base_running_runs + b.batter_base_running_runs
    c.batter_war = a.batter_war + b.batter_war

    return c