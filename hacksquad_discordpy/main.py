import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
from wrappers.team import team
from wrappers.leaderboard import leaderboard
load_dotenv()

intents = discord.Intents.all()
my_secret = os.environ["TOKEN"]  # Bot Token
bot = commands.Bot(command_prefix="!", intents=intents)
activity = discord.Activity(type=discord.ActivityType.listening, name="!help")

bot.remove_command("help")

@bot.event
async def on_ready():
    print("Bot is running as {0.user}".format(bot))


@bot.hybrid_command()
async def help(ctx):
    await ctx.send("Help")

@bot.command()
@commands.has_permissions(administrator=True)
async def sync(ctx):
    await ctx.send("Syncing the bot...")
    await bot.tree.sync()
    await ctx.send("Synced")


bot.run(my_secret)

