import itertools
import math
import random
from discord.ext import commands
from statistics import median

@commands.group()
async def stats(ctx):
    if ctx.invoked_subcommand is None:
        await ctx.send("FILLER FOR INFO")

@stats.command()
async def permutations(ctx, *set):
    if len(set) <= 7:
        perm = list(itertools.permutations(list(set)))
        await ctx.send(str(perm) + "\nNumber of permutations: " + str(len(perm)))
    else:
        await ctx.send("Number of perumtations: " + math.factorial(len(set)))
        
@stats.command()
async def combinations(ctx, num: int, *set):
    if len(set) <= 7:
        comb = list(itertools.combinations(list(set), num))
        await ctx.send(str(comb) + "\nNumber of combinations: " + str(len(comb)))
    else:
        await ctx.send("Number of combinations: " + str(math.comb(len(set), num)))

@stats.command()
async def teams(ctx, num: int, *set):
    if len(set) % num == 0 and len(set) < 70:
        ppl = list(set)
        random.shuffle(ppl)
        team = ""
        print(ppl)
        for i in range(len(set)):
            team += ppl[i]  + " "
            print(team)
            if (i + 1) % 2 == 0:
                await ctx.send(team)
                team = ""
    else:
        await ctx.send("Error: Cannot make even teams")
            
@stats.command()
async def mean(ctx, *set: tuple[int, ...]):
    await ctx.send(sum(set) / len(set))
    
@stats.command()
async def median(ctx, *set: tuple[int, ...]):
    lst = list(set)
    await ctx.send(median(lst))

@stats.command()
async def sort(ctx, *set: tuple[int, ...]):
    lst = list(set)
    lst.sort()
    await ctx.send(lst)
async def setup(bot):
    bot.add_command(stats)