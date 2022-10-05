from hacksquad_bot.main import HackSquadBot

from .core import HackSquad


async def setup(bot: HackSquadBot):
    cog = HackSquad(bot)
    await bot.add_cog(cog)
