import os
import redis
from holowhoslive.config import get_settings

settings = get_settings()

def get_redis():
    r = redis.Redis(host=settings.redis_host, port=settings.redis_port, db=settings.redis_db)
    try:
        yield r
    finally:
        r.close()
