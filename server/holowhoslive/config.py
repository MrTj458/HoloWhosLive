import os
from functools import lru_cache
from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    dev: bool = bool(os.getenv('DEV'))
    database_url: AnyUrl = os.getenv('DATABASE_URL')
    redis_url: AnyUrl = os.getenv('REDIS_URL')
    youtube_api_key: str = os.getenv('YOUTUBE_API_KEY')


@lru_cache()
def get_settings() -> Settings:
    return Settings()
