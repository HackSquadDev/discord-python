import discord
from discord.ext import commands
import os

intents = discord.Intents.all()

my_secret = os.environ["Token"]  # Bot Token
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
async def sync(ctx):
    await bot.tree.sync()
    await ctx.send("Synced")

bot.run(my_secret)

