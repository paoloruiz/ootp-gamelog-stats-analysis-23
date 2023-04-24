from typing import Dict, List, Tuple
from analysis.splits_breakdown import SplitsBreakdown
from analysis.hits import analyze_hits_gamelog_large_filter_breakdown
from game_log.play import BattingPlay
from tournament.load_tourney_plays import load_tournament_plays_testing


analysis_plays, testing_plays = load_tournament_plays_testing(tourney_type="openbronze", mod_num=5)

splits_breakdown = SplitsBreakdown()
splits_breakdown.init()

analysis_fn, filter_fn, count_fn = analyze_hits_gamelog_large_filter_breakdown(analysis_plays)

gs_types = set()
bat_plays: List[BattingPlay] = list(filter(lambda p: p.playtype == "BATTING_PLAY", analysis_plays))
for p in bat_plays:
    splits_breakdown.record(p)
    gs_types.add(p.game_sub_result)
print(gs_types)

def analyze_pitcher(p: BattingPlay) -> float:
    p_against_breakdown: Dict[str, List[Tuple[float, float]]] = splits_breakdown.get_breakdown_pitcher_bab_against(p.pitching_player.throws)
    pred_strikeout = 0.0
    for bats in p_against_breakdown.keys():
        for rate, avg in p_against_breakdown[bats]:
            pred_strikeout += analysis_fn(p.pitching_player.throws, bats, [avg, p.times_faced_off], [p.pitching_player.gb_type, p.catcher_player.cabi]) * rate

    return pred_strikeout

filtered_testing_plays: List[BattingPlay] = list(filter(filter_fn, testing_plays))

bats = ["R", "L", "S"]
throws = ["R", "L"]
for b in bats:
    for t in throws:
        flt_b_p_test = list(filter(lambda p: p.batting_player.bats == b and p.pitching_player.throws == t, filtered_testing_plays))

        true_count = sum(map(count_fn, flt_b_p_test))
        pred_count = sum(map(analyze_pitcher, flt_b_p_test))

        print(b, "-", t)
        print("true", true_count, "pred", round(pred_count, 3), "diff", round(true_count - pred_count, 3))
        print("count", len(flt_b_p_test), "dpc", round(abs(true_count - pred_count) / true_count * 100, 2))
        print()

true_count = sum(map(count_fn, filtered_testing_plays))
pred_count = sum(map(analyze_pitcher, filtered_testing_plays))

print("true", true_count, "pred", round(pred_count, 3), "diff", round(true_count - pred_count, 3))
print("count", len(filtered_testing_plays), "dpc", round(abs(true_count - pred_count) / true_count * 100, 2))


