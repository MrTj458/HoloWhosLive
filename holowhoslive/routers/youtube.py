import json
from typing import List
from holowhoslive.models.channel import Channel
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from holowhoslive.models import Channel
from holowhoslive.dependencies import get_yt_service, get_db, get_redis
from holowhoslive.schemas.channel import ChannelCreateSchema, ChannelSchema

router = APIRouter(
    prefix='/api/youtube',
    tags=['youtube'],
)


@router.get('/')
async def get_youtube_info(r=Depends(get_redis), db: Session = Depends(get_db), service=Depends(get_yt_service)):
    # Check for and return cached data if it exists
    cached_data = r.get('cached_data')
    if cached_data:
        return json.loads(cached_data)

    print('Refetching from Youtube API!')
    # Cached data didn't exist, get the channel data
    channel_list = db.query(Channel).all()

    # Fetch channel data
    channel_ids = [channel.channel_id for channel in channel_list]
    request = service.channels().list(
        id=channel_ids, part='snippet,statistics')
    channel_data = request.execute()['items']

    response_data = []
    for channel in channel_data:
        # Match Youtube object back to local db object
        current_channel = [
            c for c in channel_list if c.channel_id == channel['id']][0]

        # Add channel data
        channel_data = {**ChannelSchema.from_orm(current_channel).dict()}
        channel_data['channel_id'] = channel['id']
        channel_data['description'] = channel['snippet']['description']
        channel_data['thumbnails'] = channel['snippet']['thumbnails']
        channel_data['statistics'] = channel['statistics']
        channel_data['videos'] = []

        # Fetch videos for channel
        request = service.search().list(
            part='snippet', channelId=channel['id'], q='', order='date')
        videos = request.execute()['items']

        for video in videos:
            v_snippet = video['snippet']

            # Add video data
            video_data = {}
            video_data['id'] = video['id']['videoId']
            video_data['published_at'] = v_snippet['publishedAt']
            video_data['title'] = v_snippet['title']
            video_data['description'] = v_snippet['description']
            video_data['thumbnails'] = v_snippet['thumbnails']
            video_data['live_broadcast_content'] = v_snippet['liveBroadcastContent']

            channel_data['videos'].append(video_data)

        # Calculate if channel is live
        channel_data['is_live'] = len([video for video in channel_data['videos']
                                       if video['live_broadcast_content'] == 'live']) > 0

        response_data.append(channel_data)

    # Cache result
    r.setex('cached_data', '900', json.dumps(response_data))

    return response_data


@router.get('/channels', response_model=List[ChannelSchema])
async def get_saved_channels(db: Session = Depends(get_db)):
    channels = db.query(Channel).all()
    return channels


@router.post('/channels', response_model=ChannelSchema)
async def create_saved_channel(channel: ChannelCreateSchema, db: Session = Depends(get_db)):
    db_channel = Channel(**channel.dict())
    db.add(db_channel)
    db.commit()
    db.refresh(db_channel)
    return db_channel
