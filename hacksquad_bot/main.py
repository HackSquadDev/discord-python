import logging
import os

import discord
from discord.ext import commands

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
            command_prefix=os.environ.get("PREFIX") or "!",
            description=DESCRIPTION,
            intents=discord.Intents.all(),
        )

    async def setup_hook(self) -> None:
        for extension in EXTENSIONS:
            try:
                await self.load_extension(f"hacksquad_bot.{extension}")
            except Exception:
                logging.exception('Could not load "%s" due to an error', extension)
        await self.load_extension("jishaku")
        # await self.tree.sync()

    async def on_command_error(  # type: ignore
        self,
        context: commands.Context["HackSquadBot"],
        exception: commands.errors.CommandError,
        /,
    ):
        if isinstance(exception, commands.UserInputError):
            await context.send_help(context.command)
            return
        if isinstance(exception, commands.errors.CommandNotFound):
            return
        await context.send(
            f"`Unexpected error in command {context.command}`\n```py\n{exception}```"
        )
        return await super().on_command_error(context, exception)


Context = commands.Context[HackSquadBot]
