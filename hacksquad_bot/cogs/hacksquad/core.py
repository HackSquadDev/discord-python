import discord
from discord.ext import commands, menus

from hacksquad_bot.main import Context, HackSquadBot

from .menu import PageLeaderboard
from .utils import PRStatus, Requester


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
    async def team(self, ctx: Context, *, team_name: str):
        """
        Get the details of a team participating in Hacksquad 2022!

        Use the "Slug" as the team's name.
        """
        results = await Requester().fetch_team(team_name)

        embed = discord.Embed(title=f"Team: {results['name']}")

        if results["owner"]:
            embed.set_thumbnail(url=results["owner"]["image"])
            embed.add_field(name="Created By", value=results["owner"]["name"])

        embed.add_field(name="Team ID", value=results["id"])
        embed.add_field(name="Team slug", value=results["slug"])

        total_prs = results["prs"]
        accepted = [pr for pr in results["prs"] if pr["status"] == PRStatus.ACCEPTED]
        deleted = [pr for pr in results["prs"] if pr["status"] == PRStatus.DELETED]

        embed.description = f"The team `{results['name']}` has realized a total of `{len(total_prs)}` pull requests, which `{len(accepted)}` are accepted and `{len(deleted)}` are deleted from the competition. (Deletion ratio: `{round(len(total_prs) / len(deleted), 1)}%`)"

        last_3_prs = [pr for pr in total_prs[-3:] if pr["status"] == PRStatus.ACCEPTED]

        # sourcery skip: use-named-expression
        prs_str = "\n".join([f"**[{pr['title']}]({pr['url']})**" for pr in last_3_prs])

        if prs_str:
            embed.description += f"\n\n**{len(last_3_prs)} last accepted PRs:**\n{prs_str}"

        await ctx.send(embed=embed)

    @commands.hybrid_command()
    async def hero(self, ctx: Context, *, hero: str):
        """
        Show the details of heros who have contributed to Hacksquad 2022!
        """
        await ctx.send("The hero is a work-in-progress! Check back later!")
