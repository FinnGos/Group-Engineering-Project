from django.db import models
from Checkin.models import Location
from home.models import CustomUser
from django.contrib.auth import get_user_model
from django.db.models.signals import post_delete
from django.dispatch import receiver

class Tasks(models.Model):
    User = get_user_model()
    user = models.ManyToManyField(CustomUser,blank = True)
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
    

class UploadedImage(models.Model):
    User = get_user_model()
    task = models.OneToOneField(
        Tasks, on_delete=models.CASCADE, related_name="image",
        null=True, blank=True  # Temporary fix to allow migration
    )
    image = models.ImageField(upload_to='MediaPhotos/')
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(User, on_delete=models.CASCADE)

    @receiver(post_delete, sender=User)
    def delete_user_images(sender, instance, **kwargs):
        """
        Deletes all images uploaded by the user when their account is deleted.
        """
        UploadedImage.objects.filter(uploaded_by=instance).delete()

    def __str__(self):
        return f"Image for {self.task.task_name}" if self.task else "Unassigned Image"
