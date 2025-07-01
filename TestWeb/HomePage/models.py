from django.db import models

# Create your models here.

class SongList(models.Model):
    song_name = models.CharField(max_length=100)
    singer = models.CharField(max_length=30)
    song_link = models.CharField(max_length=100)
