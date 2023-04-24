from tournament.load_tourney_plays import load_tournament_plays
from game_log.league_player_reg_stats import TourneyLeague
import csv

tourney_plays, all_league_stats, all_stats_players, pitcher_stats = load_tournament_plays()

for ttype in tourney_plays.keys():
    league = TourneyLeague()
    league.read_plays(tourney_plays[ttype])

    vl_f = open('output/' + ttype + '_vL.csv', 'w', newline='')
    wl_f = csv.writer(vl_f)
    vr_f = open('output/' + ttype + '_vR.csv', 'w', newline='')
    wr_f = csv.writer(vr_f)

    wl_f.writerow(league.get_header_line())
    for lps in league.vl.values():
        wl_f.writerow(lps.get_sheet_line())
    wr_f.writerow(league.get_header_line())
    for lps in league.vr.values():
        wr_f.writerow(lps.get_sheet_line())

    vl_f.close()
    vr_f.close()