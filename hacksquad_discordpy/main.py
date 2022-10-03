import discord
from discord.ext import commands
import os
from dotenv import load_dotenv

load_dotenv()
intents = discord.Intents.all()

my_secret = os.environ["Token"]  # Bot Token
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
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Synced")

bot.run(my_secret)

