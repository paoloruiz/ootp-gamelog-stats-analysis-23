from dataclasses import dataclass
from typing import Dict, List
from headers.util import safe_float, safe_int, search_with_reasonable_error

from util.ip_math import add_ip, ip_to_ip_w_remainder


@dataclass
class StatsFielder:
    fielding_position: int = 0
    fielding_games: int = 0
    fielding_games_started: int = 0
    fielding_total_chances: int = 0
    fielding_assists: int = 0
    fielding_putouts: int = 0
    fielding_errors: int = 0
    fielding_double_plays: int = 0
    fielding_triple_plays: int = 0
    fielding_pct: float = 0.0
    fielding_rng: float = 0.0
    fielding_zr: float = 0.0
    fielding_eff: float = 0.0
    fielding_stolen_bases_against: int = 0
    fielding_caught_stealing_against: int = 0
    fielding_runners_thrown_out: int = 0
    fielding_ip: float = 0.0
    fielding_passed_balls: int = 0
    fielding_catcher_earned_runs: int = 0
    fielding_reg_balls_in_zone: int = 0
    fielding_reg_balls_in_zone_fielded: int = 0
    fielding_likely_balls_in_zone: int = 0
    fielding_likely_balls_in_zone_fielded: int = 0
    fielding_even_balls_in_zone: int = 0
    fielding_even_balls_in_zone_fielded: int = 0
    fielding_unlikely_balls_in_zone: int = 0
    fielding_unlikely_balls_in_zone_fielded: int = 0
    fielding_remote_balls_in_zone: int = 0
    fielding_remote_balls_in_zone_fielded: int = 0
    fielding_impossible_balls_in_zone: int = 0
    fielding_framing_runs: float = 0.0
    fielding_arm_runs: float = 0.0

def get_fielder_header_indices(headers: List[str]) -> Dict[str, int]:
    header_indices = {}
    
    fielding_starting_index = search_with_reasonable_error(headers, "SIERA")

    header_indices["fld_g_index"] = search_with_reasonable_error(headers, "G", fielding_starting_index)
    header_indices["fld_gs_index"] = search_with_reasonable_error(headers, "GS", fielding_starting_index)
    header_indices["fld_tc_index"] = search_with_reasonable_error(headers, "TC", fielding_starting_index)
    header_indices["fld_ast_index"] = search_with_reasonable_error(headers, "A", fielding_starting_index)
    header_indices["fld_po_index"] = search_with_reasonable_error(headers, "PO", fielding_starting_index)
    header_indices["fld_err_index"] = search_with_reasonable_error(headers, "E", fielding_starting_index)
    header_indices["fld_db_index"] = search_with_reasonable_error(headers, "DP", fielding_starting_index)
    header_indices["fld_tp_index"] = search_with_reasonable_error(headers, "TP", fielding_starting_index)
    header_indices["fld_pct_index"] = search_with_reasonable_error(headers, "PCT", fielding_starting_index)
    header_indices["fld_rng_index"] = search_with_reasonable_error(headers, "RNG", fielding_starting_index)
    header_indices["fld_zr_index"] = search_with_reasonable_error(headers, "ZR", fielding_starting_index)
    header_indices["fld_eff_index"] = search_with_reasonable_error(headers, "EFF", fielding_starting_index)
    header_indices["fld_sba_index"] = search_with_reasonable_error(headers, "SBA", fielding_starting_index)
    header_indices["fld_rto_index"] = search_with_reasonable_error(headers, "RTO", fielding_starting_index)
    header_indices["fld_ip_index"] = search_with_reasonable_error(headers, "IP", fielding_starting_index)
    header_indices["fld_pb_index"] = search_with_reasonable_error(headers, "PB", fielding_starting_index)
    header_indices["fld_cer_index"] = search_with_reasonable_error(headers, "CER", fielding_starting_index)
    header_indices["fld_rbiz_index"] = search_with_reasonable_error(headers, "BIZ-R", fielding_starting_index)
    header_indices["fld_rbizm_index"] = search_with_reasonable_error(headers, "BIZ-Rm", fielding_starting_index)
    header_indices["fld_lbiz_index"] = search_with_reasonable_error(headers, "BIZ-L", fielding_starting_index)
    header_indices["fld_lbizm_index"] = search_with_reasonable_error(headers, "BIZ-Lm", fielding_starting_index)
    header_indices["fld_ebiz_index"] = search_with_reasonable_error(headers, "BIZ-E", fielding_starting_index)
    header_indices["fld_ebizm_index"] = search_with_reasonable_error(headers, "BIZ-Em", fielding_starting_index)
    header_indices["fld_ubiz_index"] = search_with_reasonable_error(headers, "BIZ-U", fielding_starting_index)
    header_indices["fld_ubizm_index"] = search_with_reasonable_error(headers, "BIZ-Um", fielding_starting_index)
    header_indices["fld_zbiz_index"] = search_with_reasonable_error(headers, "BIZ-Z", fielding_starting_index)
    header_indices["fld_zbizm_index"] = search_with_reasonable_error(headers, "BIZ-Zm", fielding_starting_index)
    header_indices["fld_ibiz_index"] = search_with_reasonable_error(headers, "BIZ-I", fielding_starting_index)
    header_indices["fld_frm_index"] = search_with_reasonable_error(headers, "FRM", fielding_starting_index)
    header_indices["fld_arm_index"] = search_with_reasonable_error(headers, "ARM", fielding_starting_index)

    return header_indices

def new_stats_fielder(header_indices: Dict[str, int], position_number: int, play_line: List[str]) -> StatsFielder:
    return StatsFielder(
        fielding_position=position_number,
        fielding_games=safe_int(play_line[header_indices["fld_g_index"]]),
        fielding_games_started=safe_int(play_line[header_indices["fld_gs_index"]]),
        fielding_total_chances=safe_int(play_line[header_indices["fld_tc_index"]]),
        fielding_assists=safe_int(play_line[header_indices["fld_ast_index"]]),
        fielding_putouts=safe_int(play_line[header_indices["fld_po_index"]]),
        fielding_errors=safe_int(play_line[header_indices["fld_err_index"]]),
        fielding_double_plays=safe_int(play_line[header_indices["fld_db_index"]]),
        fielding_triple_plays=safe_int(play_line[header_indices["fld_tp_index"]]),
        fielding_pct=safe_float(play_line[header_indices["fld_pct_index"]]),
        fielding_rng=safe_float(play_line[header_indices["fld_rng_index"]]),
        fielding_zr=safe_float(play_line[header_indices["fld_zr_index"]]),
        fielding_eff=safe_float(play_line[header_indices["fld_eff_index"]]),
        fielding_stolen_bases_against=safe_int(play_line[header_indices["fld_sba_index"]]),
        fielding_runners_thrown_out=safe_int(play_line[header_indices["fld_rto_index"]]),
        fielding_ip=safe_float(play_line[header_indices["fld_ip_index"]]),
        fielding_passed_balls=safe_int(play_line[header_indices["fld_pb_index"]]),
        fielding_catcher_earned_runs=safe_int(play_line[header_indices["fld_cer_index"]]),
        fielding_reg_balls_in_zone=safe_int(play_line[header_indices["fld_rbiz_index"]]),
        fielding_reg_balls_in_zone_fielded=safe_int(play_line[header_indices["fld_rbizm_index"]]),
        fielding_likely_balls_in_zone=safe_int(play_line[header_indices["fld_lbiz_index"]]),
        fielding_likely_balls_in_zone_fielded=safe_int(play_line[header_indices["fld_lbizm_index"]]),
        fielding_even_balls_in_zone=safe_int(play_line[header_indices["fld_ebiz_index"]]),
        fielding_even_balls_in_zone_fielded=safe_int(play_line[header_indices["fld_ebizm_index"]]),
        fielding_unlikely_balls_in_zone=safe_int(play_line[header_indices["fld_ubiz_index"]]),
        fielding_unlikely_balls_in_zone_fielded=safe_int(play_line[header_indices["fld_ubizm_index"]]),
        fielding_remote_balls_in_zone=safe_int(play_line[header_indices["fld_zbiz_index"]]),
        fielding_remote_balls_in_zone_fielded=safe_int(play_line[header_indices["fld_zbizm_index"]]),
        fielding_impossible_balls_in_zone=safe_int(play_line[header_indices["fld_ibiz_index"]]),
        fielding_framing_runs=safe_float(play_line[header_indices["fld_frm_index"]]),
        fielding_arm_runs=safe_float(play_line[header_indices["fld_arm_index"]])
    )
    
def __weighted_avg__(a_stat, a_weight, b_stat, b_weight):
    return (a_stat * a_weight + b_stat * b_weight) / (a_weight + b_weight) if (a_weight + b_weight) > 0 else 0

def merge_stats_fielder(a: StatsFielder, b: StatsFielder) -> StatsFielder:
    c = StatsFielder()

    c.fielding_position = a.fielding_position
    c.fielding_games = a.fielding_games + b.fielding_games
    c.fielding_games_started = a.fielding_games_started + b.fielding_games_started
    c.fielding_total_chances = a.fielding_total_chances + b.fielding_total_chances
    c.fielding_assists = a.fielding_assists + b.fielding_assists
    c.fielding_putouts = a.fielding_putouts + b.fielding_putouts
    c.fielding_errors = a.fielding_errors + b.fielding_errors
    c.fielding_double_plays = a.fielding_double_plays + b.fielding_double_plays
    c.fielding_double_plays = a.fielding_double_plays + b.fielding_double_plays
    c.fielding_pct = __weighted_avg__(a.fielding_pct, ip_to_ip_w_remainder(a.fielding_ip), b.fielding_pct, ip_to_ip_w_remainder(b.fielding_ip))
    c.fielding_rng = __weighted_avg__(a.fielding_rng, ip_to_ip_w_remainder(a.fielding_ip), b.fielding_rng, ip_to_ip_w_remainder(b.fielding_ip))
    c.fielding_zr = a.fielding_zr + b.fielding_zr
    c.fielding_eff = __weighted_avg__(a.fielding_eff, ip_to_ip_w_remainder(a.fielding_ip), b.fielding_eff, ip_to_ip_w_remainder(b.fielding_ip))
    c.fielding_stolen_bases_against = a.fielding_stolen_bases_against + b.fielding_stolen_bases_against
    c.fielding_runners_thrown_out = a.fielding_runners_thrown_out + b.fielding_runners_thrown_out
    c.fielding_ip = add_ip(a.fielding_ip, b.fielding_ip)
    c.fielding_passed_balls = a.fielding_passed_balls + b.fielding_passed_balls
    c.fielding_catcher_earned_runs = a.fielding_catcher_earned_runs + b.fielding_catcher_earned_runs
    c.fielding_reg_balls_in_zone = a.fielding_reg_balls_in_zone + b.fielding_reg_balls_in_zone
    c.fielding_reg_balls_in_zone_fielded = a.fielding_reg_balls_in_zone_fielded + b.fielding_reg_balls_in_zone_fielded
    c.fielding_likely_balls_in_zone = a.fielding_likely_balls_in_zone + b.fielding_likely_balls_in_zone
    c.fielding_likely_balls_in_zone_fielded = a.fielding_likely_balls_in_zone_fielded + b.fielding_likely_balls_in_zone_fielded
    c.fielding_even_balls_in_zone = a.fielding_even_balls_in_zone + b.fielding_even_balls_in_zone
    c.fielding_even_balls_in_zone_fielded = a.fielding_even_balls_in_zone_fielded + b.fielding_even_balls_in_zone_fielded
    c.fielding_unlikely_balls_in_zone = a.fielding_unlikely_balls_in_zone + b.fielding_unlikely_balls_in_zone
    c.fielding_unlikely_balls_in_zone_fielded = a.fielding_unlikely_balls_in_zone_fielded + b.fielding_unlikely_balls_in_zone_fielded
    c.fielding_remote_balls_in_zone = a.fielding_remote_balls_in_zone + b.fielding_remote_balls_in_zone
    c.fielding_remote_balls_in_zone_fielded = a.fielding_remote_balls_in_zone_fielded + b.fielding_remote_balls_in_zone_fielded
    c.fielding_impossible_balls_in_zone = a.fielding_impossible_balls_in_zone + b.fielding_impossible_balls_in_zone
    c.fielding_framing_runs = a.fielding_framing_runs + b.fielding_framing_runs
    c.fielding_arm_runs = a.fielding_arm_runs + b.fielding_arm_runs

    return c