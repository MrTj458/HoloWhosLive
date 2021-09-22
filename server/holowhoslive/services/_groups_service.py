from typing import List
from fastapi import Depends
from sqlalchemy.orm import Session
from sqlalchemy import select

from holowhoslive.dependencies import get_db
from holowhoslive.schemas import GroupCreateSchema
from holowhoslive.models import Group


class GroupService:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def get_all(self) -> List[Group]:
        return self.db.execute(select(Group)).scalars().all()

    def add(self, group: GroupCreateSchema) -> Group:
        db_group = Group(**group.dict())
        self.db.add(db_group)
        self.db.commit()
        self.db.refresh(db_group)
        return db_group
