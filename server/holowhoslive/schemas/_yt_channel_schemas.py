from typing import Optional
from pydantic import BaseModel, AnyHttpUrl


class YtChannelImageSchema(BaseModel):
    default: AnyHttpUrl
    medium: AnyHttpUrl
    high: AnyHttpUrl


class YtChannelBaseSchema(BaseModel):
    first_name: str
    last_name: str
    channel_id: str
    group: str


class YtChannelCreateSchema(YtChannelBaseSchema):
    pass


class YtChannelSchema(YtChannelBaseSchema):
    id: int
    channel_name: Optional[str]
    is_live: Optional[bool]
    images: Optional[YtChannelImageSchema]
    subscribers: Optional[int]

    class Config:
        orm_mode = True
