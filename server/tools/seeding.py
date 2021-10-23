import json
import httpx


def seed_groups():
    with open("tools/data/groups.json") as f:
        groups = json.load(f)
    for group in groups:
        try:
            httpx.post("http://localhost:8000/api/groups", json=group)
        except:
            print("Error seeding group: ", group)
    print("Groups seeded")


def seed_yt_channels():
    with open("tools/data/channels.json") as f:
        channels = json.load(f)
    for channel in channels:
        try:
            httpx.post("http://localhost:8000/api/channels", json=channel)
        except:
            print("Error seeding channel: ", channel)
    print("Youtube Channels seeded!")


if __name__ == "__main__":
    seed_groups()
    seed_yt_channels()
