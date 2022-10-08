from typing import List, TypedDict

import discord
from discord import Interaction, app_commands
from discord.ext import commands
from tabulate import tabulate

from hacksquad_bot.cogs.hacksquad.utils import Requester
from hacksquad_bot.main import Context, HackSquadBot

from .utils import HACKSQUAD_COLOR, PRStatus, Requester


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
            description=f"**Github:** [{github}](https://github.com/{github})\n\n**Number of PRs:** {number_of_pulls}\n**Last 3 PRs:\n**{HackSquad(HackSquadBot).pr_formatter(pulls)}\n",
            color=discord.Color.random(),
        )
        embed.set_thumbnail(url=avatar_url)

        return embed

    @commands.hybrid_command()
    async def leaderboard(self, ctx: Context):
        """
        Show the leaderboard of HackSquad 2022!
        """
        if page <= 0:
            await interaction.response.send_message("The page cannot be negative or 0.")
            return
        page -= 1

        class MinimifiedPartialTeam(TypedDict):
            place: int
            name: str
            score: int
            slug: str

        results = await Requester().fetch_leaderboard()
        results.sort(key=lambda x: x["score"], reverse=True)

        teams: List[MinimifiedPartialTeam] = [
            MinimifiedPartialTeam(
                place=place, name=result["name"], score=result["score"], slug=result["slug"]
            )
            for place, result in enumerate(results, 1)
        ]

        list_of_teams = [teams[x : x + 10] for x in range(0, len(teams), 10)]

        # sourcery skip: min-max-identity
        if page > len(list_of_teams):
            # Last page
            page = len(list_of_teams) - 1

        teams = list_of_teams[page]
        msg = tabulate(
            teams,
            headers={"place": "Place", "name": "Name", "score": "Score", "slug": "Slug"},
            tablefmt="pretty",
        )
        msg += f"\nShowing {len(teams)} teams - Page {page + 1}/{len(list_of_teams)}"
        await interaction.response.send_message(f"```diff\n{msg}\n```")

    @app_commands.command()
    async def team(self, interaction: Interaction, *, team_slug: str):
        """
        Get the details of a team participating in Hacksquad 2022!

        Use the "Slug" as the team's name.
        """
        results = await Requester().fetch_team(team_slug)

        embed = discord.Embed(title=f"Team: {results['name']}", color=HACKSQUAD_COLOR)

        if results["owner"]:
            embed.set_thumbnail(url=results["owner"]["image"])
            embed.add_field(name="Created By", value=results["owner"]["name"])

        embed.add_field(name="Team ID", value=results["id"])
        embed.add_field(name="Team slug", value=results["slug"])

        total_prs = results["prs"]
        accepted = [pr for pr in results["prs"] if pr["status"] == PRStatus.ACCEPTED]
        deleted = [pr for pr in results["prs"] if pr["status"] == PRStatus.DELETED]

        prs_ratio = round(len(total_prs) / len(deleted), 1) if deleted else 0
        embed.description = f"The team `{results['name']}` has realized a total of `{len(total_prs)}` pull requests, which `{len(accepted)}` are accepted and `{len(deleted)}` are deleted from the competition.\n(Deletion ratio: `{f'{prs_ratio}' if prs_ratio else '0'}%`)"

        last_3_prs = accepted[-3:]

        if prs_str := "\n".join([f"**[{pr['title']}]({pr['url']})**" for pr in last_3_prs]):
            embed.description += f"\n\n**{len(last_3_prs)} last accepted PRs:**\n{prs_str}"

        await interaction.response.send_message(embed=embed)

    @app_commands.command(name="search")
    async def search_team(self, interaction: Interaction, *, query: str):
        results = await Requester().fetch_leaderboard()

        matching = [x for x in results if query in x["name"]]

        if not matching:
            await interaction.response.send_message("No results were found...")
            return

        list_str = "\n".join(
            f"- Name: `{match['name']}` / Slug: `{match['slug']}`" for match in matching
        )
        await interaction.response.send_message(f"__Results__:\n\n{list_str}")

    @app_commands.command()
    async def hero(self, interaction: discord.Interaction, *, hero: str):
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
