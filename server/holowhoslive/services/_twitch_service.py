from fastapi import Depends
import httpx
from typing import List

from holowhoslive.config import get_settings, Settings
from holowhoslive.schemas import (
    TwitchChannelImageSchema,
    TwitchChannelSchema,
    TwitchChannelCreateSchema,
    TwitchChannelApiSchema,
)
from holowhoslive.models import TwitchChannel


class TwitchService:
    def __init__(self, settings: Settings = Depends(get_settings)) -> None:
        self.settings = settings

    async def get_twitch_data(self) -> List[TwitchChannelApiSchema]:
        db_channels = await TwitchChannelSchema.from_queryset(TwitchChannel.all())
        twitch_data = await self._get_twitch_data(db_channels)

        channels = []
        for channel in db_channels:
            twitch_channel = list(
                filter(
                    lambda c: c["login"] == channel.channel_id, twitch_data["user_info"]
                )
            )[0]

            is_live = channel.channel_id in [
                c["user_login"] for c in twitch_data["stream_info"]
            ]

            channels.append(
                TwitchChannelApiSchema(
                    **channel.dict(),
                    images=TwitchChannelImageSchema(
                        default=twitch_channel["profile_image_url"]
                    ),
                    view_count=twitch_channel["view_count"],
                    is_live=is_live,
                    display_name=twitch_channel["display_name"],
                )
            )

        return channels

    async def get_all(self) -> List[TwitchChannelSchema]:
        return await TwitchChannelSchema.from_queryset(TwitchChannel.all())

    async def get(self, id) -> TwitchChannelSchema:
        return await TwitchChannelSchema.from_queryset_single(TwitchChannel.get(id=id))

    async def add(self, channel: TwitchChannelCreateSchema) -> TwitchChannelSchema:
        db_channel = await TwitchChannel.create(**channel.dict())
        return await TwitchChannelSchema.from_tortoise_orm(db_channel)

    async def update(self, id: int, channel: TwitchChannelSchema) -> None:
        await TwitchChannel.filter(id=id).update(**channel.dict(exclude_unset=True))

    async def delete(self, id: int) -> None:
        await TwitchChannel.filter(id=id).delete()

    async def _get_twitch_data(self, channels: List[TwitchChannelSchema]) -> List:
        channel_logins = [c.channel_id for c in channels]

        split_logins = [
            channel_logins[i : i + 100] for i in range(0, len(channel_logins), 100)
        ]

        user_info = []
        stream_info = []
        for login_list in split_logins:
            async with httpx.AsyncClient() as client:
                res = await client.get(
                    f"https://api.twitch.tv/helix/users?login={'&login='.join(login_list)}",
                    headers={
                        "Authorization": f"Bearer {self.settings.twitch_token}",
                        "Client-Id": self.settings.twitch_id,
                    },
                )
                user_info += res.json()["data"]

                res = await client.get(
                    f"https://api.twitch.tv/helix/streams?user_login={'&user_login='.join(login_list)}",
                    headers={
                        "Authorization": f"Bearer {self.settings.twitch_token}",
                        "Client-Id": self.settings.twitch_id,
                    },
                )
                stream_info += res.json()["data"]

        return {
            "user_info": user_info,
            "stream_info": stream_info,
        }
