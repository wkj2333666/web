from django.db import models


# Create your models here.

# 类名全小写，是因为 django 数据库中的表名格式为 大写应用名_小写类名，
# 故为了导入数据时保持命名一致，此处的类名采用小写。下同。
class singer_info(models.Model):
    singer_name = models.CharField(max_length=30)
    singer_id = models.IntegerField()
    singer_abstract = models.CharField(max_length=300)
    songs = models.JSONField(default=list)
