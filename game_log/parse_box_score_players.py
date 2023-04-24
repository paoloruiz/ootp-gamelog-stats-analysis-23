from typing import List

from game_log.box_score_lineup import BoxScoreLineup
from individual_league.stats_player.base_stats_player import DUMMY_STATS_PLAYER, BaseStatsPlayer

def __match_player__(id: str, players: List[BaseStatsPlayer], filename: str) -> BaseStatsPlayer:
    matched_players = list(filter(lambda p: p.league_id == id, players))
    if len(matched_players) == 0:
        return DUMMY_STATS_PLAYER
    if len(matched_players) != 1:
        raise Exception("matched the wrong number of players for " + filename + ": " + str(matched_players), ", with id: " + id)

    return matched_players[0]


def get_box_score_players(filename: str, all_stats_players: List[BaseStatsPlayer]):
    bsl = BoxScoreLineup(filename=filename)
    mode: str = "NONE"
    with open(filename, "r") as f:
        for line in f.readlines():
            l = line.strip()
            if l == "starting":
                mode = "STARTERS"
                continue
            elif l == "replacements":
                mode = "REPLACEMENTS"
                continue
            elif l == "pitchers":
                mode = "PITCHERS"
                continue

            if mode == "STARTERS":
                l_spl = l.split(";")
                player_id = l_spl[0]
                player = __match_player__(player_id, all_stats_players, filename)
                positions = list(map(int, l_spl[1].split(",")))
                bsl.add_starter(player, positions)
            elif mode == "REPLACEMENTS":
                l_spl = l.split(";")
                player_id = l_spl[0]
                player = __match_player__(player_id, all_stats_players, filename)
                positions = list(map(int, l_spl[1].split(",")))
                bsl.add_replacement(player, positions)
            else:
                l_spl = l.split(";")
                player_id = l_spl[0]
                player = __match_player__(player_id, all_stats_players, filename)
                bsl.add_pitcher(player)

    return bsl