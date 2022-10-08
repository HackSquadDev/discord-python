import logging
from typing import List, TypedDict

import discord
from discord import Interaction, app_commands
from discord.ext import commands
from tabulate import tabulate

from hacksquad_bot.main import HackSquadBot

from .utils import HACKSQUAD_COLOR, PRStatus, Requester, ResponseError


class HackSquad(commands.Cog):
    def __init__(self, bot: HackSquadBot) -> None:
        self.bot = bot

    @app_commands.command()
    async def leaderboard(self, interaction: Interaction, *, page: int):
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
        await interaction.response.send_message(
            "The hero is a work-in-progress! Check back later!"
        )

    async def cog_app_command_error(
        self, interaction: discord.Interaction, error: discord.app_commands.AppCommandError
    ) -> None:
        if isinstance(error, discord.app_commands.errors.CommandInvokeError) and isinstance(
            error.original, ResponseError
        ):
            if error.original.code == 404:
                await interaction.response.send_message(
                    content="Your search returned no result! Double check your command."
                )
            else:
                await interaction.response.send_message(
                    content="An unexpected error happened with the HackSquad API, can't tell what, however... Sorry!"
                )
            return
        logging.exception(error)
        await interaction.response.send_message(
            f"`Unexpected error in command {interaction.command.name if interaction.command else 'not a command'}`\n```py\n{error}```"
        )
