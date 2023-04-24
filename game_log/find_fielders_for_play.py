from dataclasses import dataclass
from typing import Dict, List

from game_log.box_score_lineup import BoxScoreLineup
from cards.card_player import CardPlayer


def __parse_batted_ball_location__(loc: str) -> List[int]:
    if loc == "P" or loc == "PS":
        return [1]
    elif loc == "13S" or loc == "13":
        return [1, 3]
    elif loc == "15S" or loc == "15":
        return [1, 5]
    elif loc == "2L" or loc == "2R" or loc == "2RF" or loc == "2LF":
        return [2]
    elif loc == "23" or loc == "23F":
        return [2, 3]
    elif loc == "25" or loc == "25F":
        return [2, 5]
    elif loc == "3D" or loc == "3L" or loc == "3S" or loc == "3" or loc == "3F" or loc == "3SF" or loc == "3DF":
        return [3]
    elif loc == "34D" or loc == "34S" or loc == "34":
        return [3, 4]
    elif loc == "4MD" or loc == "4M" or loc == "4MS" or loc == "4" or loc == "4D" or loc == "4S":
        return [4]
    elif loc == "5D" or loc == "5S" or loc == "5L" or loc == "5" or loc == "5SF" or loc == "5F" or loc == "5DF":
        return [5]
    elif loc == "56D" or loc == "56" or loc == "56S":
        return [5, 6]
    elif loc == "6M" or loc == "6MD" or loc == "6D" or loc == "6S" or loc == "6MS" or loc == "6":
        return [6]
    elif loc == "7S" or loc == "7LM" or loc == "7LS" or loc == "7" or loc == "7LD" or loc == "7D" or loc == "7LMF" or loc == "7LSF" or loc == "7LDF":
        return [7]
    elif loc == "78S" or loc == "78M" or loc == "78D" or loc == "78XD":
        return [7, 8]
    elif loc == "8LS" or loc == "8RS" or loc == "8LM" or loc == "8RM" or loc == "8RXD" or loc == "8LD" or loc == "8RD" or loc == "8LXD":
        return [8]
    elif loc == "89S" or loc == "89M" or loc == "89D" or loc == "89XD":
        return [8, 9]
    elif loc == "9S" or loc == "9LS" or loc == "9LM" or loc == "9" or loc == "9LD" or loc == "9D" or loc == "9LSF" or loc == "9LMF" or loc == "9LDF":
        return [9]
    
    print(loc, "unrecognized batted ball location")
    exit()

canned_if_fielding = [50, 50, 50, 50, 50]
canned_of_fielding = [50, 50, 50, 50]

def position_to_location_defenses(fielder: CardPlayer, position: int) -> Dict[str, List[float]]:
    pos_rating = 0
    if position == 1:
        pos_rating = fielder.defensep
    elif position == 2:
        pos_rating = fielder.defensec
    elif position == 3:
        pos_rating = fielder.defense1b
    elif position == 4:
        pos_rating = fielder.defense2b
    elif position == 5:
        pos_rating = fielder.defense3b
    elif position == 6:
        pos_rating = fielder.defensess
    elif position == 7:
        pos_rating = fielder.defenself
    elif position == 8:
        pos_rating = fielder.defensecf
    elif position == 9:
        pos_rating = fielder.defenserf
    fielder_ratings = []
    if position < 7:
        fielder_ratings.extend([fielder.ifrange, fielder.iferr, fielder.turndp, fielder.ifarm, pos_rating])
    else:
        fielder_ratings.extend([fielder.ofrange, fielder.oferr, fielder.ofarm, pos_rating])

    if position == 2:
        return {
            "2L": fielder_ratings,
            "2R": fielder_ratings,
            "23": fielder_ratings + canned_if_fielding,
            "25": fielder_ratings + canned_if_fielding
        }
    elif position == 3:
        return {
            "23": canned_if_fielding + fielder_ratings,
            "3D": fielder_ratings,
            "3L": fielder_ratings,
            "3S": fielder_ratings,
            "3": fielder_ratings,
            "34D": fielder_ratings + canned_if_fielding,
            "34S": fielder_ratings + canned_if_fielding,
            "34": fielder_ratings + canned_if_fielding
        }
    elif position == 4:
        return {
            "34D": canned_if_fielding + fielder_ratings,
            "34S": canned_if_fielding + fielder_ratings,
            "34": canned_if_fielding + fielder_ratings,
            "4MD": fielder_ratings,
            "4M": fielder_ratings,
            "4MS": fielder_ratings,
            "4": fielder_ratings,
            "4D": fielder_ratings,
            "4S": fielder_ratings
        }
    elif position == 5:
        return {
            "25": canned_if_fielding + fielder_ratings,
            "5D": fielder_ratings,
            "5S": fielder_ratings,
            "5L": fielder_ratings,
            "5": fielder_ratings,
            "56D": fielder_ratings + canned_if_fielding,
            "56S": fielder_ratings + canned_if_fielding,
            "56": fielder_ratings + canned_if_fielding
        }
    elif position == 6:
        return {
            "56D": canned_if_fielding + fielder_ratings,
            "56S": canned_if_fielding + fielder_ratings,
            "56": canned_if_fielding + fielder_ratings,
            "6MD": fielder_ratings,
            "6D": fielder_ratings,
            "6S": fielder_ratings,
            "6MS": fielder_ratings,
            "6": fielder_ratings,
            "6M": fielder_ratings
        }
    elif position == 7:
        return {
            "7S": fielder_ratings,
            "7LM": fielder_ratings,
            "7LS": fielder_ratings,
            "7": fielder_ratings,
            "7LD": fielder_ratings,
            "7D": fielder_ratings,
            "78S": fielder_ratings + canned_of_fielding,
            "78M": fielder_ratings + canned_of_fielding,
            "78D": fielder_ratings + canned_of_fielding,
            "78XD": fielder_ratings + canned_of_fielding
        }
    elif position == 8:
        return {
            "78S": canned_of_fielding + fielder_ratings,
            "78M": canned_of_fielding + fielder_ratings,
            "78D": canned_of_fielding + fielder_ratings,
            "78XD": canned_of_fielding + fielder_ratings,
            "8LS": fielder_ratings,
            "8RS": fielder_ratings,
            "8LM": fielder_ratings,
            "8RM": fielder_ratings,
            "8RXD": fielder_ratings,
            "8LD": fielder_ratings,
            "8RD": fielder_ratings,
            "8LXD": fielder_ratings,
            "89S": fielder_ratings + canned_of_fielding,
            "89M": fielder_ratings + canned_of_fielding,
            "89D": fielder_ratings + canned_of_fielding,
            "89XD": fielder_ratings + canned_of_fielding
        }
    elif position == 9:
        return {
            "89S": canned_of_fielding + fielder_ratings,
            "89M": canned_of_fielding + fielder_ratings,
            "89D": canned_of_fielding + fielder_ratings,
            "89XD": canned_of_fielding + fielder_ratings,
            "9S": fielder_ratings,
            "9LS": fielder_ratings,
            "9LM": fielder_ratings,
            "9": fielder_ratings,
            "9LD": fielder_ratings,
            "9D": fielder_ratings
        }

    print(position, "unrecognized position for finding position_to_location_defenses")
    exit()

def __parse_error__(error_pos: str) -> List[int]:
    if error_pos == "":
        return []
    elif error_pos == "E9":
        return [9]
    elif error_pos == "E8":
        return [8]
    elif error_pos == "E7":
        return [7]

    print(error_pos, "unrecognized error position")
    exit()


@dataclass
class FielderPlayer:
    player: CardPlayer
    position: int

def find_fielders_for_play(lineup: BoxScoreLineup, loc: str, error_pos: str = "") -> List[FielderPlayer]:
    loc_fielders = __parse_batted_ball_location__(loc)
    error_fielders = __parse_error__(error_pos)
    fielding_positions = __parse_batted_ball_location__(loc)
    if len(loc_fielders) == len(error_fielders) and error_fielders[0] < 7 == loc_fielders[0] < 7:
        fielding_positions = error_fielders
    fielders = []
    for pos in fielding_positions:
        if pos > 1:
            if lineup.lineup[pos] == None:
                return []
            fielders.append(FielderPlayer(
                player=lineup.lineup[pos].player.card_player,
                position=pos
            ))
    return fielders