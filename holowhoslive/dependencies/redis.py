import os
import redis

def get_redis():
    r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv('REDIS_PORT'), db=os.getenv('REDIS_BD'))
    try:
        yield r
    finally:
        r.close()
