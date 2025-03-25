"""Defines entities for database"""
from django.db import models
from django.contrib.auth.models import AbstractUser
from collectables.models import Collectable
from riddles.models import Riddle


class CustomUser(AbstractUser):
    """Extending AbstractUser in order to add points to a basic user"""
    completed_riddles = models.ManyToManyField(Riddle, blank=True)

    current_points = models.IntegerField(default=300)
    all_time_points = models.IntegerField(
        default=300
    ) # 2 types of points for the leaderboard

    selected_task = models.ForeignKey(
        "tasks.Tasks", null=True, blank=True, on_delete=models.SET_NULL
    )
    task_assign_date = models.DateField(null=True, blank=True)
    # Collectable cards owned by user
    collectables_owned = models.ManyToManyField(Collectable, blank=True)
    

    def __str__(self):
        return self.username
    
    def clean(self):
        if self.current_points < 0:
            raise ValueError("Points cannot be negative.")

    def save(self, *args, **kwargs):
        self.clean()  # Call clean before saving
        super().save(*args, **kwargs)
