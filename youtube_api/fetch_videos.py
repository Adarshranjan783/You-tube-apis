# youtube_api/fetch_videos.py

import datetime
import time
from googleapiclient.discovery import build
from youtube_api.models import Video

def fetch_videos(api_key, query):
    youtube = build('youtube', 'v3', developerKey=api_key)
    while True:
        try:
            request = youtube.search().list(
                part='snippet',
                q=query,
                type='video',
                order='date',
                publishedAfter=(datetime.datetime.utcnow() - datetime.timedelta(minutes=5)).isoformat() + 'Z',
                maxResults=50  # Adjust as needed
            )
            response = request.execute()
            for item in response['items']:
                video = Video(
                    title=item['snippet']['title'],
                    description=item['snippet']['description'],
                    published_datetime=item['snippet']['publishedAt'],
                    thumbnail_url=item['snippet']['thumbnails']['default']['url']
                )
                video.save()
            time.sleep(10)  # Wait for 10 seconds before fetching again
        except Exception as e:
            print('Error occurred:', e)
