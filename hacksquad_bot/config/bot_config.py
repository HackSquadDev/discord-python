from pydantic import BaseSettings


class BotConfig(BaseSettings):
    token: str
    prefix: str

    class Config:
        env_file = ".env"
        env_prefix = ""


bot_config = BotConfig()
