import asyncio
import httpx
from typing import List
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from holowhoslive.dependencies import get_db, get_yt_service
from holowhoslive.models import YtChannel
from holowhoslive.schemas import (
    YtChannelCreateSchema,
    YtChannelSchema,
    YtChannelImageSchema,
)


class YoutubeService:
    def __init__(
        self, db: AsyncSession = Depends(get_db), yt_client=Depends(get_yt_service)
    ):
        self.db = db
        self.yt_client = yt_client

    async def get_all_data(self) -> List[YtChannelSchema]:
        """
        Get all of the channel data from Youtube for the channels saved in the database.
        """
        db_channels = await self.db.execute(select(YtChannel))
        db_channels = db_channels.scalars().all()
        yt_data = self._get_yt_data(db_channels)

        # In parallel, grab all needed data and create list of channels
        channels = await asyncio.gather(
            *[self._create_channel(channel, yt_data) for channel in db_channels]
        )

        return channels

    async def get_all_db_data(self) -> List[YtChannelSchema]:
        """Get Youtube channel data that is saved in db"""
        channels = await self.db.execute(select(YtChannel))
        return channels.scalars().all()

    async def get(self, id: int):
        """Get a single channel from the database"""
        channel = await self.db.execute(select(YtChannel).where(YtChannel.id == id))
        return channel.scalars().first()

    async def add(self, channel: YtChannelCreateSchema) -> YtChannel:
        """Add new Channel to the database"""
        db_channel = YtChannel(**channel.dict())
        self.db.add(db_channel)
        await self.db.commit()
        await self.db.refresh(db_channel)
        return db_channel

    async def delete(self, id: int):
        """Delete a Youtube channel from the database"""
        channel = await self.get(id)
        await self.db.delete(channel)
        await self.db.commit()

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
        new_channel = YtChannelSchema(
            **channel.__dict__,
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
