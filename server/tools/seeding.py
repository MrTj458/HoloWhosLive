import json
import httpx


def seed_channels():
    with open("tools/channels.json") as f:
        channels = json.load(f)
    for channel in channels:
        httpx.post("http://localhost:8000/api/channels", json=channel)
    print("Channels seeded!")


if __name__ == "__main__":
    seed_channels()
