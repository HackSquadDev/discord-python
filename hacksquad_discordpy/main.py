import os

import discord
from discord.ext import commands

from wrappers.leaderboard import leaderboard_wrapper
from wrappers.team import team_wrapper

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

intents = discord.Intents.all()
my_secret = os.environ["TOKEN"]  # Bot Token
bot = commands.Bot(command_prefix="!", intents=intents)
activity = discord.Activity(type=discord.ActivityType.listening, name="!help")

@bot.event
async def on_ready():
    await bot.load_extension("jishaku")
    print("Bot is running as {0.user}".format(bot))

@bot.hybrid_command()
async def ping(ctx):
    await ctx.send("Pong!")


@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Synced")


bot.run(my_secret)
