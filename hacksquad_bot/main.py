import logging
import os

import discord
from discord.ext import commands
from jishaku.cog import Jishaku


DESCRIPTION = """
Hey there! I am the discord.py version of the HackSquad Bot! Nice to meeeeeeeet you!
"""
EXTENSIONS = (
    "internal_commands",
    "cogs.hacksquad",
)


class HackSquadBot(commands.AutoShardedBot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=os.environ["PREFIX"] or "!",
            description=DESCRIPTION,
            intents=discord.Intents.all(),
        )

    async def setup_hook(self) -> None:
        for extension in EXTENSIONS:
            try:
                await self.load_extension(f"hacksquad_bot.{extension}")
            except Exception:
                logging.exception('Could not load "%s" due to an error', extension)
        await self.add_cog(Jishaku(bot=self))
        await self.tree.sync()

    async def on_command_error(
        self,
        context: commands.Context["HackSquadBot"],
        exception: commands.errors.CommandError,
        /,
    ):
        if isinstance(exception, commands.errors.CommandNotFound):
            return
        return await super().on_command_error(context, exception)


Context = commands.Context[HackSquadBot]
