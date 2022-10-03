import logging
import os

import discord
from discord.ext import commands


DESCRIPTION = """
Hey there! I am the discord.py version of the HackSquad Bot! Nice to meeeeeeeet you!
"""
EXTENSIONS = (
    'internal_commands',
    'cogs.hacksquad',
)


class HackSquadBot(commands.AutoShardedBot):
    def __init__(self) -> None:
        super().__init__(
            command_prefix=os.environ['PREFIX'] or "!",
            description=DESCRIPTION,
            intents=discord.Intents.all()
        )

    async def setup_hook(self) -> None:
        for extension in EXTENSIONS:
            try:
                await self.load_extension(f"hacksquad_bot.{extension}")
            except Exception:
                logging.exception("Could not load \"%s\" due to an error", extension)
        await self.tree.sync()

    async def on_command_error(self, context: commands.Context["HackSquadBot"], exception: commands.errors.CommandError, /):
        if isinstance(exception, commands.errors.CommandNotFound):
            return
        return await super().on_command_error(context, exception)

Context = commands.Context[HackSquadBot]

# @bot.event
# async def on_ready():
#     await bot.load_extension("jishaku")
#     print("Bot is running as {0.user}".format(bot))

# @bot.hybrid_command()
# async def ping(ctx):
#     await ctx.send("Pong!")

# @bot.command()
# @commands.has_permissions(administrator=True)
# async def sync(ctx):
#     await bot.tree.sync()
#     await ctx.send("Synced")
