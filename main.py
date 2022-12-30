import discord
from discord import message
from discord.ext import commands
import random
import pathlib


tokenFile = open("data.txt", "r")
token = tokenFile.readline()
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='>', intents=intents)
cmdsdir = pathlib.Path(__file__).parent / "cmds"

# confirming bot is online
@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')
    for cmd_file in cmdsdir.glob("*.py"):
        if cmd_file.name != "__init__.py":
            print(cmd_file.name)
            print(f"cmds.{cmd_file.name[:-3]}")
            await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
    
# @bot.group()
# async def test(ctx):
#     if ctx.invoked_subcommand is None:
#         await ctx.send("wrong test command")
        
# @test.command()
# async def ping(ctx):
#     """Answers with pong"""
#     await ctx.send("pong")

# class Slapper(commands.Converter):
#     use_nicknames: bool
#     def __init__(self, *, use_nicknames) -> None:
#         self.use_nicknames = use_nicknames
        
#     async def convert(self, ctx, arguement):
#         someone = random.choice(ctx.guild.members)
#         if self.use_nicknames:
#             nickname = ctx.author.nick
        
#         return f"{ctx.author} slaps {someone} with {arguement}"
    

# @bot.command()
# async def say(ctx, *what):
#     await ctx.send(" ".join(what))
    
# @bot.command()
# async def slap(ctx, reason: Slapper(use_nicknames=True)):
#     await ctx.send(reason)
@bot.group()
async def math(ctx):
    await ctx.send(1)
#

bot.run(token)