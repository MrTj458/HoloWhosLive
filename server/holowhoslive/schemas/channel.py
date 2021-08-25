from typing import Optional
from pydantic import BaseModel, AnyHttpUrl


class ChannelImageSchema(BaseModel):
    default: AnyHttpUrl
    medium: AnyHttpUrl
    high: AnyHttpUrl


class ChannelBaseSchema(BaseModel):
    first_name: str
    last_name: str
    channel_name: str
    channel_id: str


class ChannelCreateSchema(ChannelBaseSchema):
    pass


class ChannelSchema(ChannelBaseSchema):
    id: int
    is_live: Optional[bool]
    images: Optional[ChannelImageSchema]
    subscribers: Optional[int]

    class Config:
        orm_mode = True
