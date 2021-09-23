from pydantic import BaseModel, AnyHttpUrl
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import Tortoise

from holowhoslive.models import Group, YtChannel

# Init models so relationships are available
Tortoise.init_models(["holowhoslive.models"], "models")

# -- Groups --
GroupSchema = pydantic_model_creator(Group, name="GroupSchema", exclude=["yt_channels"])
GroupCreateSchema = pydantic_model_creator(
    Group, name="GroupCreateSchema", exclude_readonly=True
)

# -- Youtube Channels --
YtChannelSchema = pydantic_model_creator(YtChannel, name="YtChannelSchema")
YtChannelCreateSchema = pydantic_model_creator(
    YtChannel, name="YtChannelCreateSchema", exclude_readonly=True
)


class YtChannelImageSchema(BaseModel):
    default: AnyHttpUrl
    medium: AnyHttpUrl
    high: AnyHttpUrl


class YtChannelApiSchema(BaseModel):
    id: int
    channel_name: str
    is_live: bool
    images: YtChannelImageSchema
    subscribers: int
    first_name: str
    last_name: str
    channel_id: str
    group: GroupSchema
