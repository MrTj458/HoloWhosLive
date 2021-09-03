import pickle
import logging
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from holowhoslive.models import Channel
from holowhoslive.actions.channels import fetch_channel_data
from holowhoslive.dependencies import get_yt_service, get_db, get_redis
from holowhoslive.schemas.channel import ChannelCreateSchema, ChannelSchema

log = logging.getLogger('uvicorn')

router = APIRouter(
    prefix='/channels',
    tags=['channels'],
)


@router.get('/', response_model=List[ChannelSchema])
def get_channel_data(r=Depends(get_redis), db: Session = Depends(get_db), service=Depends(get_yt_service)):
    """
    Get channel data for all channels saved in the database.
    """
    # Check for cached data and return if exists
    data = r.get('cached_channels')
    if data:
        return pickle.loads(data)

    # Fetch from Youtube api and cache the results
    log.info('Fetching from Youtub API')
    data = fetch_channel_data(db, service)
    r.setex('cached_channels', '300', pickle.dumps(data))

    return data


@router.post('/', response_model=ChannelSchema)
async def create_saved_channel(channel: ChannelCreateSchema, db: Session = Depends(get_db)):
    """
    Add a new channel to be searched for in the Youtube api.
    """
    db_channel = Channel(**channel.dict())
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel
