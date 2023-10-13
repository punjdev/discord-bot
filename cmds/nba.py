from discord.ext import commands
from dateutil import parser # to deal with utc date
from datetime import datetime, timedelta
import time
# import json
# import pandas as p
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import commonplayerinfo
from nba_api.live.nba.endpoints import scoreboard, boxscore, playbyplay

# from nba_api.stats.static import teams

playerID = {} # player full name: player id
teamID = {} # team: team id
athletes = players.get_players() # dict
teams = teams.get_teams() #list

@commands.group(
    aliases=['n', 'basketball']
)
async def nba(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("Missing sub-command, please reference $help nba.")

# LIVE NBA COMMANDS
##########################################################################

# all scores
@nba.command(
    aliases=['sc', 'scores'],
    enabled=True,
    hidden=False
    )
async def allScores(ctx, *name: str):
    ''' Output all scoreboards'''
    games = scoreboard.ScoreBoard().games.get_dict() # list of dicts of all the games for today
    output = ""
    for game in games: 
        home = game['homeTeam']
        away = game['awayTeam']
        
        # set quater
        if game['period'] == 1 : 
            quater = 'first'
        elif game['period'] == 2: 
            quater = 'second'
        elif game['period'] == 3: 
            quater = 'third'
        elif game['period'] == 4: 
            quater = 'fourth'
        else:
            quater = "first"
            
         # deal with utc date using parser
        date = parser.parse(game['gameTimeUTC'])
        date = date - timedelta(hours=5, minutes=0) # Convert from utc to est
        date = date.strftime("%I:%M %p")
        
        # game is finished
        if game['gameClock'] == "" and game['period'] == 4:
            matchup = f"{str(home['wins'])}-{str(home['losses'])} {home['teamCity']} {home['teamName']} vs {str(away['wins'])}-{str(away['losses'])} {away['teamCity']} {away['teamName']}"
            score = f"{home['teamTricode']} {home['score']} - {away['teamTricode']} {away['score']}"
            output += f"{matchup}\n\tFinal Score: {score}\n"
        
        # game has not started
        elif game['gameClock'] == "":
            matchup = f"{str(home['wins'])}-{str(home['losses'])} {home['teamCity']} {home['teamName']} vs {str(away['wins'])}-{str(away['losses'])} {away['teamCity']} {away['teamName']} @ {date}"
            output += f"{matchup}\n"
            
        # game is going on
        else:
            # setting time left in the quater
            clock = time.strptime(game['gameClock'], "PT%MM%S.00S")
            clock = time.strftime("%M:%S", clock)
            
             # Set f strings where each var is a output line appended to the output string
            matchup = f"{str(home['wins'])}-{str(home['losses'])} {home['teamCity']} {home['teamName']} vs {str(away['wins'])}-{str(away['losses'])} {away['teamCity']} {away['teamName']} @ {date}"
            score = f"\t{clock} remaining in the {quater} quater\n\tScore: {home['teamTricode']} {home['score']} - {away['teamTricode']} {away['score']}"
            timeouts = f"\tTimeouts Remaining: {home['teamTricode']} {home['timeoutsRemaining']} - {away['teamTricode']} {away['timeoutsRemaining']}"
            output += f"{matchup}\n{score}\n{timeouts}\n"
            
        output += f"\n"
    await ctx.send(output) # output as 1 message


# Stat commands
##########################################################################
# Return player id
@nba.command(
    aliases=['pid'],
    enabled=True,
    hidden=True)
async def getPlayerID(ctx, *name: str):
    # name is a lst, join and lower to get player name
    player = ' '.join(name)
    player = player.lower()
    id = playerID[player]
    await ctx.send(f"{player}: {playerID[player]}")
    # player_info = commonplayerinfo.CommonPlayerInfo(player_id=id) 
    # player_info.
    # await ctx.send(f"{player_info.get_response()}")

# Return team id
@nba.command(
    aliases=['tid'],
    enabled=True,
    hidden=True)
async def getteamID(ctx, *name: str):
    # name is a lst, join and lower to get team name
    team = ' '.join(name)
    team = team.lower()
    await ctx.send(f"{team}: {teamID[team]}")
        

async def setup(bot):
    for player in athletes: # playerID references a player dict from athletes name -> id
        playerID[str(player["full_name"]).lower()] = player["id"]
    # print(playerID)
    for team in teams:
        teamID[str(team["full_name"]).lower()] = team["id"]
    # print(teamID)
    bot.add_command(nba)