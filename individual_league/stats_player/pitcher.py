from dataclasses import dataclass
from typing import Dict, List

from headers.util import safe_float, safe_int, search_with_no_error, search_with_reasonable_error
from util.ip_math import add_ip, ip_to_ip_w_remainder


@dataclass
class StatsPitcher:
    pitcher_games: int = 0
    pitcher_games_start: int = 0
    pitcher_wins: int = 0
    pitcher_losses: int = 0
    pitcher_ip: float = 0.0
    pitcher_bf: int = 0
    pitcher_ab: int = 0
    pitcher_hits_against: int = 0
    pitcher_singles: int = 0
    pitcher_doubles: int = 0
    pitcher_triples: int = 0
    pitcher_homeruns: int = 0
    pitcher_runs_against: int = 0
    pitcher_earned_runs_against: int = 0
    pitcher_walks: int = 0
    pitcher_intentional_walks: int = 0
    pitcher_strikeouts: int = 0
    pitcher_hit_by_pitch: int = 0
    pitcher_babip: float = 0.0
    pitcher_sac_hits: int = 0
    pitcher_sac_flies: int = 0
    pitcher_wild_pitches: int = 0
    pitcher_double_plays: int = 0
    pitcher_relief_appearances: int = 0
    pitcher_pli: float = 0.0
    pitcher_pitches_per_game: float = 0.0
    pitcher_pitches: int = 0
    pitcher_groundballs: int = 0
    pitcher_flyballs: int = 0
    pitcher_stolen_bases: int = 0
    pitcher_caught_stealing: int = 0
    pitcher_fip: float = 0.0
    pitcher_wpa: float = 0.0
    pitcher_siera: float = 0.0
    pitcher_war: float = 0.0
    pitcher_rwar: float = 0.0

def get_pitcher_header_indices(headers: List[str]) -> Dict[str, int]:
    header_indices = {}
    pitcher_starting_index = search_with_reasonable_error(headers, "BsR")

    header_indices["pit_games_index"] = search_with_reasonable_error(headers, "G", pitcher_starting_index)
    header_indices["pit_games_started_index"] = search_with_reasonable_error(headers, "GS", pitcher_starting_index)
    header_indices["pit_wins_index"] = search_with_no_error(headers, "W", pitcher_starting_index)
    header_indices["pit_losses_index"] = search_with_no_error(headers, "L", pitcher_starting_index)
    header_indices["pit_ip_index"] = search_with_reasonable_error(headers, "IP", pitcher_starting_index)
    header_indices["pit_bf_index"] = search_with_reasonable_error(headers, "BF", pitcher_starting_index)
    header_indices["pit_ab_index"] = search_with_reasonable_error(headers, "AB", pitcher_starting_index)
    header_indices["pit_ha_index"] = search_with_reasonable_error(headers, "HA", pitcher_starting_index)
    header_indices["pit_singles_index"] = search_with_reasonable_error(headers, "1B", pitcher_starting_index)
    header_indices["pit_doubles_index"] = search_with_reasonable_error(headers, "2B", pitcher_starting_index)
    header_indices["pit_triples_index"] = search_with_reasonable_error(headers, "3B", pitcher_starting_index)
    header_indices["pit_homeruns_index"] = search_with_reasonable_error(headers, "HR", pitcher_starting_index)
    header_indices["pit_ra_index"] = search_with_reasonable_error(headers, "R", pitcher_starting_index)
    header_indices["pit_er_index"] = search_with_reasonable_error(headers, "ER", pitcher_starting_index)
    header_indices["pit_bb_index"] = search_with_reasonable_error(headers, "BB", pitcher_starting_index)
    header_indices["pit_ibb_index"] = search_with_reasonable_error(headers, "IBB", pitcher_starting_index)
    header_indices["pit_so_index"] = search_with_reasonable_error(headers, "K", pitcher_starting_index)
    header_indices["pit_hbp_index"] = search_with_reasonable_error(headers, "HP", pitcher_starting_index)
    header_indices["pit_babip_index"] = search_with_reasonable_error(headers, "BABIP", pitcher_starting_index)
    header_indices["pit_sh_index"] = search_with_reasonable_error(headers, "SH", pitcher_starting_index)
    header_indices["pit_sf_index"] = search_with_reasonable_error(headers, "SF", pitcher_starting_index)
    header_indices["pit_wp_index"] = search_with_reasonable_error(headers, "WP", pitcher_starting_index)
    header_indices["pit_dp_index"] = search_with_reasonable_error(headers, "DP", pitcher_starting_index)
    header_indices["pit_relief_app_index"] = search_with_reasonable_error(headers, "RA", pitcher_starting_index)
    header_indices["pit_pli_index"] = search_with_reasonable_error(headers, "pLi", pitcher_starting_index)
    header_indices["pit_ppg_index"] = search_with_no_error(headers, "PPG", pitcher_starting_index)
    header_indices["pit_pi_index"] = search_with_no_error(headers, "PI", pitcher_starting_index)
    header_indices["pit_gb_index"] = search_with_reasonable_error(headers, "GB", pitcher_starting_index)
    header_indices["pit_fb_index"] = search_with_reasonable_error(headers, "FB", pitcher_starting_index)
    header_indices["pit_sb_index"] = search_with_reasonable_error(headers, "SB", pitcher_starting_index)
    header_indices["pit_cs_index"] = search_with_reasonable_error(headers, "CS", pitcher_starting_index)
    header_indices["pit_fip_index"] = search_with_reasonable_error(headers, "FIP", pitcher_starting_index)
    header_indices["pit_wpa_index"] = search_with_reasonable_error(headers, "WPA", pitcher_starting_index)
    header_indices["pit_siera_index"] = search_with_reasonable_error(headers, "SIERA", pitcher_starting_index)
    header_indices["pit_war_index"] = search_with_reasonable_error(headers, "WAR", pitcher_starting_index)
    header_indices["pit_rwar_index"] = search_with_reasonable_error(headers, "rWAR", pitcher_starting_index)

    return header_indices

def new_stats_pitcher(header_indices: Dict[str, int], play_line: List[str]) -> StatsPitcher:
    return StatsPitcher(
        pitcher_games=safe_int(play_line[header_indices["pit_games_index"]]),
        pitcher_games_start=safe_int(play_line[header_indices["pit_games_started_index"]]),
        pitcher_wins=safe_int(play_line[header_indices["pit_wins_index"]]) if header_indices["pit_wins_index"] else 0,
        pitcher_losses=safe_int(play_line[header_indices["pit_losses_index"]]) if header_indices["pit_losses_index"] else 0,
        pitcher_ip=safe_float(play_line[header_indices["pit_ip_index"]]),
        pitcher_bf=safe_int(play_line[header_indices["pit_bf_index"]]),
        pitcher_ab=safe_int(play_line[header_indices["pit_ab_index"]]),
        pitcher_hits_against=safe_int(play_line[header_indices["pit_ha_index"]]),
        pitcher_singles=safe_int(play_line[header_indices["pit_singles_index"]]),
        pitcher_doubles=safe_int(play_line[header_indices["pit_doubles_index"]]),
        pitcher_triples=safe_int(play_line[header_indices["pit_triples_index"]]),
        pitcher_homeruns=safe_int(play_line[header_indices["pit_homeruns_index"]]),
        pitcher_runs_against=safe_int(play_line[header_indices["pit_ra_index"]]),
        pitcher_earned_runs_against=safe_int(play_line[header_indices["pit_er_index"]]),
        pitcher_walks=safe_int(play_line[header_indices["pit_bb_index"]]),
        pitcher_intentional_walks=safe_int(play_line[header_indices["pit_ibb_index"]]),
        pitcher_strikeouts=safe_int(play_line[header_indices["pit_so_index"]]),
        pitcher_hit_by_pitch=safe_int(play_line[header_indices["pit_hbp_index"]]),
        pitcher_babip=safe_float(play_line[header_indices["pit_babip_index"]]),
        pitcher_sac_hits=safe_int(play_line[header_indices["pit_sh_index"]]),
        pitcher_sac_flies=safe_int(play_line[header_indices["pit_sf_index"]]),
        pitcher_wild_pitches=safe_int(play_line[header_indices["pit_wp_index"]]),
        pitcher_double_plays=safe_int(play_line[header_indices["pit_dp_index"]]),
        pitcher_relief_appearances=safe_int(play_line[header_indices["pit_relief_app_index"]]),
        pitcher_pli=safe_float(play_line[header_indices["pit_pli_index"]]),
        pitcher_pitches_per_game=safe_float(play_line[header_indices["pit_ppg_index"]] if header_indices["pit_ppg_index"] > -1 else 0.0),
        pitcher_pitches=safe_int(play_line[header_indices["pit_pi_index"]] if header_indices["pit_ppg_index"] > -1 else 0),
        pitcher_groundballs=safe_int(play_line[header_indices["pit_gb_index"]]),
        pitcher_flyballs=safe_int(play_line[header_indices["pit_fb_index"]]),
        pitcher_stolen_bases=safe_int(play_line[header_indices["pit_sb_index"]]),
        pitcher_caught_stealing=safe_int(play_line[header_indices["pit_cs_index"]]),
        pitcher_fip=safe_float(play_line[header_indices["pit_fip_index"]]),
        pitcher_wpa=safe_float(play_line[header_indices["pit_wpa_index"]]),
        pitcher_siera=safe_float(play_line[header_indices["pit_siera_index"]]),
        pitcher_war=safe_float(play_line[header_indices["pit_war_index"]]),
        pitcher_rwar=safe_float(play_line[header_indices["pit_rwar_index"]]),
    )


def __weighted_avg__(a_stat, a_weight, b_stat, b_weight):
    return (a_stat * a_weight + b_stat * b_weight) / (a_weight + b_weight) if (a_weight + b_weight) > 0 else 0

def merge_stats_pitchers(a: StatsPitcher, b: StatsPitcher) -> StatsPitcher:
    c = StatsPitcher()

    c.pitcher_games = a.pitcher_games + b.pitcher_games
    c.pitcher_games_start = a.pitcher_games_start + b.pitcher_games_start
    c.pitcher_wins = a.pitcher_wins + b.pitcher_wins
    c.pitcher_losses = a.pitcher_losses + b.pitcher_losses
    c.pitcher_ip = add_ip(a.pitcher_ip, b.pitcher_ip)
    c.pitcher_bf = a.pitcher_bf + b.pitcher_bf
    c.pitcher_ab = a.pitcher_ab + b.pitcher_ab
    c.pitcher_hits_against = a.pitcher_hits_against + b.pitcher_hits_against
    c.pitcher_singles = a.pitcher_singles + b.pitcher_singles
    c.pitcher_doubles = a.pitcher_doubles + b.pitcher_doubles
    c.pitcher_triples = a.pitcher_triples + b.pitcher_triples
    c.pitcher_homeruns = a.pitcher_homeruns + b.pitcher_homeruns
    c.pitcher_runs_against = a.pitcher_runs_against + b.pitcher_runs_against
    c.pitcher_earned_runs_against = a.pitcher_earned_runs_against + b.pitcher_earned_runs_against
    c.pitcher_walks = a.pitcher_walks + b.pitcher_walks
    c.pitcher_intentional_walks = a.pitcher_intentional_walks + b.pitcher_intentional_walks
    c.pitcher_strikeouts = a.pitcher_strikeouts + b.pitcher_strikeouts
    c.pitcher_hit_by_pitch = a.pitcher_hit_by_pitch + b.pitcher_hit_by_pitch
    c.pitcher_babip = a.pitcher_babip + b.pitcher_babip
    c.pitcher_sac_hits = a.pitcher_sac_hits + b.pitcher_sac_hits
    c.pitcher_sac_flies = a.pitcher_sac_flies + b.pitcher_sac_flies
    c.pitcher_wild_pitches = a.pitcher_wild_pitches + b.pitcher_wild_pitches
    c.pitcher_double_plays = a.pitcher_double_plays + b.pitcher_double_plays
    c.pitcher_relief_appearances = a.pitcher_relief_appearances + b.pitcher_relief_appearances
    c.pitcher_pli = __weighted_avg__(a.pitcher_pli, a.pitcher_bf, b.pitcher_pli, b.pitcher_bf)
    if a.pitcher_pitches > 0 and b.pitcher_pitches > 0:
        c.pitcher_pitches_per_game = __weighted_avg__(a.pitcher_pitches_per_game, a.pitcher_bf, b.pitcher_pitches_per_game, b.pitcher_bf)
        c.pitcher_pitches = __weighted_avg__(a.pitcher_pitches, a.pitcher_bf, b.pitcher_pitches, b.pitcher_bf)
    elif a.pitcher_pitches > 0:
        c.pitcher_pitches_per_game = a.pitcher_pitches_per_game
        c.pitcher_pitches = a.pitcher_pitches
    elif b.pitcher_pitches > 0:
        c.pitcher_pitches_per_game = b.pitcher_pitches_per_game
        c.pitcher_pitches = b.pitcher_pitches
    c.pitcher_groundballs = a.pitcher_groundballs + b.pitcher_groundballs
    c.pitcher_flyballs = a.pitcher_flyballs + b.pitcher_flyballs
    c.pitcher_stolen_bases = a.pitcher_stolen_bases + b.pitcher_stolen_bases
    c.pitcher_caught_stealing = a.pitcher_caught_stealing + b.pitcher_caught_stealing
    c.pitcher_fip = __weighted_avg__(a.pitcher_fip, ip_to_ip_w_remainder(a.pitcher_ip), b.pitcher_fip, ip_to_ip_w_remainder(b.pitcher_ip))
    c.pitcher_wpa = a.pitcher_wpa + b.pitcher_wpa
    c.pitcher_siera = __weighted_avg__(a.pitcher_siera, ip_to_ip_w_remainder(a.pitcher_ip), b.pitcher_siera, ip_to_ip_w_remainder(b.pitcher_ip))
    c.pitcher_war = a.pitcher_war + b.pitcher_war
    c.pitcher_rwar = a.pitcher_rwar + b.pitcher_rwar

    return c