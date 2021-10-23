import asyncio
import httpx
from typing import List
from fastapi import Depends

from holowhoslive.config import get_settings, Settings
from holowhoslive.models import Channel
from holowhoslive.schemas import ChannelApiSchema, ChannelSchema


class YoutubeService:
    def __init__(self, settings: Settings = Depends(get_settings)):
        self.settings = settings

    async def get_youtube_data(self) -> List[ChannelApiSchema]:
        """
        Get all of the channel data from Youtube for the channels saved in the database.
        """
        db_channels = await ChannelSchema.from_queryset(
            Channel.filter(platform="Youtube").all()
        )
        yt_data = await self._get_yt_data(db_channels)

        # In parallel, grab all needed data and create list of channels
        channels = await asyncio.gather(
            *[self._create_channel(channel, yt_data) for channel in db_channels]
        )

        return channels

    async def _get_yt_data(self, channels):
        """Fetch channel data from the Youtube API"""
        channel_ids = [channel.channel_id for channel in channels]

        # Youtube API only allows for 50 channels at a time, split the array into groups of 50
        split_ids = [channel_ids[i : i + 50] for i in range(0, len(channel_ids), 50)]

        channel_data = []

        for arr in split_ids:
            async with httpx.AsyncClient() as client:
                res = await client.get(
                    f"https://youtube.googleapis.com/youtube/v3/channels?key={self.settings.youtube_api_key}&part=snippet&part=statistics&id={'&id='.join(arr)}",
                    headers={
                        "Accept": "application/json",
                    },
                )
                channel_data = [*channel_data, *res.json()["items"]]

        return channel_data

    async def _get_is_live(self, channel_id):
        """Scrape the given channel to check if it is live or not"""
        async with httpx.AsyncClient() as client:
            res = await client.get(f"https://www.youtube.com/channel/{channel_id}")

        return '{"text":" watching"}' in res.text

    async def _create_channel(self, channel, yt_data):
        """Create channel instance combining data from database and Youtube API"""
        # Find YT channel from list of channel data
        yt_channel = list(filter(lambda c: c["id"] == channel.channel_id, yt_data))[0]

        # Build channel instance
        new_channel = ChannelApiSchema(
            **channel.dict(),
            image=yt_channel["snippet"]["thumbnails"]["medium"]["url"],
            display_name=yt_channel["snippet"]["title"],
            subscribers=yt_channel["statistics"]["subscriberCount"],
            is_live=await self._get_is_live(channel.channel_id),
        )

        return new_channel
