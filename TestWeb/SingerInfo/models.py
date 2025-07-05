from django.db import models


# Create your models here.
class singer_info(models.Model):
    singer_name = models.CharField(max_length=30)
    singer_id = models.IntegerField()
    singer_abstract = models.CharField(max_length=300)
    songs = models.JSONField(default=list)
