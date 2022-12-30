from discord.ext import commands

@commands.group()
async def test(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("wrong test command")
        
@test.command()
async def ping(ctx):
    """Answers with pong"""
    await ctx.send("pong")
    
async def setup(bot):
    bot.add_command(test)