from typing import List
from fastapi import APIRouter, Depends, status, HTTPException
from starlette.status import HTTP_404_NOT_FOUND

from holowhoslive.services import TwitchService
from holowhoslive.schemas import (
    TwitchChannelApiSchema,
    TwitchChannelSchema,
    TwitchChannelCreateSchema,
)

router = APIRouter(
    prefix="/twitch",
    tags=["Twitch Channels"],
)


@router.get("/", response_model=List[TwitchChannelApiSchema])
async def get_twitch_data(twitch_service: TwitchService = Depends(TwitchService)):
    return await twitch_service.get_twitch_data()


@router.get("/saved", response_model=List[TwitchChannelSchema])
async def get_saved_twitch_data(twitch_service: TwitchService = Depends(TwitchService)):
    return await twitch_service.get_all()


@router.post(
    "/", status_code=status.HTTP_201_CREATED, response_model=TwitchChannelSchema
)
async def create_twitch_channel(
    channel: TwitchChannelCreateSchema,
    twitch_service: TwitchService = Depends(TwitchService),
):
    return await twitch_service.add(channel)


@router.put("/{id}", response_model=TwitchChannelSchema)
async def update_twitch_channel(
    id: int,
    channel: TwitchChannelCreateSchema,
    twitch_service: TwitchService = Depends(TwitchService),
):
    db_channel = await twitch_service.get(id)

    if not db_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Twitch channel not found."
        )

    await twitch_service.update(id, channel)

    return await twitch_service.get(id)


@router.delete("/{id}")
async def delete_twitch_channel(
    id: int, twitch_service: TwitchService = Depends(TwitchService)
):
    db_channel = await twitch_service.get(id)

    if not db_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Twitch channel not found."
        )

    await twitch_service.delete(id)

    return {"ok": True}
