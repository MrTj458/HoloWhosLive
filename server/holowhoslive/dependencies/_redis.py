from redis import Redis
from holowhoslive.config import get_settings

settings = get_settings()


def get_redis():
    with Redis.from_url(settings.redis_url) as r:
        yield r
