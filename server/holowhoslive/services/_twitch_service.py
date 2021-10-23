from fastapi import Depends
import httpx
from typing import List

from holowhoslive.config import get_settings, Settings
from holowhoslive.schemas import ChannelApiSchema, ChannelSchema
from holowhoslive.models import Channel


class TwitchService:
    def __init__(self, settings: Settings = Depends(get_settings)) -> None:
        self.settings = settings

    async def get_twitch_data(self) -> List[ChannelApiSchema]:
        db_channels = await ChannelSchema.from_queryset(
            Channel.filter(platform="Twitch").all()
        )
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
                ChannelApiSchema(
                    **channel.dict(),
                    # images=TwitchChannelImageSchema(
                    #     default=twitch_channel["profile_image_url"]
                    # ),
                    image=twitch_channel["profile_image_url"],
                    view_count=twitch_channel["view_count"],
                    is_live=is_live,
                    display_name=twitch_channel["display_name"],
                )
            )

        return channels

    async def _get_twitch_access_token(self) -> str:
        url = f"https://id.twitch.tv/oauth2/token?client_id={self.settings.twitch_id}&client_secret={self.settings.twitch_secret}&grant_type=client_credentials"
        async with httpx.AsyncClient() as client:
            res = await client.post(url)
            return res.json()["access_token"]

    async def _get_twitch_data(self, channels: List[ChannelSchema]) -> List:
        access_token = await self._get_twitch_access_token()
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
                        "Authorization": f"Bearer {access_token}",
                        "Client-Id": self.settings.twitch_id,
                    },
                )
                user_info += res.json()["data"]

                res = await client.get(
                    f"https://api.twitch.tv/helix/streams?user_login={'&user_login='.join(login_list)}",
                    headers={
                        "Authorization": f"Bearer {access_token}",
                        "Client-Id": self.settings.twitch_id,
                    },
                )
                stream_info += res.json()["data"]

        return {
            "user_info": user_info,
            "stream_info": stream_info,
        }
