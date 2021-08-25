import os
from holowhoslive.config import get_settings
from googleapiclient.discovery import build

settings = get_settings()

def get_yt_service():
    service = build('youtube', 'v3', developerKey=settings.youtube_api_key)
    try:
        yield service
    finally:
        service.close()
