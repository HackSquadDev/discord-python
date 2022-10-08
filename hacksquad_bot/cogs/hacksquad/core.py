import random
from typing import List, TypedDict

import discord
from discord import Interaction, app_commands
from discord.ext import commands
from tabulate import tabulate

from hacksquad_bot.cogs.hacksquad.utils import Requester
from hacksquad_bot.main import HackSquadBot

from .utils import HACKSQUAD_COLOR, NovuContributor, NovuPR, PRStatus, Requester


class HackSquad(commands.Cog):
    def __init__(self, bot: HackSquadBot) -> None:
        self.bot = bot

    @staticmethod
    def pr_formatter(pr_data: List[NovuPR]) -> str:
        if len(pr_data) > 3:
            pr_data = pr_data[:3]
        return "\n".join(f"[**{pr['title']}**]({pr['url']})\n" for pr in pr_data)

    @staticmethod
    def hero_embed_formatter(contributor: NovuContributor) -> discord.Embed:
        name = contributor["name"] or "Name not found"
        github = f"[{contributor['github']}](https://github.com/{contributor['github']})"
        avatar_url = contributor["avatar_url"]

        pulls = contributor["pulls"]
        number_of_pulls = len(pulls)

        embed = discord.Embed(
            title=f"{name}",
            description=f"**GitHub:** [{github}](https://github.com/{github})\n\n**Number of PRs:** {number_of_pulls}",
            color=HACKSQUAD_COLOR,
        )
        if pulls:
            embed.add_field(name=f"Last {len(pulls)} PRs", value=HackSquad.pr_formatter(pulls))
        embed.set_thumbnail(url=avatar_url)

        return embed

    @app_commands.command()
    async def leaderboard(self, interaction: Interaction, *, page: int):
        """
        Show the leaderboard of HackSquad 2022!
        """
        if page <= 0:
            await interaction.response.send_message("The page cannot be negative or 0.")
            return
        await interaction.response.defer()

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
        await interaction.followup.send(f"```diff\n{msg}\n```")

    @app_commands.command()
    async def team(self, interaction: Interaction, *, team_slug: str):
        """
        Get the details of a team participating in Hacksquad 2022!

        Use the "Slug" as the team's name.
        """
        await interaction.response.defer()

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

        await interaction.followup.send(embed=embed)

    @app_commands.command(name="search")
    async def search_team(self, interaction: Interaction, *, query: str):
        """
        Try to search for a team in the leaderboard.
        """
        if len(query) <= 3:
            await interaction.response.send_message(
                "The query needs to be more than 3 characters long."
            )
            return

        await interaction.response.defer()

        results = await Requester().fetch_leaderboard()

        matching = [x for x in results if query in x["name"]]

        if not matching:
            await interaction.followup.send("No results were found.")
            return

        list_str = "\n\n".join(
            f"- Name: {match['name']}\n- Slug: {match['slug']}" for match in matching
        )
        if len(list_str) > 2000:
            await interaction.followup.send(
                "Too much results were found, try to refine your query."
            )
            return
        await interaction.followup.send(
            f"__Results of {len(matching)} matchs:__\n\n```\n{list_str}\n```"
        )

    @app_commands.command()
    async def hero(self, interaction: discord.Interaction, *, hero: str):
        """
        Show the details of an hero that have contributed to Novu.
        """
        await interaction.response.defer()

        contributors = await Requester().fetch_contributors()

        for contributor in contributors:
            if contributor["github"].lower() == hero.lower():
                await interaction.followup.send(embed=self.hero_embed_formatter(contributor))
                return

        await interaction.followup.send(content="Sorry, this hero was not found :( Try again!")

    @app_commands.command()
    async def randomhero(self, interaction: Interaction):
        """
        Show the details of a random hero who have contributed to Novu.
        """
        await interaction.response.defer()

        contributors = await Requester().fetch_contributors()
        contributor = random.choice(contributors)

        await interaction.followup.send(  # type: ignore
            content="", embed=self.hero_embed_formatter(contributor)
        )
