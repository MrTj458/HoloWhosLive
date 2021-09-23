from typing import List

from holowhoslive.models import Group
from holowhoslive.schemas import GroupSchema, GroupCreateSchema


class GroupService:
    async def get_all(self) -> List[GroupSchema]:
        return await GroupSchema.from_queryset(Group.all())

    async def add(self, group: GroupCreateSchema) -> GroupSchema:
        db_group = await Group.create(**group.dict())
        return await GroupSchema.from_tortoise_orm(db_group)
