from typing import List
from fastapi import APIRouter, Depends

from holowhoslive.schemas import GroupSchema, GroupCreateSchema

from holowhoslive.services import GroupService

router = APIRouter(prefix="/groups", tags=["Groups"])


@router.get("/", response_model=List[GroupSchema])
async def get_groups(group_service: GroupService = Depends(GroupService)):
    return await group_service.get_all()


@router.post("/", response_model=GroupSchema)
async def create_group(
    group: GroupCreateSchema, group_service: GroupService = Depends(GroupService)
):
    return await group_service.add(group)
