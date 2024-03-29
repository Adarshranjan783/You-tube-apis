
from django.db import models

class Video(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    published_datetime = models.DateTimeField()
    thumbnail_url = models.URLField()

    class Meta:
        ordering = ['-published_datetime']
