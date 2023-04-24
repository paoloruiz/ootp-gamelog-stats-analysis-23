import os
from typing import Dict, List, Tuple
from game_log.parse_box_score_players import get_box_score_players
from game_log.parse_log import parse_log

from game_log.play import Play
from individual_league.league_stats import AllLeagueStats
from individual_league.load_players import load_card_players, load_card_players_file, load_stats_players
from individual_league.pitcher_stats import PitcherStats
from individual_league.stats_player.base_stats_player import BaseStatsPlayer


def load_tournament_plays() -> Tuple[Dict[str, List[Play]], AllLeagueStats, Dict[str, List[BaseStatsPlayer]], PitcherStats]:
    tourney_dirs = os.listdir("data/tournament")
    card_players = load_card_players()
    
    plays_by_tourney_type: Dict[str, List[Play]] = {}

    league_stats = AllLeagueStats()
    pitcher_stats = PitcherStats()

    all_stats_players: Dict[str, List[BaseStatsPlayer]] = {}
    
    for t_dir in tourney_dirs:
        ttype = t_dir.split("_")[0][1:]

        if ttype not in tourney_dirs:
            plays_by_tourney_type[ttype] = []

        card_players_to_use = card_players
        if "pt_card_list.csv"  in os.listdir("data/tournament/" + t_dir):
            card_players_to_use = load_card_players_file("tournament/" + t_dir + "/pt_card_list.csv")

        stats_players = list(load_stats_players(directory="data/tournament/" + t_dir, card_players=card_players_to_use, league_stats=league_stats, ttype=ttype, pitcher_stats=pitcher_stats).values())
        all_stats_players[ttype] = stats_players

        games = os.listdir("data/tournament/" + t_dir + "/games/")
        for game_file in games:
            with open("data/tournament/" + t_dir + "/games/" + game_file, "r") as f:
                home_team = get_box_score_players("data/tournament/" + t_dir + "/box_scores/" + game_file.replace(".txt", ".home.txt"), stats_players)
                visiting_team = get_box_score_players("data/tournament/" + t_dir + "/box_scores/" + game_file.replace(".txt", ".visiting.txt"), stats_players)
                lines = f.readlines()
                plays_by_tourney_type[ttype].extend(parse_log(lines, stats_players=stats_players, home_bsl=home_team, visiting_bsl=visiting_team))

    return plays_by_tourney_type, league_stats, all_stats_players, pitcher_stats


def load_tournament_plays_testing(tourney_type: str, mod_num: int) -> Tuple[List[Play], List[Play]]:
    tourney_dirs = os.listdir("data/tournament")
    card_players = load_card_players()
    
    analysis_data_plays: List[Play] = []
    test_data_plays: List[Play] = []
    
    i = 0
    for t_dir in tourney_dirs:
        ttype = t_dir.split("_")[0][1:]
        if ttype != tourney_type:
            continue

        league_stats = AllLeagueStats()
        pitcher_stats = PitcherStats()

        stats_players = list(load_stats_players(directory="data/tournament/" + t_dir, card_players=card_players, league_stats=league_stats, pitcher_stats=pitcher_stats, ttype=ttype).values())

        games = os.listdir("data/tournament/" + t_dir + "/games/")
        for game_file in games:
            with open("data/tournament/" + t_dir + "/games/" + game_file, "r") as f:
                home_team = get_box_score_players("data/tournament/" + t_dir + "/box_scores/" + game_file.replace(".txt", ".home.txt"), stats_players)
                visiting_team = get_box_score_players("data/tournament/" + t_dir + "/box_scores/" + game_file.replace(".txt", ".visiting.txt"), stats_players)
                lines = f.readlines()
                if i % mod_num == 0:
                    test_data_plays.extend(parse_log(lines, stats_players=stats_players, home_bsl=home_team, visiting_bsl=visiting_team))
                else:
                    analysis_data_plays.extend(parse_log(lines, stats_players=stats_players, home_bsl=home_team, visiting_bsl=visiting_team))
                i += 1

    return (analysis_data_plays, test_data_plays)


def load_top_team_tournament_plays(tourney_type: str) -> List[List[Play]]:
    tourney_dirs = os.listdir("data/tournament")
    card_players = load_card_players()
    
    plays: List[List[Play]] = []
    
    for t_dir in tourney_dirs:
        ttype = t_dir.split("_")[0][1:]
        if ttype != tourney_type:
            continue

        card_players_to_use = card_players
        if "pt_card_list.csv"  in os.listdir("data/tournament/" + t_dir):
            card_players_to_use = load_card_players_file("tournament/" + t_dir + "/pt_card_list.csv")

        league_stats = AllLeagueStats()
        pitcher_stats = PitcherStats()

        stats_players = list(load_stats_players(directory="data/tournament/" + t_dir, card_players=card_players_to_use, league_stats=league_stats, pitcher_stats=pitcher_stats, ttype=ttype).values())

        games = os.listdir("data/tournament/" + t_dir + "/games/")
        max_game_num = 0
        for game_file in games:
            max_game_num = max(max_game_num, int(game_file.replace(".txt", "")))
        for game_file in games:
            game_num = int(game_file.replace(".txt", ""))
            if max_game_num - 10 > game_num:
                continue
            with open("data/tournament/" + t_dir + "/games/" + game_file, "r") as f:
                home_team = get_box_score_players("data/tournament/" + t_dir + "/box_scores/" + game_file.replace(".txt", ".home.txt"), stats_players)
                visiting_team = get_box_score_players("data/tournament/" + t_dir + "/box_scores/" + game_file.replace(".txt", ".visiting.txt"), stats_players)
                lines = f.readlines()
                plays.append(parse_log(lines, stats_players=stats_players, home_bsl=home_team, visiting_bsl=visiting_team))

    return plays