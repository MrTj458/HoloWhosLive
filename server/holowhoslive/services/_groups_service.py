from typing import List
from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

from holowhoslive.dependencies import get_db
from holowhoslive.schemas import GroupCreateSchema
from holowhoslive.models import Group


class GroupService:
    def __init__(self, db: AsyncSession = Depends(get_db)):
        self.db = db

    async def get_all(self) -> List[Group]:
        return (await self.db.execute(select(Group))).scalars().all()

    async def add(self, group: GroupCreateSchema) -> Group:
        db_group = Group(**group.dict())
        self.db.add(db_group)
        await self.db.commit()
        await self.db.refresh(db_group)
        return db_group
