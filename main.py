import discord
from discord import message
from discord.ext import commands
import pathlib

# Get token data
tokenFile = open("data.txt", "r")
token = tokenFile.readline()

# init
intents = discord.Intents.default()
intents.members = True
intents.message_content = True
bot = commands.Bot(command_prefix='$', intents=intents)
cmdsdir = pathlib.Path(__file__).parent / "cmds"

# test comment
# confirming bot is online
@bot.event
async def on_ready():
    print(f'{bot.user} online!')
    for cmd_file in cmdsdir.glob("*.py"):
        if cmd_file.name != "__init__.py":
            print(cmd_file.name)
            print(f"cmds.{cmd_file.name[:-3]}")
            await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
            
@bot.event
async def on_command_error(ctx, error):   
    # if isinstance(error, commands.MissingRequiredArgument):
    await ctx.send(f"An error occurred with: {ctx.message}.\nPlease refer to $help for assistance.")
        


# allows us to update bot cmds without shutting the bot down
@bot.command(
    aliases=['reset'],
    help="Reloads/resets subcommands",
    description="Reloads all subcommands",
    breif="Call to reload bot",
    enabled=True,
    hidden=True
)
@commands.is_owner()
async def reload(ctx):
    for cmd_file in cmdsdir.glob("*.py"):
        if cmd_file.name != "__init__.py":
            await bot.unload_extension(f"cmds.{cmd_file.name[:-3]}")
            await bot.load_extension(f"cmds.{cmd_file.name[:-3]}")
            await ctx.send(f"Reloaded cmds.{cmd_file.name[:-3]}.")


bot.run(token)