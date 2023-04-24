import os
from typing import Dict
from cards.card_player import CardPlayer, headers_to_header_indices, new_card_player
from headers.header_indices import stats_headers_to_header_indices
from individual_league.league_stats import AllLeagueStats
from individual_league.pitcher_stats import PitcherStats

from individual_league.stats_player.base_stats_player import BaseStatsPlayer, new_base_stats_player, read_in_ovr_info


def load_card_players() -> Dict[str, CardPlayer]:
    f = open('data/cards/pt_card_list.csv', 'r')

    headers_unparsed = f.readline()
    headers_split = headers_unparsed.split(',')
    headers = [(lambda h: h.replace('/', '').strip())(h) for h in headers_split]
    header_indices = headers_to_header_indices(headers)
    players = {}
    for line_unparsed in f.readlines():
        line_split = line_unparsed.split(',')
        play_line = [(lambda x: x.strip())(x) for x in line_split]
        base_card_player = new_card_player(header_indices, play_line)
        players[base_card_player.cid] = base_card_player
    f.close()

    return players

def load_card_players_file(file: str) -> Dict[str, CardPlayer]:
    f = open('data/' + file, 'r')

    headers_unparsed = f.readline()
    headers_split = headers_unparsed.split(',')
    headers = [(lambda h: h.replace('/', '').strip())(h) for h in headers_split]
    header_indices = headers_to_header_indices(headers)
    players = {}
    for line_unparsed in f.readlines():
        line_split = line_unparsed.split(',')
        play_line = [(lambda x: x.strip())(x) for x in line_split]
        base_card_player = new_card_player(header_indices, play_line)
        players[base_card_player.cid] = base_card_player
    f.close()

    return players


def load_stats_players(
    directory: str,
    card_players: Dict[str, CardPlayer],
    league_stats: AllLeagueStats,
    pitcher_stats: PitcherStats,
    ttype: str
):
    filenames = list(os.listdir(directory))
    if not "ovr.csv" in filenames:
        raise Exception(directory + " has no ovr file")

    f = open(directory + "/ovr.csv", "r")
    headers_unparsed = f.readline()
    headers_split = headers_unparsed.split(',')
    headers = [(lambda h: h.replace('/', '').strip())(h) for h in headers_split]
    header_indices = stats_headers_to_header_indices(headers)

    players: Dict[str, BaseStatsPlayer] = {}
    for line_unparsed in f.readlines():
        line_split = line_unparsed.split(',')
        play_line = [(lambda x: x.strip())(x) for x in line_split]
        base_stats_player = new_base_stats_player(header_indices, play_line, card_players)
        players[base_stats_player.cid_with_id] = base_stats_player
        read_in_ovr_info(header_indices=header_indices, play_line=play_line, existing_players=players)
        league_stats.capture_player_data(ttype, players[base_stats_player.cid_with_id])
        pitcher_stats.capture_player_data(players[base_stats_player.cid_with_id])
    f.close()

    return players
