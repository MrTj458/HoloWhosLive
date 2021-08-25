from pydantic import BaseModel

class ChannelBaseSchema(BaseModel):
    first_name: str
    last_name: str
    channel_name: str
    channel_id: str

class ChannelCreateSchema(ChannelBaseSchema):
    pass

class ChannelSchema(ChannelBaseSchema):
    id: int

    class Config:
        orm_mode = True
