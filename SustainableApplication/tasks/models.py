from django.db import models
from Checkin.models import Location
from home.models import CustomUser
from django.contrib.auth import get_user_model
import os
import uuid
from django.utils.timezone import now


class Tasks(models.Model):
    User = get_user_model()
    user = models.ManyToManyField(CustomUser, blank=True)
    task_name = models.CharField(max_length=200)
    current_progress = models.IntegerField(default=0)
    target = models.IntegerField(default=0)
    reward = models.IntegerField(default=0)
    location_id = models.IntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)
    has_checked_in = models.BooleanField(default=False)
    updated_at = models.DateTimeField(auto_now=True)

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


def unique_file_name(instance, filename):
    """_summary_

    Args:
        instance (_type_): _description_
        filename (_type_): _description_

    Returns:
        _type_: _description_
    """
    ext = filename.split(".")[-1]  # Get file extension
    filename = f"{uuid.uuid4().hex}_{int(now().timestamp())}.{ext}"  # Unique file name
    return os.path.join("MediaPhotos/", filename)  # Keep path


class UploadedImage(models.Model):
    User = get_user_model()
    task = models.OneToOneField(
        Tasks,
        on_delete=models.CASCADE,
        related_name="image",
        null=True,
        blank=True,  # Temporary fix to allow migration
    )
    image = models.ImageField(upload_to=unique_file_name)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"Image for {self.task.task_name}" if self.task else "Unassigned Image"
