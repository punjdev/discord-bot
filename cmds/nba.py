from discord.ext import commands
import pandas as p
from nba_api.stats.static import players
from nba_api.stats.static import teams

playerID = {}
athletes = players.get_players() # dict
teams = teams.get_teams() #list

@commands.group()
async def nba(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("FILLER FOR INFO")
        
@nba.command(
    aliases=['id'],
    help="Reloads/resets subcommands",
    description="Reloads all subcommands",
    breif="Call to reload bot",
    enabled=True,
    hidden=True)
async def getid(ctx, *name: str):
    player = ' '.join(name)
    player = player.lower()
    await ctx.send(f"{player}: {playerID[player]}")
        
async def setup(bot):
    for player in athletes: # playerID references a player dict from athletes name -> id
        playerID[str(player["full_name"]).lower()] = player["id"]
    # print(playerID)
    bot.add_command(nba)