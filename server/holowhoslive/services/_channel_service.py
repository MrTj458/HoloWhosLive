import logging
import pickle
from typing import List
from fastapi import Depends
from aioredis import Redis

from holowhoslive.services import YoutubeService, TwitchService
from holowhoslive.dependencies import get_redis
from holowhoslive.schemas import ChannelSchema, ChannelCreateSchema, ChannelApiSchema
from holowhoslive.models import Channel


class ChannelService:
    def __init__(
        self,
        yt_service: YoutubeService = Depends(YoutubeService),
        twitch_service: TwitchService = Depends(TwitchService),
        r: Redis = Depends(get_redis),
    ) -> None:
        self.yt_service = yt_service
        self.twitch_service = twitch_service
        self.r = r
        self.log = logging.getLogger("uvicorn")

    async def get_all(self) -> List[ChannelSchema]:
        return await ChannelSchema.from_queryset(Channel.all())

    async def get(self, id: int) -> ChannelSchema:
        return await ChannelSchema.from_queryset_single(Channel.get(id=id))

    async def add(self, channel: ChannelCreateSchema) -> ChannelSchema:
        db_channel = await Channel.create(**channel.dict())
        return await ChannelSchema.from_tortoise_orm(db_channel)

    async def update(self, id: int, channel: ChannelSchema) -> None:
        await Channel.filter(id=id).update(**channel.dict(exclude_unset=True))

    async def delete(self, id: int) -> None:
        await Channel.filter(id=id).delete()

    async def get_api_data(self) -> List[ChannelApiSchema]:
        channels = await self.r.get("cached_channels")
        if channels:
            return pickle.loads(channels)

        self.log.info("Fetching from APIs")
        channels = [
            *(await self.twitch_service.get_twitch_data()),
            *(await self.yt_service.get_youtube_data()),
        ]

        await self.r.setex(
            "cached_channels",
            "300",
            pickle.dumps([channel.dict() for channel in channels]),
        )

        return channels
