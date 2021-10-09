import pickle
import logging
from typing import List
from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, status

from holowhoslive.services import YoutubeService
from holowhoslive.dependencies import get_redis

from holowhoslive.schemas import (
    YtChannelSchema,
    YtChannelCreateSchema,
    YtChannelApiSchema,
)

log = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/youtube",
    tags=["Youtube Channels"],
)


@router.get("/", response_model=List[YtChannelApiSchema])
async def get_youtube_data(
    r: Redis = Depends(get_redis), yt_service: YoutubeService = Depends(YoutubeService)
):
    """
    Get combined data from Youtube and database. Refreshed every 5 minutes.
    """
    # Check for cached data and return if exists
    data = await r.get("cached_yt_channels")
    if data:
        return pickle.loads(data)

    # Fetch from Youtube api and cache the results
    log.info("Fetching from Youtube API")
    data = await yt_service.get_youtube_data()
    await r.setex(
        "cached_yt_channels", "300", pickle.dumps([item.dict() for item in data])
    )

    return data


@router.get("/saved", response_model=List[YtChannelSchema])
async def get_saved_youtube_data(
    yt_service: YoutubeService = Depends(YoutubeService),
):
    """Get the saved channel data in the database only."""
    return await yt_service.get_all()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=YtChannelSchema)
async def create_saved_yt_channel(
    channel: YtChannelCreateSchema, yt_service: YoutubeService = Depends(YoutubeService)
):
    """
    Add a new channel to be searched for in the Youtube api.
    """
    return YtChannelSchema.from_orm(await yt_service.add(channel))


@router.put("/{id}", response_model=YtChannelSchema)
async def update_youtube_channel(
    id: int,
    channel: YtChannelCreateSchema,
    yt_service: YoutubeService = Depends(YoutubeService),
):
    db_channel = await yt_service.get(id)

    if not db_channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Youtube channel not found."
        )

    await yt_service.update(id, channel)

    return await yt_service.get(id)


@router.delete("/{id}")
async def delete_yt_channel(
    id: int, yt_service: YoutubeService = Depends(YoutubeService)
):
    channel = await yt_service.get(id)

    if not channel:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Youtube channel not found."
        )

    await yt_service.delete(id)
    return {"ok": True}
