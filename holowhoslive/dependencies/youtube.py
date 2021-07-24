import os
from googleapiclient.discovery import build

def get_yt_service():
    service = build('youtube', 'v3', developerKey=os.getenv('YOUTUBE_API_KEY'))
    try:
        yield service
    finally:
        service.close()
