
from typing import Callable, List, Tuple

from projection.projected_batter import ProjectedBatter
from projection.projected_pitcher import ProjectedStarter, ProjectedReliever


proj_batter_headers: List[Tuple[str, Callable[[ProjectedBatter], any]]] = [
    ["cid", lambda x: x.card_player.cid],
    ["full_title", lambda x: x.card_player.full_title],
    ["position", lambda x: x.position],
    ["team", lambda x: x.card_player.team],
    ["year", lambda x: int(x.card_player.year)],
    ["ovr", lambda x: int(x.card_player.ovr)],
    ["bats", lambda x: x.card_player.bats],
    ["throws", lambda x: x.card_player.throws],
    ["con", lambda x: int(x.card_player.con_ovr)],
    ["gap", lambda x: int(x.card_player.gap_ovr)],
    ["pow", lambda x: int(x.card_player.pow_ovr)],
    ["eye", lambda x: int(x.card_player.eye_ovr)],
    ["avk", lambda x: int(x.card_player.avk_ovr)],
    ["babip", lambda x: int(x.card_player.babip_ovr)],
    ["cx", lambda x: int(x.card_player.defensec)],
    ["1bx", lambda x: int(x.card_player.defense1b)],
    ["2bx", lambda x: int(x.card_player.defense2b)],
    ["3bx", lambda x: int(x.card_player.defense3b)],
    ["ssx", lambda x: int(x.card_player.defensess)],
    ["lfx", lambda x: int(x.card_player.defenself)],
    ["cfx", lambda x: int(x.card_player.defensecf)],
    ["rfx", lambda x: int(x.card_player.defenserf)],
    ["singles_vl", lambda x: float(x.singles_vl)],
    ["singles_vr", lambda x: float(x.singles_vr)],
    ["doubles_vl", lambda x: float(x.doubles_vl)],
    ["doubles_vr", lambda x: float(x.doubles_vr)],
    ["triples_vl", lambda x: float(x.triples_vl)],
    ["triples_vr", lambda x: float(x.triples_vr)],
    ["homeruns_vl", lambda x: float(x.homeruns_vl)],
    ["homeruns_vr", lambda x: float(x.homeruns_vr)],
    ["walks_vl", lambda x: float(x.walks_vl)],
    ["walks_vr", lambda x: float(x.walks_vr)],
    ["strikeouts_vl", lambda x: float(x.strikeouts_vl)],
    ["strikeouts_vr", lambda x: float(x.strikeouts_vr)],
    ["BABIP_vl", lambda x: float((x.singles_vl + x.doubles_vl + x.triples_vl) / (720 - x.strikeouts_vl - x.homeruns_vl - x.walks_vl))],
    ["BABIP_vr", lambda x: float((x.singles_vr + x.doubles_vr + x.triples_vr) / (720 - x.strikeouts_vr - x.homeruns_vr - x.walks_vr))],
    ["wOBA_vl", lambda x: float(x.woba_vl)],
    ["wOBA_vr", lambda x: float(x.woba_vr)],
    ["wSB_vl", lambda x: float(x.wsb_vl)],
    ["wSB_vr", lambda x: float(x.wsb_vr)],
    ["UBR_vl", lambda x: float(x.ubr_vl)],
    ["UBR_vr", lambda x: float(x.ubr_vr)],
    ["Fielding Runs", lambda x: float(x.fielding_runs)],
    ["WAR", lambda x: float(x.war_ovr)],
    ["WAR vL" , lambda x: float(x.war_vl)],
    ["WAR vR", lambda x: float(x.war_vr)]
]
proj_batter_hidden_cols = [
    "throws",
    "con",
    "gap",
    "pow",
    "eye",
    "avk",
    "babip",
    "singles_vl",
    "singles_vr",
    "doubles_vl",
    "doubles_vr",
    "triples_vl",
    "triples_vr",
    "homeruns_vl",
    "homeruns_vr",
    "walks_vl",
    "walks_vr",
    "strikeouts_vl",
    "strikeouts_vr",
    "BABIP_vl",
    "BABIP_vr"
]

proj_starter_headers: List[Tuple[str, Callable[[ProjectedStarter], any]]] = [
    ["cid", lambda x: x.card_player.cid],
    ["full_title", lambda x: x.card_player.full_title],
    ["team", lambda x: x.card_player.team],
    ["year", lambda x: int(x.card_player.year)],
    ["ovr", lambda x: int(x.card_player.ovr)],
    ["bats", lambda x: x.card_player.bats],
    ["throws", lambda x: x.card_player.throws],
    ["stu", lambda x: int(x.card_player.stu_ovr)],
    ["mov", lambda x: int(x.card_player.mov_ovr)],
    ["ctl", lambda x: int(x.card_player.ctl_ovr)],
    ["stm", lambda x: int(x.card_player.stamina)],
    ["bf", lambda x: float(x.bf)],
    ["k/9", lambda x: float(x.k_per_9)],
    ["bb + hbp/9", lambda x: float(x.bb_per_9)],
    ["hr/9", lambda x: float(x.hr_per_9)],
    ["ip/g", lambda x: float(x.ip_per_g)],
    ["fip", lambda x: float(x.fip)],
    ["war", lambda x: float(x.war)],
    ["war_with_relief", lambda x: float(x.war_with_relief)]
]

proj_reliever_headers: List[Tuple[str, Callable[[ProjectedReliever], any]]] = [
    ["cid", lambda x: x.card_player.cid],
    ["full_title", lambda x: x.card_player.full_title],
    ["team", lambda x: x.card_player.team],
    ["year", lambda x: int(x.card_player.year)],
    ["ovr", lambda x: int(x.card_player.ovr)],
    ["bats", lambda x: x.card_player.bats],
    ["throws", lambda x: x.card_player.throws],
    ["stu", lambda x: int(x.card_player.stu_ovr)],
    ["mov", lambda x: int(x.card_player.mov_ovr)],
    ["ctl", lambda x: int(x.card_player.ctl_ovr)],
    ["stm", lambda x: int(x.card_player.stamina)],
    ["bf", lambda x: float(x.bf)],
    ["k/9_vl", lambda x: float(x.k_per_9_vl)],
    ["k/9_vr", lambda x: float(x.k_per_9_vr)],
    ["bb + hbp/9_vl", lambda x: float(x.bb_per_9_vl)],
    ["bb + hbp/9_vr", lambda x: float(x.bb_per_9_vr)],
    ["hr/9_vl", lambda x: float(x.hr_per_9_vl)],
    ["hr/9_vr", lambda x: float(x.hr_per_9_vr)],
    ["ip/g_vl", lambda x: float(x.ip_per_g_vl)],
    ["ip/g_vr", lambda x: float(x.ip_per_g_vr)],
    ["fip_vl", lambda x: float(x.fip_vl)],
    ["fip_vr", lambda x: float(x.fip_vr)],
    ["war_vl", lambda x: float(x.war_vl)],
    ["war_vr", lambda x: float(x.war_vr)],
    ["war_ovr", lambda x: float(x.war_ovr)],
]