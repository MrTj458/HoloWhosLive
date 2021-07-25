import os
import json
import requests
import redis
from dotenv import load_dotenv

load_dotenv()


def seed_channels():
    with open('channels.json') as f:
        channels = json.load(f)
    for channel in channels:
        requests.post('http://localhost:8000/youtube/channels', json=channel)
    print('Channels seeded!')


def seed_debug_values():
    r = redis.Redis(host=os.getenv('REDIS_HOST'), port=os.getenv(
        'REDIS_PORT'), db=os.getenv('REDIS_BD'))
    with open('all_live.json') as f:
        data = json.load(f)
        r.set('all_live', json.dumps(data))

    with open('some_live.json') as f:
        data = json.load(f)
        r.set('some_live', json.dumps(data))

    with open('all_offline.json') as f:
        data = json.load(f)
        r.set('all_offline', json.dumps(data))


if __name__ == '__main__':
    # seed_channels()
    seed_debug_values()
