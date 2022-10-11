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

        if self.extra_events.get("on_command_error", None):
            return

        # Basically https://github.com/Rapptz/discord.py/pull/8991
        if context.cog:
            if context.interaction and context.cog.has_app_command_error_handler():
                return
            if not context.interaction and context.cog.has_error_handler():
                return

        if context.interaction:
            await context.interaction.response.send_message(
                f"`Unexpected error in command {context.command}`\n```py\n{exception}```"
            )
        else:
            await context.send(
                f"`Unexpected error in command {context.command}`\n```py\n{exception}```"
            )


Context = commands.Context[HackSquadBot]
