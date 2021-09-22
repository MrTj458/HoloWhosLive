from holowhoslive.config import get_settings
from googleapiclient.discovery import build

settings = get_settings()


def get_yt_service():
    with build("youtube", "v3", developerKey=settings.youtube_api_key) as yt_client:
        yield yt_client
