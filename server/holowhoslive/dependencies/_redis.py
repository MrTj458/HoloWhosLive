import aioredis
from holowhoslive.config import get_settings

settings = get_settings()


async def get_redis():
    async with aioredis.from_url(settings.redis_url) as r:
        yield r
