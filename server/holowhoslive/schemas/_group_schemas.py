from typing import Optional
from pydantic import BaseModel, AnyHttpUrl


class GroupBaseSchema(BaseModel):
    name: str
    platform: str


class GroupCreateSchema(GroupBaseSchema):
    pass


class GroupSchema(GroupBaseSchema):
    id: int

    class Config:
        orm_mode = True
