from pydantic import BaseModel

class UserBaseSchema(BaseModel):
    email: str
    username: str

class UserCreateSchema(UserBaseSchema):
    password: str

class UserSchema(UserBaseSchema):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
