from dataclasses import dataclass, field
from typing import Dict, List
from game_log.play import Play, BattingPlay

@dataclass
class LeaguePlayerStats:
    name: str
    
    cid: str

    pa: int = 0
    ab: int = 0
    hits: int = 0
    singles: int = 0
    doubles: int = 0
    triples: int = 0
    homeruns: int = 0

    bb: int = 0
    ibb: int = 0
    hbp: int = 0
    
    strikeouts: int = 0
    gidp: int = 0
    
    bf: int = 0
    pitcherab: int = 0
    hitsagainst: int = 0
    singlesagainst: int = 0
    doublesagainst: int = 0
    triplesagainst: int = 0
    homerunsagainst: int = 0
    runsagainst: int = 0
    
    bbagainst: int = 0
    ibbagainst: int = 0
    ks: int = 0
    batters_hit: int = 0
    gidpagainst: int = 0

    groundballs: int = 0
    flyballs: int = 0

    def record_batter(self, p: BattingPlay):
        self.pa += 1
        
        if p.baseball_result == "HIT_BY_PITCH":
            self.hbp += 1
        elif p.baseball_result == "INTENTIONAL_WALK":
            self.ibb += 1
            self.bb += 1
        elif p.baseball_result == "STRIKEOUT":
            self.ab += 1
            self.strikeouts += 1
        elif p.baseball_result == "WALK":
            self.bb += 1
        elif p.baseball_result == "SINGLE":
            self.ab += 1
            self.hits += 1
            self.singles += 1
        elif p.baseball_result == "DOUBLE":
            self.ab += 1
            self.hits += 1
            self.doubles += 1
        elif p.baseball_result == "TRIPLE":
            self.ab += 1
            self.hits += 1
            self.triples += 1
        elif p.baseball_result == "HOME_RUN":
            self.ab += 1
            self.hits += 1
            self.homeruns += 1
        elif p.baseball_result == "BIP_OUT":
            self.ab += 1
            if p.game_sub_result == "BUNT_FOR_HIT_DOUBLE_PLAY" or p.game_sub_result == "SAC_BUNT_DP" or p.game_sub_result == "GIDP" or p.game_sub_result == "GITP":
                self.gidp += 1
        elif p.baseball_result == "CATCHERS_INTERFERENCE":
            self.pa -= 1

    def record_pitcher(self, p: BattingPlay):
        self.bf += 1
        
        if p.baseball_result == "HIT_BY_PITCH":
            self.batters_hit += 1
        elif p.baseball_result == "INTENTIONAL_WALK":
            self.ibbagainst += 1
            self.bbagainst += 1
        elif p.baseball_result == "STRIKEOUT":
            self.pitcherab += 1
            self.ks += 1
        elif p.baseball_result == "WALK":
            self.bb += 1
        elif p.baseball_result == "SINGLE":
            self.pitcherab += 1
            self.hitsagainst += 1
            self.singlesagainst += 1
        elif p.baseball_result == "DOUBLE":
            self.pitcherab += 1
            self.hitsagainst += 1
            self.doublesagainst += 1
        elif p.baseball_result == "TRIPLE":
            self.pitcherab += 1
            self.hitsagainst += 1
            self.triplesagainst += 1
        elif p.baseball_result == "HOME_RUN":
            self.pitcherab += 1
            self.hitsagainst += 1
            self.homerunsagainst += 1
        elif p.baseball_result == "BIP_OUT":
            self.pitcherab += 1
            if p.game_sub_result == "BUNT_FOR_HIT_DOUBLE_PLAY" or p.game_sub_result == "SAC_BUNT_DP" or p.game_sub_result == "GIDP" or p.game_sub_result == "GITP":
                self.gidpagainst += 1
        elif p.baseball_result == "CATCHERS_INTERFERENCE":
            self.bf -= 1

        if p.bip_event != None:
            if p.bip_event.batted_ball_type == 1:
                self.groundballs += 1
            elif p.bip_event.batted_ball_type == 3:
                self.flyballs += 1

    def get_sheet_line(self) -> List[str]:
        return [
            self.name,
            self.cid,
            self.pa,
            self.ab,
            self.singles + self.doubles + self.triples + self.homeruns,
            self.singles,
            self.doubles,
            self.triples,
            self.homeruns,
            self.bb,
            self.ibb,
            self.hbp,
            self.strikeouts,
            self.gidp,
            self.bf,
            self.pitcherab,
            self.singlesagainst + self.doublesagainst + self.triplesagainst + self.homerunsagainst,
            self.singlesagainst,
            self.doublesagainst,
            self.triplesagainst,
            self.homerunsagainst,
            self.bbagainst,
            self.ibbagainst,
            self.ks,
            self.batters_hit,
            self.gidpagainst
        ]

@dataclass
class TourneyLeague:
    vl: Dict[str, LeaguePlayerStats] = field(default_factory=dict)
    vr: Dict[str, LeaguePlayerStats] = field(default_factory=dict)

    def read_plays(self, plays: List[Play]):
        batting_plays: List[BattingPlay] = filter(lambda p: p.playtype == "BATTING_PLAY", plays)

        for batting_play in batting_plays:
            batter = batting_play.batting_player
            if batter.cid not in self.vl:
                self.vl[batter.cid] = LeaguePlayerStats(name=batter.name, cid=batter.cid)
            if batter.cid not in self.vr:
                self.vr[batter.cid] = LeaguePlayerStats(name=batter.name, cid=batter.cid)
            
            if batting_play.pitching_player.throws == "L":
                self.vl[batter.cid].record_batter(batting_play)
            else:
                self.vr[batter.cid].record_batter(batting_play)

            pitcher = batting_play.pitching_player
            if pitcher.cid not in self.vl:
                self.vl[pitcher.cid] = LeaguePlayerStats(name=pitcher.name, cid=pitcher.cid)
            if pitcher.cid not in self.vr:
                self.vr[pitcher.cid] = LeaguePlayerStats(name=pitcher.name, cid=pitcher.cid)
                
            if batting_play.batting_player.bats == "R":
                self.vr[pitcher.cid].record_pitcher(batting_play)
            elif batting_play.batting_player.bats == "L":
                self.vl[pitcher.cid].record_pitcher(batting_play)
            else:
                if batting_play.pitching_player.throws == "L":
                    self.vr[pitcher.cid].record_pitcher(batting_play)
                else:
                    self.vl[pitcher.cid].record_pitcher(batting_play)

        

    def get_header_line(self) -> List[str]:
        return [
            "Name",
            "CID",
            "PA",
            "AB",
            "H",
            "1B",
            "2B",
            "3B",
            "HR",
            "BB",
            "IBB",
            "HP",
            "SO",
            "GIDP",
            "BF",
            "AB",
            "HA",
            "1B",
            "2B",
            "3B",
            "HR",
            "BB",
            "IBB",
            "K",
            "HP",
            "DP"
        ]