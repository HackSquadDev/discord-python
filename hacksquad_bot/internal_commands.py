from discord.ext import commands

from hacksquad_bot.main import Context, HackSquadBot


class InternalCommands(commands.Cog):
    def __init__(self, bot: HackSquadBot) -> None:
        self.bot = bot

    @commands.command(name="reload")
    async def cmd_reload_extension(self, ctx: Context, *, cog_name: str):
        """
        Attempt to reload a cog.
        """
        try:
            await self.bot.reload_extension(f"hacksquad_bot.cogs.{cog_name}")
        except Exception as e:
            await ctx.send(f"Could not reload cog due to an unexpected error:\n```py\n{e}```")
            return
        await ctx.send(f"Succesfully reloaded `{cog_name}`.")

    @commands.command(name="sync")
    async def cmd_sync(self, ctx: Context):
        msg = await ctx.send("Syncing slash commands...")
        await self.bot.tree.sync()
        await msg.edit(content="Successfully synced slash!")

async def setup(bot: HackSquadBot):
    cog = InternalCommands(bot)
    await bot.add_cog(cog)
