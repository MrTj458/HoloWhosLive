from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy.orm import Session

from holowhoslive.dependencies import get_db
from holowhoslive.models import User
from holowhoslive.schemas.user import UserSchema, UserCreateSchema

router = APIRouter(
    prefix='/api/users',
    tags=['users'],
)


@router.get('/', response_model=List[UserSchema])
async def get_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return users


@router.get('/{id}', response_model=UserSchema)
async def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == id).first()
    if not user:
        raise HTTPException(status.HTTP_404_NOT_FOUND)
    return user


@router.post('/', response_model=UserSchema)
async def create_user(user: UserCreateSchema, db: Session = Depends(get_db)):
    fake_hashed_pass = user.password + 'FakeHash'
    db_user = User(email=user.email, username=user.username,
                   hashed_password=fake_hashed_pass)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user
