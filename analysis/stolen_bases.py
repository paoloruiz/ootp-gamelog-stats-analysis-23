from dataclasses import dataclass
from typing import Callable, List
from analysis.linear_regression import RegressionAnalysisModel, perform_reg_regression

from individual_league.stats_player.base_stats_player import BaseStatsPlayer

@dataclass
class StolenBasesFormulas:
    # (speed) => sba / (walks + hbp + singles)
    get_stolen_base_attempt_per_1b: Callable[[int], float]
    # (stealing) => steal / sba
    get_successful_steal_rate: Callable[[int], float]

low_min_denom = 10

def get_stolen_bases_formulas(players: List[BaseStatsPlayer]) -> StolenBasesFormulas:
    sba_ram = RegressionAnalysisModel(
        get_x=lambda player: player.card_player.speed,
        get_y_numerator=lambda player: player.stats_batter.ovr.batter_stolen_bases + player.stats_batter.ovr.batter_caught_stealing, 
        get_y_denominator=lambda player: player.stats_batter.ovr.batter_singles + player.stats_batter.ovr.batter_walks + player.stats_batter.ovr.batter_hit_by_pitch,
        min_y_denom=low_min_denom,
        should_use_cooks_distance=True
    )
    sba_analysis = perform_reg_regression(players, sba_ram)
    

    steal_ram = RegressionAnalysisModel(
        get_x=lambda player: player.card_player.steal,
        get_y_numerator=lambda player: player.stats_batter.ovr.batter_stolen_bases, 
        get_y_denominator=lambda player: player.stats_batter.ovr.batter_stolen_bases + player.stats_batter.ovr.batter_caught_stealing,
        min_y_denom=low_min_denom,
        should_use_cooks_distance=True
    )
    steal_analysis = perform_reg_regression(players, steal_ram)

    return StolenBasesFormulas(
        get_stolen_base_attempt_per_1b=lambda stat: sba_analysis.slope * stat + sba_analysis.intercept,
        get_successful_steal_rate=lambda stat: steal_analysis.slope * stat + steal_analysis.intercept
    )