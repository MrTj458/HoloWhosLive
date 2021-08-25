import os
from functools import lru_cache
from pydantic import BaseSettings, AnyUrl


class Settings(BaseSettings):
    database_url: AnyUrl = os.getenv('DATABASE_URL')
    redis_host: str = os.getenv('REDIS_HOST')
    redis_port: str = os.getenv('REDIS_PORT')
    redis_db: str = os.getenv('REDIS_DB')
    youtube_api_key: str = os.getenv('YOUTUBE_API_KEY')


@lru_cache()
def get_settings() -> Settings:
    return Settings()
