from django.db import models

# Create your models here.
class song_info(models.Model):
    song_id = models.IntegerField()
    singers = models.JSONField(default=dict)
    song_name = models.CharField(max_length=50)
    lyric = models.CharField(max_length=1000)
    comments = models.JSONField(default=list)