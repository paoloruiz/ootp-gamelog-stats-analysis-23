from typing import Dict, List, Tuple
from analysis.splits_breakdown import SplitsBreakdown
from analysis.xbh import analyze_xbh_gamelog_large_filter_breakdown
from game_log.play import BattingPlay
from tournament.load_tourney_plays import load_tournament_plays_testing


analysis_plays, testing_plays = load_tournament_plays_testing(tourney_type="openbronze", mod_num=5)

splits_breakdown = SplitsBreakdown()
splits_breakdown.init()

analysis_fn, filter_fn, count_fn = analyze_xbh_gamelog_large_filter_breakdown(analysis_plays)

gs_types = set()
bat_plays: List[BattingPlay] = list(filter(lambda p: p.playtype == "BATTING_PLAY", analysis_plays))
for p in bat_plays:
    splits_breakdown.record(p)
    gs_types.add(p.game_sub_result)
print(gs_types)

def analyze_batter(p: BattingPlay) -> float:
    pred_strikeout = 0.0
    t_possibilities = ["R", "L"]
    for throws in t_possibilities:
        rating = p.batting_player.gap_vl if throws == "L" else p.batting_player.gap_vr
        pred_strikeout += analysis_fn(throws, p.batting_player.bats, [rating], [0]) / 2

    return pred_strikeout

filtered_testing_plays: List[BattingPlay] = list(filter(filter_fn, testing_plays))

bats = ["R", "L", "S"]
throws = ["R", "L"]
for b in bats:
    for t in throws:
        flt_b_p_test = list(filter(lambda p: p.batting_player.bats == b and p.pitching_player.throws == t, filtered_testing_plays))

        true_count = sum(map(count_fn, flt_b_p_test))
        pred_count = sum(map(analyze_batter, flt_b_p_test))
        tot_diff = sum(map(lambda p: abs(count_fn(p) - analyze_batter(p)), flt_b_p_test))

        print(b, "-", t)
        print("true", true_count, "pred", round(pred_count, 3), "diff", round(true_count - pred_count, 3))
        print("count", len(flt_b_p_test), "dpc", round(abs(true_count - pred_count) / true_count * 100, 2), "abs_dpc", round(tot_diff / len(flt_b_p_test) * 100, 2))
        print()

true_count = sum(map(count_fn, filtered_testing_plays))
pred_count = sum(map(analyze_batter, filtered_testing_plays))
tot_diff = sum(map(lambda p: abs(count_fn(p) - analyze_batter(p)), filtered_testing_plays))

print("true", true_count, "pred", round(pred_count, 3), "diff", round(true_count - pred_count, 3))
print("count", len(filtered_testing_plays), "dpc", round(abs(true_count - pred_count) / true_count * 100, 2), "abs_dpc", round(tot_diff / len(filtered_testing_plays) * 100, 2))


