# youtube_api/management/commands/fetch_videos.py

import datetime
import time
from googleapiclient.discovery import build
from youtube_api.models import Video
from django.core.management.base import BaseCommand

class Command(BaseCommand):
    help = 'Fetches videos from YouTube API and stores them in the database'

    def add_arguments(self, parser):
        parser.add_argument('api_key', type=str, help='Your YouTube API key')
        parser.add_argument('query', type=str, help='Your search query')

    def handle(self, *args, **options):
        api_key = options['api_key']
        query = options['query']
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
