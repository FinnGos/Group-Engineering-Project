from django.db import models


# Create your models here.
class Tasks(models.Model):
    task_name = models.CharField(max_length=200)
    current_progress = models.IntegerField(default=0)
    target = models.IntegerField(default=0)
    reward = models.IntegerField(default=0)
