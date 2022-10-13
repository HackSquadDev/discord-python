import logging
import random
from typing import List, TypedDict

import discord
from discord import Interaction, app_commands
from discord.ext import commands
from rapidfuzz import process

from hacksquad_bot.cogs.hacksquad.utils import Requester
from hacksquad_bot.main import HackSquadBot

from .utils import HACKSQUAD_COLOR, NovuContributor, PRStatus, Requester, ResponseError

SOME_RANDOM_ASS_QUOTES = [
    "Seriously... If you're gonna win, can you... give me one of your shirt?",
    "Hacktoberfest's nice. Hacksquad's better.",
    "I like #memes. No seriously, it's too good.",
    "btw i use arch",
    "Wait. Open Source is just for the free T-shirt? Always has been.",
    "I'm number #0 in the leaderboard bro! Who can win against me, the great HackSquad bot??",
    "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA",
    "E.",
    "I see no God up here. OTHER THAN ME!",
    "I have no idea what I'm doing...",
    "I am a NFT.",
    'Why is this variable called "SOME_RANDOM_ASS_QUOTES"? I\'m legit NOT LYING!',
    "What a Wonderful World",
    "Nevo David is awesome, don't you think?",
    "Thank you, Nevo David, HellFire, sravan, Santosh, Midka, and Capt. Pred for making me alive :)",
    "imma just .pop the line where I say nevo david is awesome... but he's so handsome tho...",
    "Hey Mods, can you be a huge freaking favor? Can you literally start banning anyone that does spammy PRs? David can you tell them.",
    "Yes, all of those quotes are not funny. Made by someone not funny.",
    "I'm not an AI, I'm just a randomly picked, stupid string!",
    "skill issue!",
]


class HackSquad(commands.Cog):
    def __init__(self, bot: HackSquadBot) -> None:
        self.bot = bot

    @app_commands.command()
    @app_commands.describe(page="Ping the bot")
    async def ping(self, interaction: Interaction) -> None:
        await interaction.response.send_message("Pong!")

    @staticmethod
    def hero_embed_formatter(contributor: NovuContributor) -> discord.Embed:
        name = f"Hero: {contributor['name']}" or "Name not found"

        last_3_pulls = contributor["pulls"][-3:]

        embed = discord.Embed(
            title=f"{name}",
            color=HACKSQUAD_COLOR,
        )
        embed.add_field(
            name="GitHub",
            value=f"[{contributor['github']}](https://github.com/{contributor['github']})",
        )
        embed.add_field(name="Total PRs", value=contributor["total_pulls"])
        embed.add_field(
            name="Total PRs in the last 3 months", value=contributor["total_last_3_months_pulls"]
        )

        if last_3_pulls:
            embed.description = f"**{len(last_3_pulls)} last PRs:**\n\n" + "\n".join(
                f"[{pr['title']}]({pr['url']})" for pr in last_3_pulls
            )
        else:
            embed.description = "No PRs found..."

        embed.set_thumbnail(url=contributor["avatar_url"])
        embed.set_footer(
            text=f"A Novu Hero: {contributor['bio'] or 'No bio'}",
            icon_url="https://i.imgur.com/zXAbZMC.png",
        )

        return embed

    @app_commands.command()
    @app_commands.describe(page="The page to show.")
    async def leaderboard(
        self, interaction: Interaction, *, page: app_commands.Range[int, 1, None] = 1
    ):
        """
        Show the leaderboard of HackSquad 2022!
        """
        if page <= 0:
            await interaction.response.send_message("The page cannot be negative or 0.")
            return
        await interaction.response.defer()

        page -= 1

        class MinifiedPartialTeam(TypedDict):
            place: int
            name: str
            score: int
            slug: str

        results = await Requester().fetch_leaderboard()
        results.sort(key=lambda x: x["score"], reverse=True)

        teams: List[MinifiedPartialTeam] = [
            MinifiedPartialTeam(
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
        embed = discord.Embed(
            title="Leaderboard - HackSquad 2022",
            color=HACKSQUAD_COLOR,
            url="https://hacksquad.dev/leaderboard",
        )

        embed.description = "\n".join(
            f"`{team['place']}` : [`{team['name']}`](https://hacksquad.dev/team/{team['slug']}) with a score of **{team['score']}** PRs  (Slug: `{team['slug']}`)"
            for team in teams
        )

        embed.set_footer(
            text=f"Page {page + 1}/{len(list_of_teams)}\n{random.choice(SOME_RANDOM_ASS_QUOTES)}",
            icon_url="https://i.imgur.com/kDynel4.png",
        )

        await interaction.followup.send(embed=embed)

    @app_commands.command()
    @app_commands.describe(
        team_slug="The team's slug. You can find it by searching or in the leaderboard."
    )
    async def team(self, interaction: Interaction, *, team_slug: str):
        """
        Get the details of a team participating in Hacksquad 2022!

        Use the "Slug" as the team's name.
        """
        await interaction.response.defer()

        results = await Requester().fetch_team(team_slug)

        embed = discord.Embed(
            title=f"Team: {results['name']}",
            url=f"https://hacksquad.dev/team/{results['slug']}",
            color=HACKSQUAD_COLOR,
        )

        if results["owner"]:
            embed.set_thumbnail(url=results["owner"]["image"])
            embed.add_field(name="Created By", value=results["owner"]["name"])

        embed.add_field(name="Team ID", value=results["id"])
        embed.add_field(name="Team slug", value=results["slug"])
        embed.add_field(name="Disqualified", value="Yes" if results["disqualified"] else "No")

        embed.add_field(
            name=f"Members ({len(results['users'])})",
            value=(
                "\n".join(
                    f"- [{user['name']}](https://github.com/{user['handle']}) ({user['handle']})"
                    for user in results["users"]
                )
            ),
        )

        results["prs"].sort(key=lambda x: x["created_at"])

        total_prs = results["prs"]
        accepted = [pr for pr in results["prs"] if pr["status"] == PRStatus.ACCEPTED]
        deleted = [pr for pr in results["prs"] if pr["status"] == PRStatus.DELETED]

        prs_ratio = round((len(deleted) / len(total_prs)) * 100, 1)
        embed.description = f"The team `{results['name']}` has realized a total of `{len(total_prs)}` pull requests, which `{len(accepted)}` are accepted and `{len(deleted)}` are deleted from the competition.\n(Deletion ratio: `{prs_ratio}%`)"

        last_3_prs = accepted[-3:]

        if prs_str := "\n".join([f"**[{pr['title']}]({pr['url']})**" for pr in last_3_prs]):
            embed.description += f"\n\n**{len(last_3_prs)} last accepted PRs:**\n{prs_str}"

        await interaction.followup.send(embed=embed)

    @team.autocomplete("team_slug")
    async def team_slug_autocomplete(
        self, _: discord.Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        result = await Requester().fetch_leaderboard()
        return [
            app_commands.Choice(name=team["name"], value=team["slug"])
            for team in result
            if current.lower() in team["name"].lower()
        ][:25]

    @app_commands.command(name="search")
    @app_commands.describe(query="Your search query")
    async def search_team(self, interaction: Interaction, *, query: str):
        """
        Try to search for a team in the leaderboard.
        """
        await interaction.response.defer()

        results = await Requester().fetch_leaderboard()

        matching = process.extract(query, [team["name"] for team in results], limit=10)

        if not matching:
            await interaction.followup.send("No results were found.")
            return

        embed = discord.Embed(
            title=f"Search Result ({len(matching)} match)",
            color=HACKSQUAD_COLOR,
        )

        embed.description = "\n".join(
            f"`{place}` - `{match[0]}` (Percentage Match: `{round(match[1], 1)}%`)"
            for place, match in enumerate(matching, 1)
        )

        # list_str = "\n\n".join(
        #     f"- Name: {match['name']}\n- Slug: {match['slug']}" for match in matching
        # )
        await interaction.followup.send(
            # f"__Results of {len(matching)} match:__\n\n```\n{list_str}\n```"
            embed=embed
        )

    @app_commands.command()
    async def hero(self, interaction: discord.Interaction, *, hero: str):
        """
        Show the details of an hero that have contributed to Novu.
        """
        await interaction.response.defer()

        contributor = await Requester().fetch_contributor(hero)

        await interaction.followup.send(embed=self.hero_embed_formatter(contributor))

    @hero.autocomplete("hero")
    async def hero_autocomplete(
        self, _: discord.Interaction, current: str
    ) -> List[app_commands.Choice[str]]:
        result = await Requester().fetch_contributors_mini()
        return [
            app_commands.Choice(name=contributor["github"], value=contributor["github"])
            for contributor in result
            if current.lower() in contributor["github"].lower()
        ][:25]

    @app_commands.command()
    async def randomhero(self, interaction: Interaction):
        """
        Show the details of a random hero who have contributed to Novu.
        """
        await interaction.response.defer()

        contributors = await Requester().fetch_contributors_mini()
        random_contributor = random.choice(contributors)
        contributor = await Requester().fetch_contributor(random_contributor["github"])

        await interaction.followup.send(content="", embed=self.hero_embed_formatter(contributor))

    async def cog_app_command_error(
        self, interaction: discord.Interaction, error: app_commands.AppCommandError
    ) -> None:
        if isinstance(error, app_commands.CommandInvokeError) and isinstance(
            error.original, ResponseError
        ):
            if error.original.code == 404:
                await interaction.followup.send(
                    "Could not find what you're looking for :( Try again!"
                )
            else:
                await interaction.followup.send(
                    f"An unexpected error happened with the HackSquad API: Status code: {error.original.code}"
                )
            return
        logging.exception(error)
        await interaction.followup.send(f"Unexpected error:\n\n```py\n{error}\n```")
