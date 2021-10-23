from typing import List
from fastapi import APIRouter, Depends, status, HTTPException

from holowhoslive.schemas import ChannelApiSchema, ChannelSchema, ChannelCreateSchema
from holowhoslive.services import ChannelService


router = APIRouter(prefix="/channels", tags=["channels"])


@router.get("/", response_model=List[ChannelApiSchema])
async def get_channel_data(channel_service: ChannelService = Depends(ChannelService)):
    return await channel_service.get_api_data()


@router.get("/saved", response_model=List[ChannelSchema])
async def get_saved_channels(channel_service: ChannelService = Depends(ChannelService)):
    return await channel_service.get_all()


@router.get("/{id}", response_model=ChannelSchema)
async def get_saved_channel(
    id: int, channel_service: ChannelService = Depends(ChannelService)
):
    return await channel_service.get(id)


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=ChannelSchema)
async def create_channel(
    channel: ChannelCreateSchema,
    channel_service: ChannelService = Depends(ChannelService),
):
    return await channel_service.add(channel)


@router.put("/{id}", response_model=ChannelSchema)
async def update_channel(
    id: int,
    channel: ChannelCreateSchema,
    channel_service: ChannelService = Depends(ChannelService),
):
    db_channel = await channel_service.get(id)

    if not db_channel:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="channel not found")

    await channel_service.update(id, channel)

    return await channel_service.get(id)


@router.delete("{id}")
async def delete_channel(
    id: int, channel_service: ChannelService = Depends(ChannelService)
):
    db_channel = await channel_service.get(id)

    if not db_channel:
        raise HTTPException(status.HTTP_404_NOT_FOUND, detail="channel not found")

    await channel_service.delete(id)

    return {"ok": True}
