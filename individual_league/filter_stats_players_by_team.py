from typing import Dict, List, Set
from cards.card_player import CardPlayer

from individual_league.stats_player.base_stats_player import BaseStatsPlayer

def __is_team_match__(team_name: str, stats_player: BaseStatsPlayer) -> bool:
    return stats_player.team_name_only in team_name

def get_possible_batters_for_team(
    team_name: str,
    stats_players: List[BaseStatsPlayer]
) -> List[BaseStatsPlayer]:
    return list(filter(lambda p: p.stats_batter != None and p.stats_batter.ovr != None and p.stats_batter.ovr.batter_pa > 0 and __is_team_match__(team_name, p), stats_players))

def __get_possible_fielders_for_position__(
    stats_players: List[BaseStatsPlayer],
    pos: int
) -> List[BaseStatsPlayer]:
    return list(filter(lambda p: p.stats_fielder != None and pos in p.stats_fielder.keys(), stats_players))

def get_possible_fielders_for_team(
    stats_players: List[BaseStatsPlayer]
) -> Dict[int, List[BaseStatsPlayer]]:
    team_fielders = {}
    for i in range(2, 10):
        team_fielders[i] = __get_possible_fielders_for_position__(stats_players, i)
    return team_fielders

def get_possible_pitchers_for_team(
    team_name: str,
    stats_players: List[BaseStatsPlayer]
) -> List[BaseStatsPlayer]:
    return list(filter(lambda p: p.stats_pitcher != None and p.stats_pitcher.all != None and p.stats_pitcher.all.pitcher_bf > 0 and __is_team_match__(team_name, p), stats_players))

def get_player_from_list(
    player_name: str,
    stats_players: List[BaseStatsPlayer]
) -> CardPlayer:
    possible_players: List[BaseStatsPlayer] = list(filter(lambda p: p.card_player.name == player_name, stats_players))

    if len(possible_players) > 1:
        name_set: Set[str] = set(map(lambda p: p.card_player.full_title, possible_players))
        if len(name_set) == 1:
            return possible_players[0].card_player

    if len(possible_players) != 1:
        raise Exception("Did not find an exact match for possible players: " + str(possible_players) + ", name: " + player_name + ", possible players: " + str(list(map(lambda p: p.card_player.name, stats_players))))

    return possible_players[0].card_player

def get_stats_player_from_list(
    player_name: str,
    stats_players: List[BaseStatsPlayer]
) -> CardPlayer:
    possible_players: List[BaseStatsPlayer] = list(filter(lambda p: p.card_player.name == player_name, stats_players))

    if len(possible_players) > 1:
        name_set: Set[str] = set(map(lambda p: p.card_player.full_title, possible_players))
        if len(name_set) != 1:
            raise Exception("Did not find an exact match for possible players: " + str(possible_players) + ", name: " + player_name + ", possible players: " + str(list(map(lambda p: p.card_player.name, stats_players))))

        if possible_players[0].stats_fielder == None:
            for p in possible_players:
                if p.stats_fielder != None:
                    raise Exception("Did not find an exact match for possible players: " + str(possible_players) + ", name: " + player_name + ", possible players: " + str(list(map(lambda p: p.card_player.name, stats_players))))

        positions = set(possible_players[0].stats_fielder.keys())
        for p in possible_players:
            if p.stats_fielder == None or positions != set(p.stats_fielder.keys()):
                raise Exception("Did not find an exact match for possible players: " + str(possible_players) + ", name: " + player_name + ", possible players: " + str(list(map(lambda p: p.card_player.name, stats_players))))

        return possible_players[0]


    if len(possible_players) != 1:
        raise Exception("Did not find an exact match for possible players: " + str(possible_players) + ", name: " + player_name + ", possible players: " + str(list(map(lambda p: p.card_player.name, stats_players))))

    return possible_players[0]