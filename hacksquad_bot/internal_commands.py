from typing import Optional

from discord import Guild
from discord.ext import commands

from hacksquad_bot.main import Context, HackSquadBot


class InternalCommands(commands.Cog):
    def __init__(self, bot: HackSquadBot) -> None:
        self.bot = bot

    @commands.command(name="load")
    async def cmd_load_extension(self, ctx: Context, *, cog_name: str):
        """
        Attempt to load a cog.

        Parameters
        ----------
        cog_name : str
            The cog to load.
        """
        try:
            await self.bot.load_extension(f"hacksquad_bot.cogs.{cog_name}")
        except commands.errors.ExtensionAlreadyLoaded:
            await ctx.send("This extension is already loaded.")
            return
        except commands.errors.ExtensionNotFound:
            await ctx.send("Cannot find extension.")
            return
        except Exception as e:
            await ctx.send(
                f"Could not load cog due to an unexpected error:\n```py\n{e}```"
            )
            return
        await ctx.send(f"Succesfully loaded `{cog_name}`.")

    @commands.command(name="reload")
    async def cmd_reload_extension(self, ctx: Context, *, cog_name: str):
        """
        Attempt to reload a cog.

        Parameters
        ----------
        cog_name : str
            The cog to reload.
        """
        try:
            await self.bot.reload_extension(f"hacksquad_bot.cogs.{cog_name}")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send("This extension is not loaded.")
            return
        except commands.errors.ExtensionNotFound:
            await ctx.send("Cannot find extension.")
            return
        except Exception as e:
            await ctx.send(
                f"Could not reload cog due to an unexpected error:\n```py\n{e}```"
            )
            return
        await ctx.send(f"Succesfully reloaded `{cog_name}`.")

    @commands.command(name="unload")
    async def cmd_unload_extension(self, ctx: Context, *, cog_name: str):
        """
        Attempt to unload a cog.
        """
        try:
            await self.bot.unload_extension(f"hacksquad_bot.cogs.{cog_name}")
        except commands.errors.ExtensionNotLoaded:
            await ctx.send("This extension is not loaded.")
            return
        except commands.errors.ExtensionNotFound:
            await ctx.send("Cannot find extension.")
            return
        except Exception as e:
            await ctx.send(
                f"Could not unload cog due to an unexpected error:\n```py\n{e}```"
            )
            return
        await ctx.send(f"Succesfully unloaded `{cog_name}`.")

    @commands.is_owner()
    @commands.command(name="sync")
    async def cmd_sync(self, ctx: Context, *, guild: Optional[Guild]):
        """
        Sync slash commands globally or in a server.
        """
        msg = await ctx.send(
            f"Syncing slash commands for guild {guild.name}..."
            if guild
            else "Syncing slash commands... Please wait, this might take a while..."
        )
        await self.bot.tree.sync(guild=guild)
        await msg.edit(
            content=f"Successfully synced slash for guild {guild.name}"
            if guild
            else "Successfully synced slash!"
        )


async def setup(bot: HackSquadBot):
    cog = InternalCommands(bot)
    await bot.add_cog(cog)
