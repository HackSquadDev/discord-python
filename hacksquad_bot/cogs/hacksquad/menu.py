from typing import Iterable

from discord.ext import menus
from tabulate import tabulate

from hacksquad_bot.cogs.hacksquad.utils import PartialTeam


class PageLeaderboard(menus.ListPageSource):
    def __init__(self, entries: Iterable[PartialTeam]):
        super().__init__(entries, per_page=10)

    async def format_page(self, menu: menus.MenuPages, page: Iterable[PartialTeam]) -> str:
        for value in page:
            if value.get("id"):
                value.pop("id")  # type: ignore (Weird error here ("k" not assignable to "Never"))

        elements = [value.values() for value in page]

        table = tabulate(
            elements, headers=["Place", "Team Name", "Score", "Slug"], tablefmt="pretty"
        )
        return f"```\n{table}\n```"
