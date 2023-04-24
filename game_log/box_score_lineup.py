from dataclasses import dataclass, field
from typing import Dict, List

from individual_league.stats_player.base_stats_player import BaseStatsPlayer


@dataclass
class BoxScorePlayer:
    player: BaseStatsPlayer
    cur_position: int
    next_position: List[int]

@dataclass
class BoxScoreLineup:
    filename: str
    lineup: Dict[int, BoxScorePlayer] = field(default_factory=dict)
    pinch_hitters: List[BoxScorePlayer] = field(default_factory=list)
    replacements: List[BoxScorePlayer] = field(default_factory=list)
    pitchers: List[BoxScorePlayer] = field(default_factory=list)

    def __print_lineup__(self):
        for i in self.lineup.keys():
            if self.lineup[i] == None:
                print(i)
            else:
                print(str(i) + "-" + self.lineup[i].player.card_player.name)

    def add_starter(self, player: BaseStatsPlayer, positions: List[int]):
        cur_position = positions[0]
        next_positions = positions[1:]
        self.lineup[cur_position] = BoxScorePlayer(
            player=player,
            cur_position=cur_position,
            next_position=next_positions
        )

    def add_replacement(self, player: BaseStatsPlayer, positions: List[int]):
        self.replacements.append(BoxScorePlayer(
            player=player,
            cur_position=-1,
            next_position=positions
        ))

    def add_pitcher(self, player: BaseStatsPlayer):
        self.pitchers.append(BoxScorePlayer(
            player=player,
            cur_position=-1,
            next_position=[]
        ))

    def __move_batter_from_position__(self, pos: int, c: int = 0):
        old_player = self.lineup[pos]
        if old_player != None and len(old_player.next_position) > 0:
            self.lineup[pos] = None
            self.__move_batter_from_position__(old_player.next_position[0], c=c + 1)
            self.lineup[old_player.next_position[0]] = BoxScorePlayer(
                player=old_player.player,
                cur_position=old_player.next_position[0],
                next_position=old_player.next_position[1:]
            )

    def __replace_batter_from_replacements__(self, name: str, position: int = -2):
        replacements = list(filter(lambda p: p.player.card_player.name == name, self.replacements))
        if len(replacements) != 1:
            raise Exception("Found multiple replacements: " + str(replacements) + " for " + name + " in file " + self.filename)
        
        replacement = replacements[0]
        if position != -2:
            while replacement.next_position[0] != position:
                replacement.next_position = replacement.next_position[1:]

        if replacement.next_position[0] == -1:
            self.pinch_hitters.append(BoxScorePlayer(
                player=replacement.player,
                cur_position=replacement.next_position[0],
                next_position=replacement.next_position[1:]
            ))
        else:
            self.__move_batter_from_position__(replacement.next_position[0])
            self.lineup[replacement.next_position[0]] = BoxScorePlayer(
                player=replacement.player,
                cur_position=replacement.next_position[0],
                next_position=replacement.next_position[1:]
            )
        self.replacements = list(filter(lambda p: p.player.card_player.name != name, self.replacements))

    def __replace_batter_from_pinch_hitters__(self, name: str):
        replacements = list(filter(lambda p: p.player.card_player.name == name, self.pinch_hitters))
        if len(replacements) != 1:
            raise Exception("Found multiple replacements: " + str(replacements) + " for " + name + " in file " + self.filename)
        
        replacement = replacements[0]

        if replacement.next_position[0] == -1:
            self.pinch_hitters.append(BoxScorePlayer(
                player=replacement.player,
                cur_position=replacement.next_position[0],
                next_position=replacement.next_position[1:]
            ))
        else:
            self.__move_batter_from_position__(replacement.next_position[0])
            self.lineup[replacement.next_position[0]] = BoxScorePlayer(
                player=replacement.player,
                cur_position=replacement.next_position[0],
                next_position=replacement.next_position[1:]
            )
        self.pinch_hitters = list(filter(lambda p: p.player.card_player.name != name, self.pinch_hitters))

    def replace_batter(self, name: str):
        if len(list(filter(lambda p: p.player.card_player.name == name, self.pinch_hitters))) == 1:
            self.__replace_batter_from_pinch_hitters__(name)
        else:
            self.__replace_batter_from_replacements__(name)

    def replace_fielder(self, name: str, position: int):
        i = 2
        while i < 10:
            if self.lineup[i] != None and self.lineup[i].player.card_player.name == name:
                break
            i += 1
        if i == 10:
            if len(list(filter(lambda p: p.player.card_player.name == name, self.pinch_hitters))) == 1:
                self.__replace_batter_from_pinch_hitters__(name)
                return
            elif len(list(filter(lambda p: p.player.card_player.name == name, self.replacements))) == 1:
                self.__replace_batter_from_replacements__(name, position=position)
                return
            elif len(list(filter(lambda p: p.player.cid == "no", self.replacements))) > 0:
                self.__move_batter_from_position__(position)
                self.lineup[position] = None
                return
            else:
                raise Exception("Could not replace " + name + " in " + self.filename)
        if len(self.lineup[i].next_position) == 0:
            return
        next_pos = self.lineup[i].next_position[0]
        self.__move_batter_from_position__(next_pos)
        self.lineup[next_pos] = BoxScorePlayer(
            player=self.lineup[i].player,
            cur_position=next_pos,
            next_position=self.lineup[i].next_position[1:]
        )


"""
Name - 2
Name - 3
...
sub - 1 <- inning
Name - 2
sub - 3 <- inning
Name - 9 <- position
...
sub - unknown
Name - 3
"""