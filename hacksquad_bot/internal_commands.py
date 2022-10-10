import time
from typing import Optional

import discord
from discord import Guild, Interaction, app_commands
from discord.ext import commands, menus
from discord.ext.menus.views import ViewMenu

from hacksquad_bot.main import Context, HackSquadBot


class MyMenu(ViewMenu):
    async def send_initial_message(self, interaction: Interaction, channel):
        global home_embed
        home_embed = discord.Embed(title="Hacksquad Help Menu", color=discord.Color.random())
        home_embed.set_author(
            name=f"{interaction.message.author}",
            icon_url=f"{interaction.message.author.avatar.url}",
        )
        home_embed.set_thumbnail(url="https://i.imgur.com/kDynel4.png")
        home_embed.add_field(
            name="🦸🏻 Hero:", value="Get information about our beloved heros ❤️", inline=False
        )
        home_embed.add_field(
            name="🏅 Leaderboard:", value="Who is the best of the best?", inline=False
        )
        home_embed.add_field(name="🧑‍🤝‍🧑 Team:", value="Get information about teams", inline=False)

        return await self.send_with_view(channel, embed=home_embed)

    @menus.button("\N{HOUSE WITH GARDEN}")
    async def on_home(self, interaction):
        await interaction.followup.send(embed=home_embed)

    @menus.button("\N{SPORTS MEDAL}")
    async def help_lb(self, interaction):  # LIGMA BALLS
        embed = discord.Embed(title="Hacksquad Help Menu", color=discord.Color.random())
        embed.add_field(
            name="__Leaderboard:__",
            value="`/leaderboard`\nTop teams participating in hacksquad 2022",
            inline=False,
        )
        embed.set_author(
            name=f"{interaction.message.author}",
            icon_url=f"{interaction.message.author.avatar.url}",
        )
        await interaction.followup.send(embed=embed)

    @menus.button("\N{SUPERHERO}\N{EMOJI MODIFIER FITZPATRICK TYPE-1-2}")
    async def help_hero(self, interaction):
        embed = discord.Embed(title="Hacksquad Help Menu", color=discord.Color.random())
        embed.add_field(
            name="__Hero:__",
            value="`/hero`\nGet information about our beloved heros ❤️",
            inline=False,
        )
        embed.add_field(
            name="__RandomHero:__", value="`/randomhero`\nGet a random hero", inline=False
        )
        embed.set_author(
            name=f"{interaction.message.author}",
            icon_url=f"{interaction.message.author.avatar.url}",
        )
        await interaction.followup.send(embed=embed)

    @menus.button("\N{ADULT}\N{ZERO WIDTH JOINER}\N{HANDSHAKE}\N{ZERO WIDTH JOINER}\N{ADULT}")
    async def help_teams(self, interaction):
        embed = discord.Embed(title="Hacksquad Help Menu", color=discord.Color.random())
        embed.add_field(
            name="__Teams:__",
            value="`/team`\nGet information about the teams with their slug",
            inline=False,
        )
        embed.set_author(
            name=f"{interaction.message.author}",
            icon_url=f"{interaction.message.author.avatar.url}",
        )
        await interaction.followup.send(embed=embed)

    @menus.button("\N{BLACK SQUARE FOR STOP}\ufe0f")
    async def on_stop(self, interaction):
        await interaction.message.delete()
        self.stop()


class InternalCommands(commands.Cog):
    def __init__(self, bot: HackSquadBot) -> None:
        self.bot = bot
        self.bot.remove_command("help")

    @commands.command()
    async def help(self, ctx: commands.Context) -> None:
        """Sends the help message"""
        await MyMenu().start(ctx)

    @app_commands.command()
    async def ping(self, interaction: Interaction) -> None:
        """Show the ping of the bot"""
        start = time.monotonic()
        await interaction.response.defer()
        end = time.monotonic()
        overall = round((end - start) * 1000, 1)
        ws = round(self.bot.latency * 1000, 1)
        e = discord.Embed(
            title="Pong! :ping_pong:",
            description=f"Websocket latency: {ws}ms\nOverall latency: {overall}ms\nAverage latency: {round((overall+ws)/2, 1)}ms",
            color=discord.Colour.random(),
        )

        await interaction.followup.send(embed=e)

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
            await ctx.send(f"Could not load cog due to an unexpected error:\n```py\n{e}```")
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
            await ctx.send(f"Could not reload cog due to an unexpected error:\n```py\n{e}```")
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
            await ctx.send(f"Could not unload cog due to an unexpected error:\n```py\n{e}```")
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
