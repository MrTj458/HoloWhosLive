from typing import Optional
from pydantic import BaseModel, AnyHttpUrl
from tortoise.contrib.pydantic import pydantic_model_creator
from tortoise import Tortoise

from holowhoslive.models import Group, Channel

# Init models so relationships are available
Tortoise.init_models(["holowhoslive.models"], "models")

# -- Groups --
GroupSchema = pydantic_model_creator(Group, name="GroupSchema")
GroupCreateSchema = pydantic_model_creator(
    Group, name="GroupCreateSchema", exclude_readonly=True
)

# -- Channels --

ChannelSchema = pydantic_model_creator(Channel, name="ChannelSchema")
ChannelCreateSchema = pydantic_model_creator(
    Channel, name="ChannelCreateSchema", exclude_readonly=True
)


class ChannelApiSchema(BaseModel):
    id: int
    display_name: str
    is_live: bool
    image: AnyHttpUrl
    subscribers: Optional[int]
    view_count: Optional[int]
    first_name: str
    last_name: str
    channel_id: str
    platform: str
    group: GroupSchema
