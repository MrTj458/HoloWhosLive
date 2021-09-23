import pickle
import logging
from typing import List
from aioredis import Redis
from fastapi import APIRouter, Depends, HTTPException, status

from holowhoslive.services import YoutubeService
from holowhoslive.dependencies import get_redis
from holowhoslive.schemas import YtChannelCreateSchema, YtChannelSchema

log = logging.getLogger("uvicorn")

router = APIRouter(
    prefix="/youtube",
    tags=["Youtube Channels"],
)


@router.get("/", response_model=List[YtChannelSchema])
async def get_yt_channel_data(
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
    log.info("Fetching from Youtub API")
    data = await yt_service.get_all_data()
    await r.setex("cached_yt_channels", "300", pickle.dumps(data))

    return data


@router.get("/saved", response_model=List[YtChannelSchema])
async def get_saved_yt_channel_data(
    yt_service: YoutubeService = Depends(YoutubeService),
):
    """Get the saved channel data in the database only."""
    return await yt_service.get_all_db_data()


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=YtChannelSchema)
async def create_saved_yt_channel(
    channel: YtChannelCreateSchema, yt_service: YoutubeService = Depends(YoutubeService)
):
    """
    Add a new channel to be searched for in the Youtube api.
    """
    return await yt_service.add(channel)


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
