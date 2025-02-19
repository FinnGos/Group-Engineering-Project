from django.db import models


# Create your models here.
class Tasks(models.Model):
    task_name = models.CharField(max_length=200)
    current_progress = models.IntegerField(default=0)
    target = models.IntegerField(default=0)
    reward = models.IntegerField(default=0)
    completed = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.completed = self.current_progress == self.target
        super().save(*args, **kwargs)

    @property
    def progress_percentage(self):
        return (self.current_progress / self.target) * 100 if self.target > 0 else 0

    def __str__(self):
        return self.task_name
