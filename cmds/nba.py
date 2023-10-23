from discord.ext import commands
from dateutil import parser # to deal with utc date
from datetime import datetime, timedelta
import time
from nba_api.stats.static import players, teams
from nba_api.stats.endpoints import leaguestandingsv3
from nba_api.live.nba.endpoints import scoreboard, boxscore, playbyplay

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
    aliases=['sc', 'scoreboard'],
    help="$[nba|n|basketball] [scores|sc|scoreboard]",
    description="Outputs all the scores for todays games.",
    breif="Todays Nba Scoreboard.",
    enabled=True,
    hidden=False
    )
async def scores(ctx, *name: str):
    '''Todays Nba Scoreboard.'''
    games = scoreboard.ScoreBoard().games.get_dict() # list of dicts of all the games for today
    output = ""
    for game in games: 
        home = game['homeTeam']
        away = game['awayTeam']
        game_leaders = game['gameLeaders']
            
         # deal with utc date using parser
        date = parser.parse(game['gameTimeUTC'])
        date = date - timedelta(hours=5, minutes=0) # Convert from utc to est
                
        # game is finished
        if game['gameClock'] == "" and game['period'] >= 4:
            matchup = f"{str(home['wins'])}-{str(home['losses'])} {home['teamCity']} {home['teamName']} vs {str(away['wins'])}-{str(away['losses'])} {away['teamCity']} {away['teamName']}"
            score = f"{home['teamTricode']} {home['score']} - {away['teamTricode']} {away['score']}"
            # player game leaders from home & away
            home_leaders = f"\t\t{game_leaders['homeLeaders']['teamTricode']}: {game_leaders['homeLeaders']['name']} {game_leaders['homeLeaders']['points']}pts/{game_leaders['homeLeaders']['rebounds']}rbs/{game_leaders['homeLeaders']['assists']}ast"
            away_leaders = f"\t\t{game_leaders['awayLeaders']['teamTricode']}: {game_leaders['awayLeaders']['name']} {game_leaders['awayLeaders']['points']}pts/{game_leaders['awayLeaders']['rebounds']}rbs/{game_leaders['awayLeaders']['assists']}ast"                 
            
            output += f"{matchup}\n\tFinal Score: {score}\n\tGame Leaders:\n{home_leaders}\n{away_leaders}\n"
        
        # game has not started
        elif game['gameClock'] == "":
            date = date.strftime("%A @ %I:%M %p")
            
            matchup = f"{str(home['wins'])}-{str(home['losses'])} {home['teamCity']} {home['teamName']} vs {str(away['wins'])}-{str(away['losses'])} {away['teamCity']} {away['teamName']} - {date}"
            output += f"{matchup}\n"
            
        # game is going on
        else:
            date = date.strftime("%I:%M %p")
                        
            # setting time left in the quater
            clock = time.strptime(game['gameClock'], "PT%MM%S.00S")
            clock = time.strftime("%M:%S", clock)
            
            # set quater
            if game['period'] == 1 : 
                quater = 'first'
            elif game['period'] == 2: 
                quater = 'second'
            elif game['period'] == 3: 
                quater = 'third'
            elif game['period'] == 4: 
                quater = 'fourth'
            
             # Set f strings where each var is a output line appended to the output string
            matchup = f"{str(home['wins'])}-{str(home['losses'])} {home['teamCity']} {home['teamName']} vs {str(away['wins'])}-{str(away['losses'])} {away['teamCity']} {away['teamName']} @ {date}"
            score = f"\t{clock} remaining in the {quater} quater\n\tScore: {home['teamTricode']} {home['score']} - {away['teamTricode']} {away['score']}"
            timeouts = f"\tTimeouts Remaining: {home['teamTricode']} {home['timeoutsRemaining']} - {away['teamTricode']} {away['timeoutsRemaining']}"
            # player game leaders from home & away
            home_leaders = f"\t\t{game_leaders['homeLeaders']['teamTricode']}: {game_leaders['homeLeaders']['name']} {game_leaders['homeLeaders']['points']}pts/{game_leaders['homeLeaders']['rebounds']}rbs/{game_leaders['homeLeaders']['assists']}ast"
            away_leaders = f"\t\t{game_leaders['awayLeaders']['teamTricode']}: {game_leaders['awayLeaders']['name']} {game_leaders['awayLeaders']['points']}pts/{game_leaders['awayLeaders']['rebounds']}rbs/{game_leaders['awayLeaders']['assists']}ast"
            
            output += f"{matchup}\n{score}\n{timeouts}\n\tGame Leaders:\n{home_leaders}\n{away_leaders}\n"
            
        output += f"\n"
        
    await ctx.send(output) # output as 1 message


# Stat commands
##########################################################################

@nba.command(
    aliases=['stand'],
    enabled=True,
    hidden=True)
async def standings(ctx):
    table = leaguestandingsv3.LeagueStandingsV3().get_dict()
    for t in table:
        print(t, table[t])
    await ctx.send("test")


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