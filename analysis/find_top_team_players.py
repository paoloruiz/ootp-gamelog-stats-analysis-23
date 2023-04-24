from dataclasses import dataclass
from typing import Dict, List, Tuple
from game_log.play import BattingPlay
from tournament.load_tourney_plays import load_top_team_tournament_plays

@dataclass
class TeamBreakdown:
    vl_starts: int
    vr_starts: int
    catching_player_abi: Tuple[int, int]
    bats_nums: Dict[str, Dict[str, int]]
    bat_stat_nums: Dict[str, Dict[str, Dict[str, Dict[str, Dict[str, Tuple[int, int]]]]]]
    pitch_nums: Dict[str, Dict[str, int]]
    pitch_stat_nums: Dict[str, Dict[str, Dict[str, Dict[str, Dict[str, Tuple[int, int]]]]]]
    speeds: Dict[str, Tuple[int, int]]

    def get_cabi(self) -> float:
        return self.catching_player_abi[0] / self.catching_player_abi[1]

    def get_speed(self, throws: str) -> float:
        return self.speeds[throws][0] / self.speeds[throws][1]

def get_rating_level(rating: int):
    if rating < 50:
        return "low"
    
    if rating < 100:
        return "high"

    return "super"

def find_top_team_players(ttype: str) -> TeamBreakdown:
    vl_starts = 0
    vr_starts = 0

    catching_player_abi: Tuple[int, int] = (0, 0)

    bats_nums: Dict[str, Dict[str, int]] = {}

    possible_throws = ["L", "R"]
    possible_bats = ["L", "R", "S"]

    # Starting pitcher
    for t in possible_throws:
        bats_nums[t] = {}
        # Which bats they face
        for b in possible_bats:
            bats_nums[t][b] = 0

    bat_attrs = ["pow", "avk", "gap", "bab", "eye"]

    bat_stat_nums: Dict[str, Dict[str, Dict[str, Dict[str, Dict[str, Tuple[int, int]]]]]] = {}

    # Starting pitcher
    for t in possible_throws:
        bat_stat_nums[t] = {}
        # Current pitcher arm
        for cur_t in possible_throws:
            bat_stat_nums[t][cur_t] = {}
            # Which bats they face
            for b in possible_bats:
                bat_stat_nums[t][cur_t][b] = {}
                # Batting attributes
                for b_attr in bat_attrs:
                    bat_stat_nums[t][cur_t][b][b_attr] = {
                        "low": (0, 0),
                        "high": (0, 0),
                        "super": (0, 0)
                    }

    pitch_nums: Dict[str, Dict[str, int]] = {}

    # Starting pitcher
    for t in possible_throws:
        pitch_nums[t] = {}
        # Current pitcher for team
        for cur_t in possible_throws:
            pitch_nums[t][cur_t] = 0

    pit_attrs = ["stu", "mov", "ctl"]

    pitch_stat_nums: Dict[str, Dict[str, Dict[str, Dict[str, Dict[str, Tuple[int, int]]]]]] = {}

    # Starting pitcher
    for t in possible_throws:
        pitch_stat_nums[t] = {}
        # Current pitcher
        for cur_t in possible_throws:
            pitch_stat_nums[t][cur_t] = {}
            # Batter
            for b in possible_bats:
                pitch_stat_nums[t][cur_t][b] = {}
                # Attributes
                for p_attr in pit_attrs:
                    pitch_stat_nums[t][cur_t][b][p_attr] = {
                        "low": (0, 0),
                        "high": (0, 0),
                        "super": (0, 0)
                    }

    # Starting pitcher
    speeds: Dict[str, Tuple[int, int]] = {
        "L": (0, 0),
        "R": (0, 0)
    }

    games: List[List[BattingPlay]] = load_top_team_tournament_plays(ttype)

    for game in games:
        tm1 = game[0].cur_team

        tm1_plays = list(filter(lambda p: p.cur_team == tm1, game))
        tm2_plays = list(filter(lambda p: p.cur_team != tm1, game))
        if tm1_plays[0].pitching_player.throws == "L":
            vl_starts += 1
        else:
            vr_starts += 1
        if tm2_plays[0].pitching_player.throws == "L":
            vl_starts += 1
        else:
            vr_starts += 1

        tm1_starter_throws = tm1_plays[0].pitching_player.throws
        tm2_starter_throws = tm2_plays[0].pitching_player.throws

        for play in tm1_plays:
            bats_nums[tm1_starter_throws][play.batting_player.bats] += 1
            pitch_nums[tm1_starter_throws][play.pitching_player.throws] += 1

            pow_rat = play.batting_player.pow_vl if play.pitching_player.throws == "L" else play.batting_player.pow_vr
            pow_rat_lvl = get_rating_level(pow_rat)
            tup = bat_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["pow"][pow_rat_lvl]
            bat_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["pow"][pow_rat_lvl] = (tup[0] + pow_rat, tup[1] + 1)
            eye_rat = play.batting_player.eye_vl if play.pitching_player.throws == "L" else play.batting_player.eye_vr
            eye_rat_lvl = get_rating_level(eye_rat)
            tup = bat_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["eye"][eye_rat_lvl]
            bat_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["eye"][eye_rat_lvl] = (tup[0] + eye_rat, tup[1] + 1)
            bab_rat = play.batting_player.babip_vl if play.pitching_player.throws == "L" else play.batting_player.babip_vr
            bab_rat_lvl = get_rating_level(bab_rat)
            tup = bat_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["bab"][bab_rat_lvl]
            bat_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["bab"][bab_rat_lvl] = (tup[0] + bab_rat, tup[1] + 1)
            gap_rat = play.batting_player.gap_vl if play.pitching_player.throws == "L" else play.batting_player.gap_vr
            gap_rat_lvl = get_rating_level(gap_rat)
            tup = bat_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["gap"][gap_rat_lvl]
            bat_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["gap"][gap_rat_lvl] = (tup[0] + gap_rat, tup[1] + 1)
            avk_rat = play.batting_player.avk_vl if play.pitching_player.throws == "L" else play.batting_player.avk_vr
            avk_rat_lvl = get_rating_level(avk_rat)
            tup = bat_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["avk"][avk_rat_lvl]
            bat_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["avk"][avk_rat_lvl] = (tup[0] + avk_rat, tup[1] + 1)
            
            is_vl_rating = (play.pitching_player.throws == "R" and play.batting_player.bats == "S") or play.batting_player.bats == "L"
            stu_rat = play.pitching_player.stu_vl if is_vl_rating else play.pitching_player.stu_vr
            stu_rat_lvl = get_rating_level(stu_rat)
            tup = pitch_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["stu"][stu_rat_lvl]
            pitch_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["stu"][stu_rat_lvl] = (tup[0] + stu_rat, tup[1] + 1)
            mov_rat = play.pitching_player.mov_vl if is_vl_rating else play.pitching_player.mov_vr
            mov_rat_lvl = get_rating_level(mov_rat)
            tup = pitch_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["mov"][mov_rat_lvl]
            pitch_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["mov"][mov_rat_lvl] = (tup[0] + mov_rat, tup[1] + 1)
            ctl_rat = play.pitching_player.ctl_vl if is_vl_rating else play.pitching_player.ctl_vr
            ctl_rat_lvl = get_rating_level(ctl_rat)
            tup = pitch_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["ctl"][ctl_rat_lvl]
            pitch_stat_nums[tm1_starter_throws][play.pitching_player.throws][play.batting_player.bats]["ctl"][ctl_rat_lvl] = (tup[0] + ctl_rat, tup[1] + 1)

            catching_player_abi = (catching_player_abi[0] + play.catcher_player.cabi, catching_player_abi[1] + 1)
            speeds[tm1_starter_throws] = (speeds[tm1_starter_throws][0] + play.batting_player.speed, speeds[tm1_starter_throws][1] + 1)

        for play in tm2_plays:
            bats_nums[tm2_starter_throws][play.batting_player.bats] += 1
            pitch_nums[tm2_starter_throws][play.pitching_player.throws] += 1

            pow_rat = play.batting_player.pow_vl if play.pitching_player.throws == "L" else play.batting_player.pow_vr
            pow_rat_lvl = get_rating_level(pow_rat)
            tup = bat_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["pow"][pow_rat_lvl]
            bat_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["pow"][pow_rat_lvl] = (tup[0] + pow_rat, tup[1] + 1)
            eye_rat = play.batting_player.eye_vl if play.pitching_player.throws == "L" else play.batting_player.eye_vr
            eye_rat_lvl = get_rating_level(eye_rat)
            tup = bat_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["eye"][eye_rat_lvl]
            bat_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["eye"][eye_rat_lvl] = (tup[0] + eye_rat, tup[1] + 1)
            bab_rat = play.batting_player.babip_vl if play.pitching_player.throws == "L" else play.batting_player.babip_vr
            bab_rat_lvl = get_rating_level(bab_rat)
            tup = bat_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["bab"][bab_rat_lvl]
            bat_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["bab"][bab_rat_lvl] = (tup[0] + bab_rat, tup[1] + 1)
            gap_rat = play.batting_player.gap_vl if play.pitching_player.throws == "L" else play.batting_player.gap_vr
            gap_rat_lvl = get_rating_level(gap_rat)
            tup = bat_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["gap"][gap_rat_lvl]
            bat_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["gap"][gap_rat_lvl] = (tup[0] + gap_rat, tup[1] + 1)
            avk_rat = play.batting_player.avk_vl if play.pitching_player.throws == "L" else play.batting_player.avk_vr
            avk_rat_lvl = get_rating_level(avk_rat)
            tup = bat_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["avk"][avk_rat_lvl]
            bat_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["avk"][avk_rat_lvl] = (tup[0] + avk_rat, tup[1] + 1)
            
            is_vl_rating = (play.pitching_player.throws == "R" and play.batting_player.bats == "S") or play.batting_player.bats == "L"
            stu_rat = play.pitching_player.stu_vl if is_vl_rating else play.pitching_player.stu_vr
            stu_rat_lvl = get_rating_level(stu_rat)
            tup = pitch_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["stu"][stu_rat_lvl]
            pitch_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["stu"][stu_rat_lvl] = (tup[0] + stu_rat, tup[1] + 1)
            mov_rat = play.pitching_player.mov_vl if is_vl_rating else play.pitching_player.mov_vr
            mov_rat_lvl = get_rating_level(mov_rat)
            tup = pitch_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["mov"][mov_rat_lvl]
            pitch_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["mov"][mov_rat_lvl] = (tup[0] + mov_rat, tup[1] + 1)
            ctl_rat = play.pitching_player.ctl_vl if is_vl_rating else play.pitching_player.ctl_vr
            ctl_rat_lvl = get_rating_level(ctl_rat)
            tup = pitch_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["ctl"][ctl_rat_lvl]
            pitch_stat_nums[tm2_starter_throws][play.pitching_player.throws][play.batting_player.bats]["ctl"][ctl_rat_lvl] = (tup[0] + ctl_rat, tup[1] + 1)

            catching_player_abi = (catching_player_abi[0] + play.catcher_player.cabi, catching_player_abi[1] + 1)
            speeds[tm2_starter_throws] = (speeds[tm2_starter_throws][0] + play.batting_player.speed, speeds[tm2_starter_throws][1] + 1)

    return TeamBreakdown(
        vl_starts=vl_starts,
        vr_starts=vr_starts,
        catching_player_abi=catching_player_abi,
        bats_nums=bats_nums,
        bat_stat_nums=bat_stat_nums,
        pitch_nums=pitch_nums,
        pitch_stat_nums=pitch_stat_nums,
        speeds=speeds
    )
        

    