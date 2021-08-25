from holowhoslive.actions.channels import fetch_channel_data
import pickle
from typing import List
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from holowhoslive.models import Channel
from holowhoslive.dependencies import get_yt_service, get_db, get_redis
from holowhoslive.schemas.channel import ChannelCreateSchema, ChannelSchema

router = APIRouter(
    prefix='/api/channels',
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
        print('Fetched from Redis cache')
        return pickle.loads(data)

    # Fetch from Youtube api and cache the results
    print('Fetching from YT API')
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
