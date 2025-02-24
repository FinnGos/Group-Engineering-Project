from django.db import models
from Checkin.models import Location


# Create your models here.
class Tasks(models.Model):
    task_name = models.CharField(max_length=200)
    current_progress = models.IntegerField(default=0)
    target = models.IntegerField(default=0)
    reward = models.IntegerField(default=0)
    # please change to forgein keys from loactions database in implementation
    # artful dodger coordinates at present
    location_id = models.IntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    # not sure if needs to be change in future
    has_checked_in = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        self.completed = self.current_progress == self.target
        super().save(*args, **kwargs)

    @property
    def latitude(self):
        """Retrieve latitude dynamically from related location object"""
        return self.location.latitude if self.location else None
    
    @property
    def longitude(self):
        """Retrieve longitude dynamically from related location object"""
        return self.location.longitude if self.location else None

    @property
    def progress_percentage(self):
        return (self.current_progress / self.target) * 100 if self.target > 0 else 0

    def __str__(self):
        return self.task_name