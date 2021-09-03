import os
from redis import Redis
from holowhoslive.config import get_settings

settings = get_settings()


def get_redis():
    r = Redis.from_url(settings.redis_url)
    try:
        yield r
    finally:
        r.close()
