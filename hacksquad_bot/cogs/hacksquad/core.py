import random

from discord.ext import commands

from hacksquad_bot.cogs.hacksquad.utils import Requester
from hacksquad_bot.main import Context, HackSquadBot


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
        """
        Get the details of a team participating in Hacksquad 2022!
        """
        await ctx.send("The team is a work-in-progress! Check back later!")

    @commands.hybrid_command()
    async def hero(self, ctx: Context, *, hero: str):
        """
        Show the details of heros who have contributed to Hacksquad 2022!
        """
        message = await ctx.send("Proccessing request...")
        contributors = await Requester().fetch_contributors()
        for contributor in contributors:
            contributor = dict(contributor)
            if contributor["github"] == hero:
                await message.edit(content="", embed=Requester().hero_embed_formatter(contributor))

    @commands.hybrid_command()
    async def randomhero(self, ctx: Context):
        """
        Show the details of heros who have contributed to Hacksquad 2022!
        """
        message = await ctx.send("Proccessing request...")
        contributors = await Requester().fetch_contributors()
        contributor = random.choice(contributors)

        await message.edit(content="", embed=Requester().hero_embed_formatter(contributor))
