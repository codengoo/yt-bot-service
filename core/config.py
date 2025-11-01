from functools import lru_cache
from pydantic import Field
from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    API_KEY: str = Field("se@cret0", description="Secret api key for calling service from outside")

    SHEET_ID_PHAT_NGUOI: str = Field("_",description="Shet id")

    DISCORD_BOT_TOKEN: str = Field("se@cret0", description="Discord bot token")
    DISCORD_CHANNEL_PHAT_NGUOI: str = Field("", description="Discord channel phat nguoi")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
