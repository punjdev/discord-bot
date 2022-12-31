
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
            
@bot.command()
async def reload(ctx):
    for cmd_file in cmdsdir.glob("*.py"):
        if cmd_file.name != "__init__.py":
            await bot.unload_extension(f"cmds.{cmd_file.name[:-3]}")
            await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")

bot.run(token)