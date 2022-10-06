from typing import List

from discord.ext import commands, menus

from hacksquad_bot.main import Context, HackSquadBot

from .menu import PageLeaderboard
from .utils import Requester


class HackSquad(commands.Cog):
    def __init__(self, bot: HackSquadBot) -> None:
        self.bot = bot

    @commands.hybrid_command()
    async def leaderboard(self, ctx: Context):
        """
        Show the leaderboard of HackSquad 2022!
        """
        results = await Requester().fetch_leaderboard()
        results.sort(key=lambda x: x["score"], reverse=True)

        for place, result in enumerate(results):
            result["place"] = place

        m = menus.MenuPages(source=PageLeaderboard(results), delete_message_after=True)

        await m.start(ctx)  # type: ignore

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
        await ctx.send("The hero is a work-in-progress! Check back later!")
