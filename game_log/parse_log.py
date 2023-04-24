from dataclasses import dataclass, field
import re
from typing import Dict, List
from cards.card_player import CardPlayer
from game_log.box_score_lineup import BoxScoreLineup
from game_log.game import ManOnBase
from game_log.play import BattingPlay, Play, BIPEvent
from game_log.find_fielders_for_play import find_fielders_for_play
from individual_league.filter_stats_players_by_team import get_player_from_list, get_possible_batters_for_team, get_possible_pitchers_for_team
from individual_league.stats_player.base_stats_player import BaseStatsPlayer
from scraping.box_score_converter import __pos_to_num__

first_play_pattern = re.compile(r"^\[%T\]\tTop of the 1st - (.+) batting - Pitching for (.+) : [LR]HP .+$")
pitching_switch_pattern = re.compile(r"^\[%B\]\tPitching: [LR]HP (.+)$")
batting_switch_pattern = re.compile(r"^\[%B\]\tBatting: [LRS]HB (.+)$")

position_switch_pattern = re.compile(r"^\[%B\]\tNow (at|in) (C|1B|2B|3B|SS|LF|CF|RF): (.+)$")
pinch_hit_pattern = re.compile(r"^\[%B\]\tPinch Hitting: [RLS]HB (.+)$")
pinch_runner_pattern = re.compile(r"^\[%B\]\tPinch Runner at (1st|2nd|3rd) (.+):$")

noop_pattern = re.compile(r"^\[%N\]\t\d-\d: (Called Strike|Swinging Strike|Ball|Foul Ball, location: ..|Bunted foul|Bunt missed!|Foul Ball, location: (\S+), Error on foul ball, ..)$")
balk_pattern = re.compile(r"^\[%N\]\tBalk!$")
wild_pitch_pattern = re.compile(r"^\[%N\]\tWild Pitch!$")
throwing_error_pattern = re.compile(r"^\[%N\]\tThrowing error, (\S+)$")
passed_ball_pattern = re.compile(r"^\[%N\]\tPassed Ball!$")

# play stuff happened
hbp_pattern = re.compile(r"^\[%N\]\t\d-\d: Hit by Pitch$")
strikeout_pattern = re.compile(r"^\[%N\]\t\d-2: Strikes out (swinging|looking)$")
strikeout2_pattern = re.compile(r"^\[%N\]\tBatter strikes out.$")
strikeout_passed_ball_pattern = re.compile(r"^\[%N\]\t\d-2: Strikes out (swinging|looking) passed ball, reaches first!$")
strikeout_wild_pitch_pattern = re.compile(r"^\[%N\]\t\d-2: Strikes out (swinging|looking) wild pitch, reaches first!$")
ibb_pattern = re.compile(r"^\[%N\]\t\d-\d: Intentional Walk$")
walk_pattern = re.compile(r"^\[%N\]\t3-\d: Base on Balls$")
bunt_for_hit_safe_pattern = re.compile(r"^\[%N\]\t\d-\d: Bunt for hit to (\S+) - play at first, batter safe!$")
single_pattern = re.compile(r"^\[%N\]\t\d-\d: SINGLE  \((Groundball|Flyball|Line Drive|Popup), (\S+), .+\)$")
single_rundown_safe_pattern = re.compile(r"^\[%N\]\tSINGLE, rundown, safe at 1st$")
single_rundown_out_pattern = re.compile(r"^\[%N\]\tSINGLE, rundown, out at 1st!$")
single_out_pattern = re.compile(r"^\[%N\]\t\d-\d: SINGLE  \((Groundball|Flyball|Line Drive), (\S+), .+\) - OUT at second base trying to stretch hit.$")
single_out2_pattern = re.compile(r"^\[%N\]\tSINGLE, but batter called out on appeal for missing first base!$")
double_pattern = re.compile(r"^\[%N\]\t\d-\d: DOUBLE  \((Groundball|Flyball|Line Drive|Popup), (\S+), .+\)$")
double_out_pattern = re.compile(r"^\[%N\]\t\d-\d: DOUBLE  \((Groundball|Flyball|Line Drive), (\S+), .+\) - OUT at third base trying to stretch hit.$")
double_from_single_error_pattern = re.compile(r"^\[%N\]\t\d-\d: Single, Error in OF, (\S+), batter to second base \((Groundball|Flyball|Line Drive), (\S+), .+\)$")
triple_pattern = re.compile(r"^\[%N\]\t\d-\d: TRIPLE  \((Groundball|Flyball|Line Drive|Popup), (\S+), .+\)$")
home_run_pattern = re.compile(r"^\[%N\]\t\d-\d:  (SOLO|2-RUN|3-RUN|GRAND SLAM) HOME RUN  \((Flyball|Line Drive), (\S+), .+\),? (Distance : \d+ ft|\(Inside the Park\))$")
strikeout_with_caught_stealing_pattern = re.compile(r"^\[%N\]\t\d-2: Strikes out (swinging|looking), (\S)+ out at first.$")

bip_error_pattern = re.compile(r"^\[%N\]\t\d-\d: Reached on error, (\S+) \((Groundball|Line Drive|Flyball|Popup), (\S+), .+\)$")
bip_error_dropped_throw_pattern = re.compile(r"^\[%N\]\t\d-\d: Reached via error on a dropped throw from (P|C|1B|2B|3B|SS|LF|CF|RF), (\S+) \((Groundball), (\S+), .+\)$")
squeeze_bunt_runner_out_pattern = re.compile(r"^\[%N\]\t\d-\d: Squeeze Bunt to (\S+) - play home, runner OUT, batter safe! (\S+)$")
squeeze_bunt_scores_pattern = re.compile(r"^\[%N\]\t\d-\d: Squeeze Bunt to (\S+) - play home, runner scores, batter safe!$")
squeeze_bunt_scores_out_pattern = re.compile(r"^\[%N\]\t\d-\d: Squeeze Bunt to (\S+) - play at first, runner scores, batter OUT! (\S+)$")
squeeze_bunt_runner_out2_pattern = re.compile(r"^\[%N\]\tSqueeze bunt is on, (.+) is out$")
bunt_for_hit_out_pattern = re.compile(r"^\[%N\]\t\d-\d: Bunt for hit to (\S+) - play at first, batter OUT! (\S+)$")
bunt_for_hit_out2_pattern = re.compile(r"^\[%N\]\t\d-\d: Bunt - Flyout to (\S+)! (\S+)$")
bunt_for_hit_double_play_pattern = re.compile(r"^\[%N\]\t\d-\d: Bunt - Flyout to (\S+) - DP at (second|third)! (\S+)$")
sac_bunt_pattern = re.compile(r"^\[%N\]\t\d-\d: Sac Bunt to (\S+) - play at (first|second|third), (batter|runner) OUT! (\S+)$")
sac_bunt_dp_pattern = re.compile(r"^\[%N\]\t\d-\d: Sac Bunt to (\S+) - play at (first|second|third), (batter|runner) OUT -> throw to (first|second|third), DP!$")
sac_bunt_dp2_pattern = re.compile(r"^\[%N\]\t\d-\d: Sac Bunt - play at (first|second|third), (batter|runner) OUT -> throw to (first|second|third), DP!$")
sac_bunt_safe_pattern = re.compile(r"^\[%N\]\t\d-\d: Sac Bunt (to|by) (\S+) - play at (first|second|third), (batter|runner) safe!$")
fly_out_pattern = re.compile(r"^\[%N\]\t\d-\d:  Fly out, (\S+)  \((Flyball|Line Drive|Popup), (\S+), .+\)$")
ground_out_pattern = re.compile(r"^\[%N\]\t\d-\d: Grounds? out,? (\S+) \((Groundball), (\S+), .+\)$")
gidp_pattern = re.compile(r"^\[%N\]\t\d-\d: (Grounds|Lined) into (double play|DP|DOUBLE play), (\S+) \((Groundball|Line Drive|Flyball|Popup), (\S+), .+\)$")
gitp_pattern = re.compile(r"^\[%N\]\t\d-\d: (Grounds|Lined|Lines) into (TRIPLE play|TP), (\S+) \((Groundball|Line Drive|Flyball|Popup), (\S+), .+\)$")
gidp_no_count_pattern = re.compile(r"^\[%N\]\t(Grounds|Lined) into (double play|DP), (\S+) \((Groundball|Line Drive|Flyball|Popup), (\S+), .+\)$")
gifc_pattern = re.compile(r"^\[%N\]\t\d-\d: (Grounds|Lined) into (fielders choice|FC) (\S+) \((Groundball|Line Drive|Flyball|Popup), (\S+), .+\)$")
fielders_choice_pattern = re.compile(r"^\[%N\]\t\d-\d: Fielders Choice at (2nd|3rd|home), (\S+) \((Groundball|Flyball|Line Drive|Popup), (\S+), .+\)$")
fielders_choice2_pattern = re.compile(r"^\[%N\]\t\d-\d: Fielders Choice attempt at (2nd|3rd|home), Runner SAFE. (\S+) \((Groundball|Flyball|Line Drive|Popup), (\S+), .+\)$")
pickoff_catcher_pattern = re.compile(r"^\[%N\]\tPickoff Throw by Catcher to First - Out!$")
pickoff_catcher_error_pattern = re.compile(r"^\[%N\]\tPickoff Throw by Catcher to First - Error! E2$")
pickoff_pitcher_pattern = re.compile(r"^\[%N\]\tPickoff Throw to (First|Second) - Out! 1-3( CS)?$")
pickoff_pitcher2_pattern = re.compile(r"^\[%N\]\tPickoff Throw to (First|Second) - Out!$")
pickoff_pitcher_error_pattern = re.compile(r"^\[%N\]\tPickoff Throw to (First|Second) - Error! E1$")
pickoff_advance_pattern = re.compile(r"^\[%N\]\tPickoff Play to 1st, Runner tries for 2nd, SAFE after rundown.$")
pickoff_rundown_out_pattern = re.compile(r"^\[%N\]\tPickoff Play to 1st, Runner tries for 2nd, OUT after rundown.$")
caught_stealing_pattern = re.compile(r"^\[%N\]\t(.+) is caught stealing (2nd|3rd) base (\S+)$")
caught_stealing_home_pattern = re.compile(r"^\[%N\]\tSteal of home, (.+) is out$")
successful_steal_home_pattern = re.compile(r"^\[%N\]\tSteal of home, (.+) is safe$")
successful_steal_pattern = re.compile(r"^\[%N\]\t(.+) steals (2nd|3rd) base( \(no throw\))?$")
successful_steal_error_pattern = re.compile(r"^\[%N\]\t(.+) steals (2nd|3rd), throwing error, (\S+)$")
catcher_interference_pattern = re.compile(r"^\[%N\]\t\d-\d: Reaches on Catchers interference$")

# TODO get rid of this stuff when ready
runner_scores_pattern = re.compile(r"^\[%N\]\t(.+) scores$")
runner_advances_third_pattern = re.compile(r"^\[%N\]\t(.+) advances to 3rd base$")
runner_to_third_pattern = re.compile(r"^\[%N\]\t(.+) to third$")
runner_to_second_pattern = re.compile(r"^\[%N\]\t(.+) to second$")
runner_tags_safe_throw_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tags up, SAFE at 3rd with throw by (LF|CF|RF)$")
runner_tags_safe_no_throw_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tags up, SAFE at (2nd|3rd), no throw by (LF|CF|RF)$")
runner_tags_safe_pattern = re.compile(r"^\[%N\]\tRunner from (1st|2nd) tags up, SAFE at (2nd|3rd)$")
runner_tags_scores_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tags up, SCORES, throw by (LF|CF|RF)$")
runner_tags_scores_no_throw_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tags up, SCORES, no throw by (LF|CF|RF)$")
runner_tags_out_pattern = re.compile(r"^\[%N\]\tRunner from (1st|2nd|3rd) tags up, OUT at (2nd|3rd|HOME)! (\S+)$")
runner_tries_safe_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tries for (3rd|Home), SAFE after rundown.$")
runner_tries_safe2_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tries for (3rd|Home), SAFE, throw by (P|C|1B|2B|3B|SS|LF|CF|RF) to home$")
runner_tries_safe3_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tries for (3rd|Home), throw by (P|C|1B|2B|3B|SS|LF|CF|RF) and SAFE!$")
runner_tries_error_score_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tries for (3rd|Home), throw by (P|C|1B|2B|3B|SS|LF|CF|RF) and ERROR! Runner scores!$")
runner_tries_out_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tries for (3rd|Home), throw by (P|C|1B|2B|3B|SS|LF|CF|RF) and OUT! (\S+)$")
runner_tries_out2_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tries for (3rd|Home), OUT! (\S+)$")
runner_tries_out_rundown_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tries for (3rd|Home), OUT after rundown.$")
runner_tries_no_advance_no_throw_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tries for (3rd|Home), SAFE, no throw by (P|C|1B|2B|3B|SS|LF|CF|RF)$")
runner_tries_no_advance_throw_pattern = re.compile(r"^\[%N\]\tRunner from (2nd|3rd) tries for (3rd|Home), SAFE, throw by (LF|CF|RF) to (3rd|home)$")
runner_tags_trailing_out_pattern = re.compile(r"^\[%N\]\tRunner from 2nd tries for 3rd, SAFE, throw by (LF|CF|RF) made at trailing runner, OUT! (\S)+$")
runner_tries_trailing_safe_pattern = re.compile(r"^\[%N\]\tRunner from 3rd tries for Home, SAFE, throw by (LF|CF|RF) to trailing runner, SAFE at third!$")
runner_tries_trailing_out_pattern = re.compile(r"^\[%N\]\tRunner from 3rd tries for Home, SAFE, throw by (LF|CF|RF) to trailing runner, OUT at third! (\S+)$")
runner_tries_double_play_pattern = re.compile(r"^\[%N\]\tRunner from 2nd tries for 3rd, throw by (C|LF|CF|RF) and OUT! (\S+) Double Play!$")
hidden_ball_pattern = re.compile(r"^\[%N\]\tHidden ball trick at (first|second|third) base, runner out!$")

def __batted_ball_type_str_int__(bb_type: str) -> int:
    if bb_type == "Bunt":
        return 0
    if bb_type == "Groundball":
        return 1
    elif bb_type == "Line Drive":
        return 2
    elif bb_type == "Flyball":
        return 3
    elif bb_type == "Popup":
        return 4

    print(bb_type, "unrecognized batted ball type")
    exit()

def __get_catcher__(home_bsl: BoxScoreLineup, visiting_bsl: BoxScoreLineup, home_team: str, cur_batting_team: str) -> CardPlayer:
    if home_team == cur_batting_team:
        if visiting_bsl.lineup[2] == None:
            return None

        return visiting_bsl.lineup[2].player.card_player
    else:
        if home_bsl.lineup[2] == None:
            return None

        return home_bsl.lineup[2].player.card_player

@dataclass
class Faceoffs:
    d: Dict[str, int] = field(default_factory=dict)

    def record_faceoff(self, pitching_team: str, pitcher: CardPlayer, batter: CardPlayer) -> int:
        faceoff = pitching_team + pitcher.name + batter.name
        if faceoff not in self.d:
            self.d[faceoff] = 0

        self.d[faceoff] += 1

        return self.d[faceoff]

def parse_log(
    lines: List[str],
    stats_players: List[BaseStatsPlayer],
    home_bsl: BoxScoreLineup,
    visiting_bsl: BoxScoreLineup
) -> List[Play]:
    first_play_match = first_play_pattern.match(lines[0])

    visiting_team = first_play_match.group(1)
    visiting_batters = get_possible_batters_for_team(visiting_team, stats_players)
    visiting_pitchers = get_possible_pitchers_for_team(visiting_team, stats_players)

    home_team = first_play_match.group(2)
    home_batters = get_possible_batters_for_team(home_team, stats_players)
    home_pitchers = get_possible_pitchers_for_team(home_team, stats_players)

    cur_batting_team: str = None
    cur_batter = None
    cur_pitcher = None
    cur_inning: int = 0

    faceoffs: Faceoffs = Faceoffs()


    plays: List[Play] = []
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        if line.startswith("[%T]\tTop"):
            cur_batting_team = visiting_team
            cur_inning += 1
            i += 1
            continue

        if line.startswith("[%T]\tBottom"):
            cur_batting_team = home_team
            i += 1
            continue

        if line.startswith("[%F]"):
            i += 1
            continue

        match = pitching_switch_pattern.match(line)
        if match != None:
            pitcher_name = match.group(1)
            if pitcher_name == "Jim Unknown":
                return plays
            cur_pitcher = get_player_from_list(pitcher_name, visiting_pitchers if cur_batting_team == home_team else home_pitchers)
            i += 1
            continue

        match = batting_switch_pattern.match(line)
        if match != None:
            batter_name = match.group(1)
            if batter_name == "Jim Unknown":
                return plays
            cur_batter = get_player_from_list(batter_name, home_batters if cur_batting_team == home_team else visiting_batters)
            i += 1
            continue

        match = pinch_hit_pattern.match(line)
        if match != None:
            batter_name = match.group(1)
            cur_batter = get_player_from_list(batter_name, home_batters if cur_batting_team == home_team else visiting_batters)
            if cur_batting_team == home_team:
                home_bsl.replace_batter(batter_name)
            else:
                visiting_bsl.replace_batter(batter_name)
            i += 1
            continue

        match = pinch_runner_pattern.match(line)
        if match != None:
            """
            runner_name = match.group(2)
            if cur_batting_team == home_team:
                home_bsl.replace_batter(runner_name)
            else:
                visiting_bsl.replace_batter(runner_name)
            """
            i += 1
            continue

        match = noop_pattern.match(line)
        if match != None:
            i += 1
            continue

        match = balk_pattern.match(line)
        if match != None:
            """
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BALK",
                    game_sub_result="BALK",
                    bip_event=None
                )
            )
            """
            i += 1
            continue

        match = wild_pitch_pattern.match(line)
        if match != None:
            """
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="WILD_PITCH",
                    game_sub_result="WILD_PITCH",
                    bip_event=None
                )
            )
            """
            i += 1
            continue

        match = throwing_error_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = passed_ball_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = hbp_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="HIT_BY_PITCH",
                    game_sub_result="HIT_BY_PITCH",
                    bip_event=None
                )
            )
            i += 1
            continue

        match = ibb_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="INTENTIONAL_WALK",
                    game_sub_result="INTENTIONAL_WALK",
                    bip_event=None
                )
            )
            i += 1
            continue

        match = strikeout_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="STRIKEOUT",
                    game_sub_result="STRIKEOUT",
                    bip_event=None
                )
            )
            i += 1
            continue

        match = strikeout2_pattern.match(line)
        if match != None:
            # This is a noop - a strikeout has already been recorded
            i += 1
            continue

        match = strikeout_with_caught_stealing_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="STRIKEOUT",
                    # TODO maybe redo this
                    game_sub_result="STRIKEOUT_W_CAUGHT_STEALING",
                    bip_event=None
                )
            )
            i += 1
            continue

        match = strikeout_passed_ball_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="PASSED_BALL",
                    game_sub_result="STRIKEOUT",
                    bip_event=None
                )
            )
            i += 1
            continue

        match = strikeout_wild_pitch_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="WILD_PITCH",
                    game_sub_result="STRIKEOUT",
                    bip_event=None
                )
            )
            i += 1
            continue

        match = walk_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="WALK",
                    game_sub_result="WALK",
                    bip_event=None
                )
            )
            i += 1
            continue

        match = single_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="SINGLE",
                    game_sub_result="SINGLE",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(2)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(1)),
                        location=match.group(2),
                        game_outcome="HIT"
                    )
                )
            )
            i += 1
            continue

        match = single_rundown_safe_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="SINGLE",
                    game_sub_result="SINGLE",
                    # No info recorded
                    bip_event=None
                )
            )
            i += 1
            continue

        match = single_rundown_out_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="SINGLE",
                    # No info recorded
                    bip_event=None
                )
            )
            i += 1
            continue

        match = single_out_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="SINGLE",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(2)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(1)),
                        location=match.group(2),
                        game_outcome="HIT_BAD_BASERUNNING"
                    )
                )
            )
            i += 1
            continue

        match = single_out2_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="SINGLE",
                    # Not enough info
                    bip_event=None
                )
            )
            i += 1
            continue

        match = double_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="DOUBLE",
                    game_sub_result="DOUBLE",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(2)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(1)),
                        location=match.group(2),
                        game_outcome="HIT"
                    )
                )
            )
            i += 1
            continue

        match = double_out_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="DOUBLE",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(2)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(1)),
                        location=match.group(2),
                        game_outcome="HIT_BAD_BASERUNNING"
                    )
                )
            )
            i += 1
            continue

        match = double_from_single_error_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="DOUBLE",
                    game_sub_result="SINGLE",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(3), match.group(1)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(2)),
                        location=match.group(3),
                        game_outcome="HIT_ERROR"
                    )
                )
            )
            i += 1
            continue

        match = triple_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="TRIPLE",
                    game_sub_result="TRIPLE",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(2)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(1)),
                        location=match.group(2),
                        game_outcome="HIT"
                    )
                )
            )
            i += 1
            continue

        match = home_run_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="HOME_RUN",
                    game_sub_result="HOME_RUN",
                    bip_event=None
                )
            )
            i += 1
            continue

        match = bunt_for_hit_safe_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="SINGLE",
                    game_sub_result="BUNT_FOR_HIT",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(1)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__("Bunt"),
                        location=match.group(1),
                        game_outcome="HIT"
                    )
                )
            )
            i += 1
            continue

        match = squeeze_bunt_scores_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="SINGLE",
                    game_sub_result="BUNT_FOR_HIT",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(1)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__("Bunt"),
                        location=match.group(1),
                        game_outcome="HIT"
                    )
                )
            )
            i += 1
            continue

        match = squeeze_bunt_scores_out_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="BUNT_FOR_HIT_OUT",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(1)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__("Bunt"),
                        location=match.group(1),
                        game_outcome="OUT"
                    )
                )
            )
            i += 1
            continue


        match = fly_out_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            # TODO watch out for SAC fly
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="BIP_OUT",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(3)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(2)),
                        location=match.group(3),
                        game_outcome="OUT"
                    )
                )
            )
            i += 1
            continue

        match = ground_out_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            # TODO watch out for SAC fly?
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="BIP_OUT",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(3)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(2)),
                        location=match.group(3),
                        game_outcome="OUT"
                    )
                )
            )
            i += 1
            continue

        match = bunt_for_hit_out_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            # TODO remove these from regular hits?
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="BUNT_FOR_HIT_OUT",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(1)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__("Bunt"),
                        location=match.group(1),
                        game_outcome="OUT"
                    )
                )
            )
            i += 1
            continue

        match = squeeze_bunt_runner_out_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            # TODO remove these from regular hits?
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="SINGLE",
                    game_sub_result="SQUEEZE_BUNT",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(1)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__("Bunt"),
                        location=match.group(1),
                        game_outcome="OUT"
                    )
                )
            )
            i += 1
            continue

        match = bunt_for_hit_out2_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            # TODO remove these from regular hits?
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="BUNT_FOR_HIT_OUT",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(1)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__("Bunt"),
                        location=match.group(1),
                        game_outcome="OUT"
                    )
                )
            )
            i += 1
            continue

        match = bunt_for_hit_double_play_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            # TODO remove these from regular hits?
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="BUNT_FOR_HIT_DOUBLE_PLAY",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(1)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__("Bunt"),
                        location=match.group(1),
                        game_outcome="OUT"
                    )
                )
            )
            i += 1
            continue

        match = bip_error_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="SINGLE",
                    game_sub_result="BIP_ERROR",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(3)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(2)),
                        location=match.group(3),
                        game_outcome="HIT_ERROR"
                    )
                )
            )
            i += 1
            continue

        match = bip_error_dropped_throw_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="SINGLE",
                    game_sub_result="BIP_ERROR",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(4)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(3)),
                        location=match.group(4),
                        game_outcome="HIT_ERROR"
                    )
                )
            )
            i += 1
            continue

        match = sac_bunt_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            # TODO watch out for advances?
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="SAC_BUNT_OUT",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(1)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__("Bunt"),
                        location=match.group(1),
                        game_outcome="OUT"
                    )
                )
            )
            i += 1
            continue

        match = sac_bunt_dp_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            # TODO watch out for advances?
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="SAC_BUNT_DP",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(1)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__("Bunt"),
                        location=match.group(1),
                        game_outcome="OUT"
                    )
                )
            )
            i += 1
            continue

        match = sac_bunt_dp2_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            # TODO watch out for advances?
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="SAC_BUNT_DP",
                    bip_event=None
                )
            )
            i += 1
            continue

        match = sac_bunt_safe_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="SINGLE",
                    game_sub_result="SAC_BUNT_HIT",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(2)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__("Bunt"),
                        location=match.group(2),
                        game_outcome="HIT"
                    )
                )
            )
            i += 1
            continue

        match = gidp_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="GIDP",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(5)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(4)),
                        location=match.group(5),
                        game_outcome="DOUBLE_OUT"
                    )
                )
            )
            i += 1
            continue

        match = gitp_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="BIP_OUT",
                    game_sub_result="GITP",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(5)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(4)),
                        location=match.group(5),
                        game_outcome="TRIPLE_OUT"
                    )
                )
            )
            i += 1
            continue

        match = gidp_no_count_pattern.match(line)
        if match != None:
            # TODO need to cover this by the flyout play
            i += 1
            continue

        match = gifc_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="SINGLE",
                    game_sub_result="FIELDERS_CHOICE",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(5)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(4)),
                        location=match.group(5),
                        game_outcome="OUT"
                    )
                )
            )
            i += 1
            continue

        match = fielders_choice_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="SINGLE",
                    game_sub_result="FIELDERS_CHOICE",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(4)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(3)),
                        location=match.group(4),
                        game_outcome="OUT"
                    )
                )
            )
            i += 1
            continue

        match = fielders_choice2_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="SINGLE",
                    game_sub_result="SINGLE",
                    bip_event=BIPEvent(
                        fielder=find_fielders_for_play(home_bsl if cur_batting_team != home_team else visiting_bsl, match.group(4)),
                        batter=cur_batter,
                        batted_ball_type=__batted_ball_type_str_int__(match.group(3)),
                        location=match.group(4),
                        game_outcome="HIT"
                    )
                )
            )
            i += 1
            continue

        match = pickoff_catcher_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = pickoff_catcher_error_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = pickoff_pitcher_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = pickoff_pitcher2_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = pickoff_pitcher_error_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = pickoff_advance_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = pickoff_rundown_out_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = caught_stealing_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = caught_stealing_home_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = successful_steal_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = successful_steal_home_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = successful_steal_error_pattern.match(line)
        if match != None:
            # TODO
            i += 1
            continue

        match = catcher_interference_pattern.match(line)
        if match != None:
            catching_player = __get_catcher__(home_bsl, visiting_bsl, home_team, cur_batting_team)
            if catching_player == None:
                return plays
            plays.append(
                BattingPlay(
                    playtype="BATTING_PLAY",
                    cur_inning=cur_inning,
                    pitching_player=cur_pitcher,
                    batting_player=cur_batter,
                    catcher_player=catching_player,
                    cur_team=cur_batting_team,
                    times_faced_off=faceoffs.record_faceoff(cur_batting_team, cur_pitcher, cur_batter),
                    baseball_result="CATCHERS_INTERFERENCE",
                    game_sub_result="CATCHERS_INTERFERENCE",
                    bip_event=None
                )
            )
            i += 1
            continue

        match = position_switch_pattern.match(line)
        if match != None:
            fielder_name = match.group(3)
            new_pos = int(__pos_to_num__(match.group(2)))
            if cur_batting_team == home_team:
                visiting_bsl.replace_fielder(fielder_name, position=new_pos)
            else:
                home_bsl.replace_fielder(fielder_name, position=new_pos)
            i += 1
            continue

        # TODO these go away later
        match = runner_scores_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_advances_third_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_to_third_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_to_second_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_no_advance_no_throw_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_no_advance_throw_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tags_scores_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tags_scores_no_throw_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tags_safe_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tags_safe_throw_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tags_safe_no_throw_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tags_out_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tags_trailing_out_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_trailing_safe_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_trailing_out_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_safe_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_safe2_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_safe3_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_error_score_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_out_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_out2_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_out_rundown_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = runner_tries_double_play_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = squeeze_bunt_runner_out2_pattern.match(line)
        if match != None:
            i += 1
            continue
        match = hidden_ball_pattern.match(line)
        if match != None:
            i += 1
            continue

        print(line)
        exit()
    
    return plays