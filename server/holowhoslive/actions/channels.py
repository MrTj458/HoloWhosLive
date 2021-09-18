import asyncio
import httpx
from typing import List
from sqlalchemy.orm import Session

from holowhoslive.models import Channel
from holowhoslive.schemas.channel import ChannelImageSchema, ChannelSchema


def _get_yt_data(channels, yt_service):
    channel_ids = [channel.channel_id for channel in channels]

    # Youtube API only allows for 50 channels at a time, split the array into groups of 50
    split_ids = [channel_ids[i:i+50] for i in range(0, len(channel_ids), 50)]

    channel_data = []

    for arr in split_ids:
        yt_request = yt_service.channels().list(
            id=arr, part='snippet,statistics')
        channel_data = [*channel_data, *yt_request.execute()['items']]

    return channel_data


async def _get_is_live(channel_id):
    async with httpx.AsyncClient() as client:
        res = await client.get(f'https://www.youtube.com/channel/{channel_id}')

    return '{"text":" watching"}' in res.text


async def _create_channel(channel, yt_data):
    # Find YT channel from list of channel data
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
        channel_name=yt_channel['snippet']['title'],
        subscribers=yt_channel['statistics']['subscriberCount'],
        is_live=await _get_is_live(channel.channel_id),
    )

    return new_channel

async def fetch_channel_data(db: Session, yt_service) -> List[ChannelSchema]:
    """
        Get all of the channel data from Youtube for the channels saved in the database.
    """
    db_channels = db.query(Channel).all()
    yt_data = _get_yt_data(db_channels, yt_service)

    # In parallel, grab all needed data and create list of channels
    channels = await asyncio.gather(*[_create_channel(channel, yt_data) for channel in db_channels])

    return channels
