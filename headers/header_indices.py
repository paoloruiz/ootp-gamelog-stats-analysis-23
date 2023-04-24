from dataclasses import dataclass
from typing import Dict, List
from headers.util import search_with_reasonable_error

from individual_league.stats_player.batter import get_batter_header_indices
from individual_league.stats_player.pitcher import get_pitcher_header_indices
from individual_league.stats_player.fielder import get_fielder_header_indices

@dataclass
class StatsHeaderIndices:
    main_header_indices: Dict[str, int]
    batter_header_indices: Dict[str, int]
    pitcher_header_indices: Dict[str, int]
    fielding_header_indices: Dict[str, int]

def stats_headers_to_header_indices(headers: List[str]) -> StatsHeaderIndices:
    header_indices = {}

    batter_header_indices = get_batter_header_indices(headers)
    pitcher_header_indices = get_pitcher_header_indices(headers)
    fielder_header_indices = get_fielder_header_indices(headers)

    header_indices["cid_index"] = search_with_reasonable_error(headers, "CID")
    header_indices["id_index"] = search_with_reasonable_error(headers, "ID")
    header_indices["pos_index"] = search_with_reasonable_error(headers, "POS")
    header_indices["tm_index"] = search_with_reasonable_error(headers, "TM")
    header_indices["tm_short_index"] = header_indices["tm_index"] + 1 if headers[header_indices["tm_index"] + 1] == "TM" else -1

    return StatsHeaderIndices(
        main_header_indices=header_indices,
        batter_header_indices=batter_header_indices,
        pitcher_header_indices=pitcher_header_indices,
        fielding_header_indices=fielder_header_indices
    )
