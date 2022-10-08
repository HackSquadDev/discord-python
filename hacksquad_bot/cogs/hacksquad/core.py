import random

import discord
from discord.ext import commands

from hacksquad_bot.cogs.hacksquad.utils import Requester
from hacksquad_bot.main import Context, HackSquadBot


class HackSquad(commands.Cog):
    def __init__(self, bot: HackSquadBot) -> None:
        self.bot = bot

    @staticmethod
    def pr_formatter(pr_data: list):
        if len(pr_data) > 3:
            pr_data = pr_data[:3]
        prs = ""
        for pr in pr_data:
            prs += f"[**{pr['title']}**]({pr['url']})\n"

        return prs

    @staticmethod
    def hero_embed_formatter(contributor: dict):
        name = contributor["name"]
        github = f"[{contributor['github']}](https://github.com/{contributor['github']})"
        avatar_url = contributor["avatar_url"]

        pulls = contributor["pulls"]
        number_of_pulls = len(pulls)

        embed = discord.Embed(
            title=f"{name}",
            description=f"<:github:1026874300956938300> [{github}](https://github.com/{github})\n\n**Number of PRs:** {number_of_pulls}\n**Last 3 PRs:\n**{HackSquad(HackSquadBot).pr_formatter(pulls)}\n",
            color=discord.Color.random(),
        )
        embed.set_thumbnail(url=avatar_url)

        return embed

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
                await message.edit(
                    content=None, embed=HackSquad(HackSquadBot).hero_embed_formatter(contributor)
                )

    @commands.hybrid_command()
    async def randomhero(self, ctx: Context):
        """
        Show the details of heros who have contributed to Hacksquad 2022!
        """
        message = await ctx.send("Getting a random hero... That one must be awesome")
        contributors = await Requester().fetch_contributors()
        contributor = random.choice(contributors)

        await message.edit(content=None, embed=self.hero_embed_formatter(contributor))
