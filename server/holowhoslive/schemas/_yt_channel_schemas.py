from typing import Optional
from pydantic import BaseModel, AnyHttpUrl

from holowhoslive.schemas._group_schemas import GroupSchema


class YtChannelImageSchema(BaseModel):
    default: AnyHttpUrl
    medium: AnyHttpUrl
    high: AnyHttpUrl


class YtChannelBaseSchema(BaseModel):
    first_name: str
    last_name: str
    channel_id: str


class YtChannelCreateSchema(YtChannelBaseSchema):
    group_id: int


class YtChannelSchema(YtChannelBaseSchema):
    id: int
    channel_name: Optional[str]
    is_live: Optional[bool]
    images: Optional[YtChannelImageSchema]
    subscribers: Optional[int]
    group: GroupSchema

    class Config:
        orm_mode = True
