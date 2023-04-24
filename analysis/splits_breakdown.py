from dataclasses import dataclass, field
from typing import Dict, List, Tuple

from game_log.play import BattingPlay
from util.breakpoints import HIGH_BREAKPOINT, MID_BREAKPOINT

def __average__(lst: List[int]) -> float:
    if len(lst) == 0:
        return 0

    return sum(lst) / len(lst)

@dataclass
class HLStat:
    sh_stat: List[int] = field(default_factory=list)
    h_stat: List[int] = field(default_factory=list)
    l_stat: List[int] = field(default_factory=list)

    def record(self, st: int):
        if st >= HIGH_BREAKPOINT:
            self.sh_stat.append(st)
        elif st >= MID_BREAKPOINT:
            self.h_stat.append(st)
        else:
            self.l_stat.append(st)

    def __get_sh_breakdown__(self) -> Tuple[int, float]:
        return (len(self.sh_stat), __average__(self.sh_stat))

    def __get_h_breakdown__(self) -> Tuple[int, float]:
        return (len(self.h_stat), __average__(self.h_stat))

    def __get_l_breakdown__(self) -> Tuple[int, float]:
        return (len(self.l_stat), __average__(self.l_stat))


@dataclass
class BatterStatBreakdown:
    avk: HLStat = HLStat()
    gap: HLStat = HLStat()
    pow: HLStat = HLStat()
    eye: HLStat = HLStat()
    bab: HLStat = HLStat()
    gbt: Dict[int, int] = field(default_factory=dict)
    fbt: Dict[int, int] = field(default_factory=dict)
    bbt: Dict[int, int] = field(default_factory=dict)

    def record(self, play: BattingPlay, is_vl: bool):
        if play.batting_player.gb_hit_type not in self.gbt:
            self.gbt[play.batting_player.gb_hit_type] = 0
        if play.batting_player.fb_hit_type not in self.fbt:
            self.fbt[play.batting_player.fb_hit_type] = 0
        if play.batting_player.batted_ball_type not in self.bbt:
            self.bbt[play.batting_player.batted_ball_type] = 0
        self.gbt[play.batting_player.gb_hit_type] += 1
        self.fbt[play.batting_player.fb_hit_type] += 1
        self.bbt[play.batting_player.batted_ball_type] += 1
        if is_vl:
            self.avk.record(play.batting_player.avk_vl)
            self.gap.record(play.batting_player.gap_vl)
            self.pow.record(play.batting_player.pow_vl)
            self.eye.record(play.batting_player.eye_vl)
            self.bab.record(play.batting_player.babip_vl)
        else:
            self.avk.record(play.batting_player.avk_vr)
            self.gap.record(play.batting_player.gap_vr)
            self.pow.record(play.batting_player.pow_vr)
            self.eye.record(play.batting_player.eye_vr)
            self.bab.record(play.batting_player.babip_vr)

    def __get_avk_breakdown__(self) -> List[Tuple[int, float]]:
        return [self.avk.__get_sh_breakdown__(), self.avk.__get_h_breakdown__(), self.avk.__get_l_breakdown__()]

    def __get_gap_breakdown__(self) -> List[Tuple[int, float]]:
        return [self.gap.__get_sh_breakdown__(), self.gap.__get_h_breakdown__(), self.gap.__get_l_breakdown__()]

    def __get_pow_breakdown__(self) -> List[Tuple[int, float]]:
        return [self.pow.__get_sh_breakdown__(), self.pow.__get_h_breakdown__(), self.pow.__get_l_breakdown__()]

    def __get_eye_breakdown__(self) -> List[Tuple[int, float]]:
        return [self.eye.__get_sh_breakdown__(), self.eye.__get_h_breakdown__(), self.eye.__get_l_breakdown__()]

    def __get_bab_breakdown__(self) -> List[Tuple[int, float]]:
        return [self.bab.__get_sh_breakdown__(), self.bab.__get_h_breakdown__(), self.bab.__get_l_breakdown__()]

    def __get_gbt_breakdown__(self) -> List[Tuple[int, float]]:
        d = []
        for gb_type in self.gbt.keys():
            d.append((self.gbt[gb_type], gb_type))
        return d

    def __get_fbt_breakdown__(self) -> List[Tuple[int, float]]:
        d = []
        for fb_type in self.fbt.keys():
            d.append((self.fbt[fb_type], fb_type))
        return d

    def __get_bbt_breakdown__(self) -> List[Tuple[int, float]]:
        d = []
        for bb_type in self.bbt.keys():
            d.append((self.bbt[bb_type], bb_type))
        return d

@dataclass
class PitcherStatBreakdown:
    stu: HLStat = HLStat()
    mov: HLStat = HLStat()
    ctl: HLStat = HLStat()
    gbp: Dict[int, int] = field(default_factory=dict)

    def record(self, play: BattingPlay, is_vl: bool):
        if play.pitching_player.gb_type not in self.gbp:
            self.gbp[play.pitching_player.gb_type] = 0
        self.gbp[play.pitching_player.gb_type] += 1
        if is_vl:
            self.stu.record(play.pitching_player.stu_vl)
            self.mov.record(play.pitching_player.mov_vl)
            self.ctl.record(play.pitching_player.ctl_vl)
        else:
            self.stu.record(play.pitching_player.stu_vr)
            self.mov.record(play.pitching_player.mov_vr)
            self.ctl.record(play.pitching_player.ctl_vr)

    def __get_stu_breakdown__(self) -> List[Tuple[int, float]]:
        return [self.stu.__get_sh_breakdown__(), self.stu.__get_h_breakdown__(), self.stu.__get_l_breakdown__()]

    def __get_mov_breakdown__(self) -> List[Tuple[int, float]]:
        return [self.mov.__get_sh_breakdown__(), self.mov.__get_h_breakdown__(), self.mov.__get_l_breakdown__()]

    def __get_ctl_breakdown__(self) -> List[Tuple[int, float]]:
        return [self.ctl.__get_sh_breakdown__(), self.ctl.__get_h_breakdown__(), self.ctl.__get_l_breakdown__()]

    def __get_gbp_breakdown__(self) -> List[Tuple[int, float]]:
        d = []
        for gb_type in self.gbp.keys():
            d.append((self.gbp[gb_type], gb_type))
        return d


@dataclass
class SplitsBreakdown:
    pitcher: Dict[str, Dict[str, BatterStatBreakdown]] = field(default_factory=dict)
    batter: Dict[str, Dict[str, PitcherStatBreakdown]] = field(default_factory=dict)

    def init(self):
        self.pitcher["L"] = {
            "R": BatterStatBreakdown(),
            "L": BatterStatBreakdown(),
            "S": BatterStatBreakdown()
        }
        self.pitcher["R"] = {
            "R": BatterStatBreakdown(),
            "L": BatterStatBreakdown(),
            "S": BatterStatBreakdown()
        }
        self.batter["L"] = {
            "R": PitcherStatBreakdown(),
            "L": PitcherStatBreakdown()
        }
        self.batter["R"] = {
            "R": PitcherStatBreakdown(),
            "L": PitcherStatBreakdown()
        }
        self.batter["S"] = {
            "R": PitcherStatBreakdown(),
            "L": PitcherStatBreakdown()
        }

    def record(self, play: BattingPlay):
        self.pitcher[play.pitching_player.throws][play.batting_player.bats].record(play, is_vl=play.pitching_player.throws == "L")
        self.batter[play.batting_player.bats][play.pitching_player.throws].record(play, is_vl=play.batting_player.bats == "L" or (play.pitching_player.throws == "R" and play.batting_player.bats == "S"))

    def get_breakdown_pitcher_avk_against(self, throws: str) -> Dict[str, List[Tuple[float, float]]]:
        r_against: List[Tuple[int, float]] = self.pitcher[throws]["R"].__get_avk_breakdown__()
        r_tot = sum(map(lambda b: b[0], r_against))
        l_against: List[Tuple[int, float]] = self.pitcher[throws]["L"].__get_avk_breakdown__()
        l_tot = sum(map(lambda b: b[0], l_against))
        s_against: List[Tuple[int, float]] = self.pitcher[throws]["S"].__get_avk_breakdown__()
        s_tot = sum(map(lambda b: b[0], s_against))

        tot_evnt = r_tot + l_tot + s_tot
        r_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), r_against))
        l_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), l_against))
        s_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), s_against))
        return {
            "R": r_rate_against,
            "L": l_rate_against,
            "S": s_rate_against
        }

    def get_breakdown_pitcher_pow_against(self, throws: str) -> Dict[str, List[Tuple[float, float]]]:
        r_against: List[Tuple[int, float]] = self.pitcher[throws]["R"].__get_pow_breakdown__()
        r_tot = sum(map(lambda b: b[0], r_against))
        l_against: List[Tuple[int, float]] = self.pitcher[throws]["L"].__get_pow_breakdown__()
        l_tot = sum(map(lambda b: b[0], l_against))
        s_against: List[Tuple[int, float]] = self.pitcher[throws]["S"].__get_pow_breakdown__()
        s_tot = sum(map(lambda b: b[0], s_against))

        tot_evnt = r_tot + l_tot + s_tot
        r_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), r_against))
        l_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), l_against))
        s_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), s_against))
        return {
            "R": r_rate_against,
            "L": l_rate_against,
            "S": s_rate_against
        }

    def get_breakdown_pitcher_eye_against(self, throws: str) -> Dict[str, List[Tuple[float, float]]]:
        r_against: List[Tuple[int, float]] = self.pitcher[throws]["R"].__get_eye_breakdown__()
        r_tot = sum(map(lambda b: b[0], r_against))
        l_against: List[Tuple[int, float]] = self.pitcher[throws]["L"].__get_eye_breakdown__()
        l_tot = sum(map(lambda b: b[0], l_against))
        s_against: List[Tuple[int, float]] = self.pitcher[throws]["S"].__get_eye_breakdown__()
        s_tot = sum(map(lambda b: b[0], s_against))

        tot_evnt = r_tot + l_tot + s_tot
        r_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), r_against))
        l_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), l_against))
        s_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), s_against))
        return {
            "R": r_rate_against,
            "L": l_rate_against,
            "S": s_rate_against
        }

    def get_breakdown_pitcher_bab_against(self, throws: str) -> Dict[str, List[Tuple[float, float]]]:
        r_against: List[Tuple[int, float]] = self.pitcher[throws]["R"].__get_bab_breakdown__()
        r_tot = sum(map(lambda b: b[0], r_against))
        l_against: List[Tuple[int, float]] = self.pitcher[throws]["L"].__get_bab_breakdown__()
        l_tot = sum(map(lambda b: b[0], l_against))
        s_against: List[Tuple[int, float]] = self.pitcher[throws]["S"].__get_bab_breakdown__()
        s_tot = sum(map(lambda b: b[0], s_against))

        tot_evnt = r_tot + l_tot + s_tot
        r_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), r_against))
        l_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), l_against))
        s_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), s_against))
        return {
            "R": r_rate_against,
            "L": l_rate_against,
            "S": s_rate_against
        }

    def get_breakdown_batter_stu_against(self, bats: str) -> Dict[str, List[Tuple[float, float]]]:
        r_against: List[Tuple[int, float]] = self.batter[bats]["R"].__get_stu_breakdown__()
        r_tot = sum(map(lambda b: b[0], r_against))
        l_against: List[Tuple[int, float]] = self.batter[bats]["L"].__get_stu_breakdown__()
        l_tot = sum(map(lambda b: b[0], l_against))

        tot_evnt = r_tot + l_tot
        r_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), r_against))
        l_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), l_against))
        return {
            "R": r_rate_against,
            "L": l_rate_against
        }

    def get_breakdown_batter_mov_against(self, bats: str) -> Dict[str, List[Tuple[float, float]]]:
        r_against: List[Tuple[int, float]] = self.batter[bats]["R"].__get_mov_breakdown__()
        r_tot = sum(map(lambda b: b[0], r_against))
        l_against: List[Tuple[int, float]] = self.batter[bats]["L"].__get_mov_breakdown__()
        l_tot = sum(map(lambda b: b[0], l_against))

        tot_evnt = r_tot + l_tot
        r_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), r_against))
        l_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), l_against))
        return {
            "R": r_rate_against,
            "L": l_rate_against
        }

    def get_breakdown_batter_ctl_against(self, bats: str) -> Dict[str, List[Tuple[float, float]]]:
        r_against: List[Tuple[int, float]] = self.batter[bats]["R"].__get_ctl_breakdown__()
        r_tot = sum(map(lambda b: b[0], r_against))
        l_against: List[Tuple[int, float]] = self.batter[bats]["L"].__get_ctl_breakdown__()
        l_tot = sum(map(lambda b: b[0], l_against))

        tot_evnt = r_tot + l_tot
        r_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), r_against))
        l_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), l_against))
        return {
            "R": r_rate_against,
            "L": l_rate_against
        }

    def get_breakdown_batter_gb_type_against(self, bats: str) -> Dict[str, List[Tuple[float, float]]]:
        r_against: List[Tuple[int, float]] = self.batter[bats]["R"].__get_gbp_breakdown__()
        r_tot = sum(map(lambda b: b[0], r_against))
        l_against: List[Tuple[int, float]] = self.batter[bats]["L"].__get_gbp_breakdown__()
        l_tot = sum(map(lambda b: b[0], l_against))

        tot_evnt = r_tot + l_tot
        r_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), r_against))
        l_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), l_against))
        return {
            "R": r_rate_against,
            "L": l_rate_against
        }

    def get_breakdown_pitcher_gb_type_against(self, throws: str) -> Dict[str, List[Tuple[float, float]]]:
        r_against: List[Tuple[int, float]] = self.pitcher[throws]["R"].__get_gbt_breakdown__()
        r_tot = sum(map(lambda b: b[0], r_against))
        l_against: List[Tuple[int, float]] = self.pitcher[throws]["L"].__get_gbt_breakdown__()
        l_tot = sum(map(lambda b: b[0], l_against))
        s_against: List[Tuple[int, float]] = self.pitcher[throws]["S"].__get_gbt_breakdown__()
        s_tot = sum(map(lambda b: b[0], l_against))

        tot_evnt = r_tot + l_tot + s_tot
        r_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), r_against))
        l_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), l_against))
        s_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), s_against))
        return {
            "R": r_rate_against,
            "L": l_rate_against,
            "S": s_rate_against
        }

    def get_breakdown_pitcher_fb_type_against(self, throws: str) -> Dict[str, List[Tuple[float, float]]]:
        r_against: List[Tuple[int, float]] = self.pitcher[throws]["R"].__get_fbt_breakdown__()
        r_tot = sum(map(lambda b: b[0], r_against))
        l_against: List[Tuple[int, float]] = self.pitcher[throws]["L"].__get_fbt_breakdown__()
        l_tot = sum(map(lambda b: b[0], l_against))
        s_against: List[Tuple[int, float]] = self.pitcher[throws]["S"].__get_fbt_breakdown__()
        s_tot = sum(map(lambda b: b[0], l_against))

        tot_evnt = r_tot + l_tot + s_tot
        r_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), r_against))
        l_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), l_against))
        s_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), s_against))
        return {
            "R": r_rate_against,
            "L": l_rate_against,
            "S": s_rate_against
        }

    def get_breakdown_pitcher_bb_type_against(self, throws: str) -> Dict[str, List[Tuple[float, float]]]:
        r_against: List[Tuple[int, float]] = self.pitcher[throws]["R"].__get_bbt_breakdown__()
        r_tot = sum(map(lambda b: b[0], r_against))
        l_against: List[Tuple[int, float]] = self.pitcher[throws]["L"].__get_bbt_breakdown__()
        l_tot = sum(map(lambda b: b[0], l_against))
        s_against: List[Tuple[int, float]] = self.pitcher[throws]["S"].__get_bbt_breakdown__()
        s_tot = sum(map(lambda b: b[0], l_against))

        tot_evnt = r_tot + l_tot + s_tot
        r_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), r_against))
        l_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), l_against))
        s_rate_against = list(map(lambda b: (b[0] / tot_evnt, b[1]), s_against))
        return {
            "R": r_rate_against,
            "L": l_rate_against,
            "S": s_rate_against
        }

