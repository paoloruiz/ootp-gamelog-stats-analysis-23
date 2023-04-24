
from analysis.walks import analyze_walks_gamelog_large_filter_breakdown
from analysis.homeruns import analyze_homeruns_gamelog_large_filter_breakdown
from analysis.hits import analyze_hits_gamelog_large_filter_breakdown
from analysis.strikeouts import analyze_strikeouts_gamelog_large_filter_breakdown
from tournament.load_tourney_plays import load_tournament_plays

ap, _, _, _ = load_tournament_plays()
analysis_plays = ap["openbronze"]

bb_fn, _, _ = analyze_walks_gamelog_large_filter_breakdown(analysis_plays)
hr_fn, _, _ = analyze_homeruns_gamelog_large_filter_breakdown(analysis_plays)
ht_fn, _, _ = analyze_hits_gamelog_large_filter_breakdown(analysis_plays)
so_fn, _, _ = analyze_strikeouts_gamelog_large_filter_breakdown(analysis_plays)

print("Lpitch Rbat")
print("bb", round(bb_fn("L", "R", [60, 1], [60, 80]) / bb_fn("L", "R", [60, 1], [60, 40]), 3))
print("hr", round(hr_fn("L", "R", [60, 1], [60, 80]) / hr_fn("L", "R", [60, 1], [60, 40]), 3))
print("ht", round(ht_fn("L", "R", [60, 1], [2.5, 80]) / ht_fn("L", "R", [60, 1], [2.5, 40]), 3))
print("so", round(so_fn("L", "R", [60, 1], [60, 80]) / so_fn("L", "R", [60, 1], [60, 40]), 3))

print("Lpitch Lbat")
print("bb", round(bb_fn("L", "L", [60, 1], [60, 80]) / bb_fn("L", "L", [60, 1], [60, 40]), 3))
print("hr", round(hr_fn("L", "L", [60, 1], [60, 80]) / hr_fn("L", "L", [60, 1], [60, 40]), 3))
print("ht", round(ht_fn("L", "L", [60, 1], [2.5, 80]) / ht_fn("L", "L", [60, 1], [2.5, 40]), 3))
print("so", round(so_fn("L", "L", [60, 1], [60, 80]) / so_fn("L", "L", [60, 1], [60, 40]), 3))

print("Lpitch Sbat")
print("bb", round(bb_fn("L", "S", [60, 1], [60, 80]) / bb_fn("L", "S", [60, 1], [60, 40]), 3))
print("hr", round(hr_fn("L", "S", [60, 1], [60, 80]) / hr_fn("L", "S", [60, 1], [60, 40]), 3))
print("ht", round(ht_fn("L", "S", [60, 1], [2.5, 80]) / ht_fn("L", "S", [60, 1], [2.5, 40]), 3))
print("so", round(so_fn("L", "S", [60, 1], [60, 80]) / so_fn("L", "S", [60, 1], [60, 40]), 3))

print("Rpitch Rbat")
print("bb", round(bb_fn("R", "R", [60, 1], [60, 80]) / bb_fn("R", "R", [60, 1], [60, 40]), 3))
print("hr", round(hr_fn("R", "R", [60, 1], [60, 80]) / hr_fn("R", "R", [60, 1], [60, 40]), 3))
print("ht", round(ht_fn("R", "R", [60, 1], [2.5, 80]) / ht_fn("R", "R", [60, 1], [2.5, 40]), 3))
print("so", round(so_fn("R", "R", [60, 1], [60, 80]) / so_fn("R", "R", [60, 1], [60, 40]), 3))

print("Rpitch Lbat")
print("bb", round(bb_fn("R", "L", [60, 1], [60, 80]) / bb_fn("R", "L", [60, 1], [60, 40]), 3))
print("hr", round(hr_fn("R", "L", [60, 1], [60, 80]) / hr_fn("R", "L", [60, 1], [60, 40]), 3))
print("ht", round(ht_fn("R", "L", [60, 1], [2.5, 80]) / ht_fn("R", "L", [60, 1], [2.5, 40]), 3))
print("so", round(so_fn("R", "L", [60, 1], [60, 80]) / so_fn("R", "L", [60, 1], [60, 40]), 3))

print("Rpitch Sbat")
print("bb", round(bb_fn("R", "S", [60, 1], [60, 80]) / bb_fn("R", "S", [60, 1], [60, 40]), 3))
print("hr", round(hr_fn("R", "S", [60, 1], [60, 80]) / hr_fn("R", "S", [60, 1], [60, 40]), 3))
print("ht", round(ht_fn("R", "S", [60, 1], [2.5, 80]) / ht_fn("R", "S", [60, 1], [2.5, 40]), 3))
print("so", round(so_fn("R", "S", [60, 1], [60, 80]) / so_fn("R", "S", [60, 1], [60, 40]), 3))