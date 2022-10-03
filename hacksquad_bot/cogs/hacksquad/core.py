from discord.ext import commands

from hacksquad_bot.main import HackSquadBot, Context


class HackSquad(commands.Cog):
    
    def __init__(self, bot: HackSquadBot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def leaderboard(self, ctx: Context):
        """
        Show the leaderboard of HackSquad 2022!
        """
        await ctx.send("The leaderboard is a work-in-progress! Check back later!")

    @commands.hybrid_command()
    async def teams(self, ctx: Context):
        await ctx.send("The team is a work-in-progress! Check back later!")
