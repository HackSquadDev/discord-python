from .core import HackSquad
from hacksquad_bot.main import HackSquadBot


async def setup(bot: HackSquadBot):
    cog = HackSquad(bot)
    await bot.add_cog(cog)
