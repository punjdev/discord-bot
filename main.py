import discord
from discord import message
from discord.ext import commands
from commands import *
import random


tokenFile = open("data.txt", "r")
token = tokenFile.readline()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
# client = discord.Client(intents=intents)

bot = commands.Bot(command_prefix='>', intents=intents)

class Slapper(commands.Converter):
    use_nicknames: bool
    def __init__(self, *, use_nicknames) -> None:
        self.use_nicknames = use_nicknames
        
    async def convert(self, ctx, arguement):
        someone = random.choice(ctx.guild.members)
        if self.use_nicknames:
            nickname = ctx.author.nick
        
        return f"{ctx.author} slaps {someone} with {arguement}"
    
# confirming bot is online
@bot.event
async def on_ready():
    # for guild in client.guilds:
    #     print(guild.name)
    print(f'{bot.user} has connected to Discord!')


@bot.command(name="ping",
             aliases = ["p"],
             help = "PING ya",
             description="Help command",
             breif = "breif test",
             enabled = True,
             hidden = False
            )
async def ping(ctx):
    """Answers with pong"""
    await ctx.send("pong")

@bot.command()
async def say(ctx, *what):
    await ctx.send(" ".join(what))
    
@bot.command()
async def slap(ctx, reason: Slapper(use_nicknames=True)):
    await ctx.send(reason)
    

bot.run(token)