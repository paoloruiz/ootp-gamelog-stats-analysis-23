from typing import Callable, Dict, List
from analysis.find_top_team_players import find_top_team_players
from analysis.pitcher_peripherals import get_pitcher_peripherals
from analysis.stolen_bases import get_stolen_bases_formulas
from analysis.triple_rate import analyze_triples_gamelog_large_filter_breakdown
from cards.card_player import CardPlayer
from game_log.play import BattingPlay
from individual_league.load_players import load_card_players
from projection.projected_batter import project_batters
from projection.projected_pitcher import project_relievers, project_starters
from tournament.load_tourney_plays import load_tournament_plays
from analysis.homeruns import analyze_homeruns_gamelog_large_filter_breakdown
from analysis.hits import analyze_hits_gamelog_large_filter_breakdown
from analysis.strikeouts import analyze_strikeouts_gamelog_large_filter_breakdown
from analysis.walks import analyze_walks_gamelog_large_filter_breakdown
from analysis.xbh import analyze_xbh_gamelog_large_filter_breakdown
from analysis.fielding import analyze_defense_gamelog_breakdown
from individual_league.determine_linear_weights import get_woba_constants
from util.generate_tourney_selections_sheet import generate_tourney_proj_batter_selections
from util.generate_worksheet import generate_worksheet
from projection.projection_headers import proj_batter_headers, proj_batter_hidden_cols, proj_starter_headers, proj_reliever_headers
import xlsxwriter

tourneys: Dict[str, Callable[[CardPlayer], bool]] = {
    "openbronze": lambda p: p.ovr < 70,
    "openiron": lambda p: p.ovr < 60
}

tourney_plays, all_league_stats, all_stats_players, pitcher_stats = load_tournament_plays()

card_players = load_card_players()

batters = list(filter(lambda p: p.position != 1 or p.con_ovr > 40, card_players.values()))
sp = list(filter(lambda p: " SP " in p.full_title or (p.stamina > 50 and p.stu_ovr > 40), card_players.values()))
rp = list(filter(lambda p: p.position == 1 or p.stu_ovr > 40, card_players.values()))

for ttype in tourneys.keys():
    workbook = xlsxwriter.Workbook('output/' + ttype + '_tourney_sheet.xlsx', { "use_future_functions": True })
    batter_sheet = workbook.add_worksheet("BAT")
    batter_select_sheet = workbook.add_worksheet("proj-bat-selections")
    sp_sheet = workbook.add_worksheet("SP")
    rp_sheet = workbook.add_worksheet("RP")

    linear_weights_model = get_woba_constants(all_stats_players[ttype], all_league_stats.league_stats[ttype])
    team_breakdown = find_top_team_players(ttype)
    t_plays: List[BattingPlay] = tourney_plays[ttype]
    print(team_breakdown.pitch_nums)

    filter_fn = tourneys[ttype]

    ttype_bats: List[CardPlayer] = list(filter(filter_fn, batters))
    ttype_sp: List[CardPlayer] = list(filter(filter_fn, sp))
    ttype_rp: List[CardPlayer] = list(filter(filter_fn, rp))

    stats_batters = list(filter(lambda p: p.stats_batter != None and p.stats_batter.ovr.batter_pa > 0, all_stats_players[ttype]))
    stats_starters = list(filter(lambda p: p.stats_pitcher != None and p.stats_pitcher.all.pitcher_bf > 0 and p.stats_pitcher.all.pitcher_pitches_per_game > 50, all_stats_players[ttype]))
    stats_relievers = list(filter(lambda p: p.stats_pitcher != None and p.stats_pitcher.all.pitcher_bf > 0 and p.stats_pitcher.all.pitcher_pitches_per_game < 30, all_stats_players[ttype]))

    hr_analysis, _, _ = analyze_homeruns_gamelog_large_filter_breakdown(t_plays)
    h_analysis, _, _ = analyze_hits_gamelog_large_filter_breakdown(t_plays)
    so_analysis, _, _ = analyze_strikeouts_gamelog_large_filter_breakdown(t_plays)
    bb_analysis, _, _ = analyze_walks_gamelog_large_filter_breakdown(t_plays)
    xbh_analysis, _, _ = analyze_xbh_gamelog_large_filter_breakdown(t_plays)
    triple_analysis, _, _ = analyze_triples_gamelog_large_filter_breakdown(t_plays)
    _, _, _, _, def_analysis = analyze_defense_gamelog_breakdown(t_plays)
    sb_formulas = get_stolen_bases_formulas(stats_batters)
    starter_formulas = get_pitcher_peripherals(stats_starters)
    reliever_formulas = get_pitcher_peripherals(stats_relievers)

    projected_batters = project_batters(
        batters=ttype_bats,
        team_breakdown=team_breakdown,
        lwm=linear_weights_model,
        league_stats=all_league_stats.league_stats[ttype],
        hr_analysis=hr_analysis,
        bb_analysis=bb_analysis,
        so_analysis=so_analysis,
        h_analysis=h_analysis,
        xbh_analysis=xbh_analysis,
        def_analysis=def_analysis,
        triple_analysis=triple_analysis,
        stolen_base_formulas=sb_formulas
    )
    projected_batters.sort(key=lambda p: p.war_ovr, reverse=True)
    generate_worksheet(projected_batters, batter_sheet, proj_batter_headers, "con", proj_batter_hidden_cols, "projected batters")

    generate_tourney_proj_batter_selections(batter_select_sheet, projected_batters, "projected batter selections")

    projected_starters = project_starters(
        pitchers=ttype_sp,
        lwm=linear_weights_model,
        team_breakdown=team_breakdown,
        pitcher_stats=pitcher_stats,
        pitching_formulas=starter_formulas,
        hr_analysis=hr_analysis,
        bb_analysis=bb_analysis,
        so_analysis=so_analysis,
        h_analysis=h_analysis,
        xbh_analysis=xbh_analysis,
        triple_analysis=triple_analysis
    )
    projected_starters.sort(key=lambda p: p.war_with_relief, reverse=True)
    generate_worksheet(projected_starters, sp_sheet, proj_starter_headers, "stu", [], "projected sp")

    projected_relievers = project_relievers(
        pitchers=ttype_rp,
        lwm=linear_weights_model,
        team_breakdown=team_breakdown,
        pitcher_stats=pitcher_stats,
        pitching_formulas=reliever_formulas,
        hr_analysis=hr_analysis,
        bb_analysis=bb_analysis,
        so_analysis=so_analysis,
        h_analysis=h_analysis,
        xbh_analysis=xbh_analysis,
        triple_analysis=triple_analysis
    )
    projected_relievers.sort(key=lambda p: p.war_ovr, reverse=True)
    generate_worksheet(projected_relievers, rp_sheet, proj_reliever_headers, "stu", [], "projected rp")

    workbook.close()