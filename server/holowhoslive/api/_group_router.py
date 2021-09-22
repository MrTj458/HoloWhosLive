from typing import List
from fastapi import APIRouter, Depends

from holowhoslive.schemas import GroupSchema, GroupCreateSchema
from holowhoslive.services import GroupService

router = APIRouter(prefix="/groups", tags=["groups"])


@router.get("/", response_model=List[GroupSchema])
def get_groups(group_service: GroupService = Depends(GroupService)):
    return group_service.get_all()


@router.post("/", response_model=GroupSchema)
def create_group(
    group: GroupCreateSchema, group_service: GroupService = Depends(GroupService)
):
    return group_service.add(group)
