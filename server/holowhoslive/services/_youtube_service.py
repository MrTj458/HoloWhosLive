import asyncio
import httpx
from typing import List
from fastapi import Depends

from holowhoslive.dependencies import get_yt_service
from holowhoslive.models import YtChannel
from holowhoslive.schemas import (
    YtChannelCreateSchema,
    YtChannelSchema,
    YtChannelImageSchema,
    YtChannelApiSchema,
)


class YoutubeService:
    def __init__(self, yt_client=Depends(get_yt_service)):
        self.yt_client = yt_client

    async def get_youtube_data(self) -> List[YtChannelApiSchema]:
        """
        Get all of the channel data from Youtube for the channels saved in the database.
        """
        db_channels = await YtChannelSchema.from_queryset(YtChannel.all())
        yt_data = self._get_yt_data(db_channels)

        # In parallel, grab all needed data and create list of channels
        channels = await asyncio.gather(
            *[self._create_channel(channel, yt_data) for channel in db_channels]
        )

        return channels

    async def get_all(self) -> List[YtChannelSchema]:
        """Get Youtube channel data that is saved in db"""
        return await YtChannelSchema.from_queryset(YtChannel.all())

    async def get(self, id: int) -> YtChannelSchema:
        """Get a single channel from the database"""
        return await YtChannelSchema.from_queryset_single(YtChannel.get(id=id))

    async def add(self, channel: YtChannelCreateSchema) -> YtChannelSchema:
        """Add new Channel to the database"""
        db_channel = await YtChannel.create(**channel.dict())
        return await YtChannelSchema.from_tortoise_orm(db_channel)

    async def update(self, id: int, channel: YtChannelCreateSchema) -> None:
        await YtChannel.filter(id=id).update(**channel.dict(exclude_unset=True))

    async def delete(self, id: int):
        """Delete a Youtube channel from the database"""
        await YtChannel.filter(id=id).delete()

    def _get_yt_data(self, channels):
        """Fetch channel data from the Youtube API"""
        channel_ids = [channel.channel_id for channel in channels]

        # Youtube API only allows for 50 channels at a time, split the array into groups of 50
        split_ids = [channel_ids[i : i + 50] for i in range(0, len(channel_ids), 50)]

        channel_data = []

        for arr in split_ids:
            yt_request = self.yt_client.channels().list(
                id=arr, part="snippet,statistics"
            )
            channel_data = [*channel_data, *yt_request.execute()["items"]]

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
        new_channel = YtChannelApiSchema(
            **channel.dict(),
            images=YtChannelImageSchema(
                default=yt_channel["snippet"]["thumbnails"]["default"]["url"],
                medium=yt_channel["snippet"]["thumbnails"]["medium"]["url"],
                high=yt_channel["snippet"]["thumbnails"]["high"]["url"],
            ),
            channel_name=yt_channel["snippet"]["title"],
            subscribers=yt_channel["statistics"]["subscriberCount"],
            is_live=await self._get_is_live(channel.channel_id),
        )

        return new_channel
