

from dataclasses import dataclass
from typing import Callable, List

from individual_league.stats_player.base_stats_player import BaseStatsPlayer
from analysis.linear_regression import RegressionAnalysisModel, perform_regression

low_min_denom = 10

@dataclass
class PitchingPlayerFormulas:
    # (hold) => (steal attempts) / (hits)
    get_stolen_bases_attempted_per_hit: Callable[[int], float]
    # (hold) => (steal successes) / (steal attempt)
    get_caught_stealing_per_steal: Callable[[int], float]
    # (gb_type) => gidp / bip
    get_gidp_per_bip: Callable[[int], float]
    # (stamina) => bf / game
    get_bf_per_game: Callable[[int], float]

def get_pitcher_peripherals(players: List[BaseStatsPlayer]):
    pitchers_only = list(filter(lambda player: player.stats_pitcher.all.pitcher_bf > 0, players))

    sba_ram = RegressionAnalysisModel(
        get_x=lambda player: player.card_player.hold,
        get_y_numerator=lambda player: player.stats_pitcher.all.pitcher_stolen_bases + player.stats_pitcher.all.pitcher_caught_stealing, 
        get_y_denominator=lambda player: player.stats_pitcher.all.pitcher_singles + player.stats_pitcher.all.pitcher_walks + player.stats_pitcher.all.pitcher_hit_by_pitch,
        min_y_denom=low_min_denom,
        should_use_cooks_distance=True
    )
    sba_analysis = perform_regression(pitchers_only, sba_ram)
    

    steal_ram = RegressionAnalysisModel(
        get_x=lambda player: player.card_player.hold,
        get_y_numerator=lambda player: player.stats_pitcher.all.pitcher_caught_stealing, 
        get_y_denominator=lambda player: player.stats_pitcher.all.pitcher_stolen_bases + player.stats_pitcher.all.pitcher_caught_stealing,
        min_y_denom=2,
        should_use_cooks_distance=True
    )
    steal_analysis = perform_regression(pitchers_only, steal_ram)
    

    gidp_ram = RegressionAnalysisModel(
        get_x=lambda player: player.card_player.gb_type,
        get_y_numerator=lambda player: player.stats_pitcher.all.pitcher_double_plays, 
        get_y_denominator=lambda player: player.stats_pitcher.all.pitcher_ab - player.stats_pitcher.all.pitcher_strikeouts - player.stats_pitcher.all.pitcher_homeruns,
        min_y_denom=low_min_denom,
        should_use_cooks_distance=True
    )
    gidp_analysis = perform_regression(pitchers_only, gidp_ram)


    stam_ram = RegressionAnalysisModel(
        get_x=lambda player: player.card_player.stamina,
        get_y_numerator=lambda player: player.stats_pitcher.all.pitcher_bf, 
        get_y_denominator=lambda player: player.stats_pitcher.all.pitcher_games,
        min_y_denom=low_min_denom,
        should_use_cooks_distance=True
    )
    stam_analysis = perform_regression(pitchers_only, stam_ram)

    return PitchingPlayerFormulas(
        get_stolen_bases_attempted_per_hit=lambda stat: sba_analysis.slope * stat + sba_analysis.intercept,
        get_caught_stealing_per_steal=lambda stat: steal_analysis.slope * stat + steal_analysis.intercept,
        get_gidp_per_bip=lambda gb_type: gb_type * gidp_analysis.slope + gidp_analysis.intercept,
        get_bf_per_game=lambda stamina: stamina * stam_analysis.slope + stam_analysis.intercept
    )