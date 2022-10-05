import contextlib
import os

from hacksquad_bot.main import HackSquadBot

with contextlib.suppress(ImportError):
    from dotenv import load_dotenv  # type: ignore

    load_dotenv()

bot = HackSquadBot()
bot.run(os.environ["TOKEN"])
