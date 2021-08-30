from typing import Optional
from pydantic import BaseModel, AnyHttpUrl


class ChannelImageSchema(BaseModel):
    default: AnyHttpUrl
    medium: AnyHttpUrl
    high: AnyHttpUrl


class ChannelBaseSchema(BaseModel):
    first_name: str
    last_name: str
    channel_id: str
    group: str


class ChannelCreateSchema(ChannelBaseSchema):
    pass


class ChannelSchema(ChannelBaseSchema):
    id: int
    channel_name: Optional[str]
    is_live: Optional[bool]
    images: Optional[ChannelImageSchema]
    subscribers: Optional[int]

    class Config:
        orm_mode = True
