# ootp-gamelog-stats-analysis-23

This is a repo meant to analyze individual game logs from a league (regular PT or tournament)

## Intro

Hey y'all. If you're familiar with my other work, this builds on that. The quality of code/stuff may be a step down because not everything is finished, but I'm a bit bored of OOTP right now. I don't plan on doing too much further here, but some planned stuff is included.

## Scraping a League/Tourney

Warning: scraping will read OOTP's google servers and make a request every 5 seconds. Generally when scraping a website (even google) it's common to wait 5 seconds between requests. That's what I have configured. If you change this (or even if you run this) you may run the risk of getting an IP ban.

Make sure python is installed alongside this code and install dependencies. I usually use VSCode to edit/run things.

You'll need a couple things here.

1. Get a copy of the league/tournament OVR file. Do a pull with basically all the counting stats checked (for a full list of the stats I use, see the league pulls section from https://forums.ootpdevelopments.com/showthread.php?t=325240). Drop this file in import_data
2. Get the league hash - when you open the OVR file in the browser, you'll see one part of the url is not readable, being a list of letterns and numbers like 7ea10000000000000000ad51 . You'll want to copy that somewhere.
3. Name the league. Usually I do this - 
    For league files I name it league_year_name so it might be league_2024_g317.
    For tournament files I name it T[tournamenttype]_[numberofteams]_[id] so it might be Topenbronze_32_11 (I wouldn't recommend putting any spaces " " in the name)

Once you have the data from 2 and 3, edit the leagues_to_scrape.txt file - put the hash first, then a comma, followed by the league name.

WARNING: Importing takes a while so I would recommend making sure the leagues_to_scrape file only contains lines for leagues you want to pull.

You can run `python import_data.py` to read the ovr files into the correct place. Then you can run `python scrape_all_leagues.py` to scrape leagues/tournaments. It'll take ~10 minutes per tournament (more if it's a larger tournament) and much longer for a league pull. Just leave it running in the background and wait.

## Generating vL/vR files.

You can run `python generate_splits.py` and in the `output` folder check for the tournament type file with vL and vR.

## How did I find the URL's

I used WireShark (https://www.wireshark.org/) and ran it. Then I opened OOTP and loaded some stats in a tournament and saw what url it loaded.

## Caveats

I provide some basic log analysis for batting events. I don't have baserunning or non-batting event parsing working. I also stop parsing a game when 40 overall "Jim Unknown" players enter the game. I regard any stats produced against a "Jim Unknown" as not worth reading.

## Other stuff

If you look into the `project_tourneys.py` file or the `test.py` file you'll see where I've tried to implement some data analysis deeply around individual hitter-pitcher matchups that also takes into account defense. At the current stage of code it's more of an interesting project rather than a useful one. Anyone is free to try to make the code work better/produce better results.

If you want to use this you'll need to keep a cards folder in the `data/` folder and pop a pt_card_list.csv in there. You can kind of tell what it should look like by reading the other code in here. If you need help, message me on discord and ask for what it might look like.