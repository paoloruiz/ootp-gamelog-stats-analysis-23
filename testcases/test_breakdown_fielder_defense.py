from typing import List
from analysis.fielding import analyze_defense_gamelog_breakdown
from analysis.splits_breakdown import SplitsBreakdown
from game_log.play import BattingPlay
from tournament.load_tourney_plays import load_tournament_plays_testing


analysis_plays, testing_plays = load_tournament_plays_testing(tourney_type="openbronze", mod_num=5)

splits_breakdown = SplitsBreakdown()
splits_breakdown.init()

analysis_fn, filter_fn, count_fn, valid_locs = analyze_defense_gamelog_breakdown(analysis_plays)

gs_types = set()
bat_plays: List[BattingPlay] = list(filter(lambda p: p.playtype == "BATTING_PLAY", analysis_plays))

filtered_testing_plays: List[BattingPlay] = list(filter(filter_fn, testing_plays))

for loc in valid_locs:
    flt_b_p_test = list(filter(lambda p: loc in p.bip_event.location, filtered_testing_plays))

    true_count = sum(map(count_fn, flt_b_p_test))
    pred_count = sum(map(analysis_fn, flt_b_p_test))
    tot_diff = sum(map(lambda p: abs(count_fn(p) - analysis_fn(p)), flt_b_p_test))

    print(loc)
    print("true", true_count, "pred", round(pred_count, 3), "diff", round(true_count - pred_count, 3))
    print("count", len(flt_b_p_test), "dpc", round(abs(true_count - pred_count) / true_count * 100, 2), "abs_dpc", round(tot_diff / len(flt_b_p_test) * 100, 2))
    print()

true_count = sum(map(count_fn, filtered_testing_plays))
pred_count = sum(map(analysis_fn, filtered_testing_plays))
tot_diff = sum(map(lambda p: abs(count_fn(p) - analysis_fn(p)), filtered_testing_plays))

print("true", true_count, "pred", round(pred_count, 3), "diff", round(true_count - pred_count, 3))
print("count", len(filtered_testing_plays), "dpc", round(abs(true_count - pred_count) / true_count * 100, 2), "abs_dpc", round(tot_diff / len(filtered_testing_plays) * 100, 2))
