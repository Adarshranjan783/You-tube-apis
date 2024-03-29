from django.shortcuts import render

# Create your views here.
# youtube_api/views.py

from django.core.paginator import Paginator
from django.http import JsonResponse
from youtube_api.models import Video

def get_videos(request):
    videos = Video.objects.all()
    paginator = Paginator(videos, 10)  # 10 videos per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    video_data = [{
        'title': video.title,
        'description': video.description,
        'published_datetime': video.published_datetime,
        'thumbnail_url': video.thumbnail_url
    } for video in page_obj]
    return JsonResponse({'videos': video_data})
