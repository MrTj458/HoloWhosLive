import json
import requests


def seed_channels():
    with open('tools/channels.json') as f:
        channels = json.load(f)
    for channel in channels:
        requests.post('http://localhost:8000/api/youtube/channels', json=channel)
    print('Channels seeded!')


if __name__ == '__main__':
    seed_channels()
