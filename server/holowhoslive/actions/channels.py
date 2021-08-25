import requests
from typing import List
from sqlalchemy.orm import Session

from holowhoslive.models import Channel
from holowhoslive.schemas.channel import ChannelImageSchema, ChannelSchema


def get_yt_data(channels, yt_service):
    channel_ids = [channel.channel_id for channel in channels]
    yt_request = yt_service.channels().list(
        id=channel_ids, part='snippet,statistics')

    return yt_request.execute()['items']


def get_is_live(channel_id):
    channel_text = requests.get(
        f'https://www.youtube.com/channel/{channel_id}').text

    return '{"text":" watching"}' in channel_text


def fetch_channel_data(db: Session, yt_service) -> List[ChannelSchema]:
    """
        Get all of the channel data from Youtube for the channels saved in the database.
    """
    db_channels = db.query(Channel).all()
    yt_data = get_yt_data(db_channels, yt_service)

    # Grab all needed data and create Channel object
    channels: List[ChannelSchema] = []

    for channel in db_channels:
        # Find the channel in the fetched YT data list
        yt_channel = list(
            filter(lambda c: c['id'] == channel.channel_id, yt_data))[0]

        # Build channel instance
        new_channel = ChannelSchema(
            **channel.__dict__,
            images=ChannelImageSchema(
                default=yt_channel['snippet']['thumbnails']['default']['url'],
                medium=yt_channel['snippet']['thumbnails']['medium']['url'],
                high=yt_channel['snippet']['thumbnails']['high']['url'],
            ),
            subscribers=yt_channel['statistics']['subscriberCount'],
            is_live=get_is_live(channel.channel_id),
        )

        channels.append(new_channel)

    return channels
