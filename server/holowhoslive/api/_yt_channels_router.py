import pickle
import logging
from typing import List
from aioredis import Redis
from fastapi import APIRouter, Depends

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
    return await yt_service.get_db_data()


@router.post("/", response_model=YtChannelSchema)
async def create_saved_yt_channel(
    channel: YtChannelCreateSchema, yt_service: YoutubeService = Depends(YoutubeService)
):
    """
    Add a new channel to be searched for in the Youtube api.
    """
    return await yt_service.add_channel(channel)
