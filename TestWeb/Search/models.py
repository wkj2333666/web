from django.db import models

# Create your models here.
class search_song(models.Model):
    song_id = models.IntegerField()
    song_name = models.CharField(max_length=100)
    singers_name = models.CharField(max_length=100)
    lyric = models.CharField(max_length=1000)