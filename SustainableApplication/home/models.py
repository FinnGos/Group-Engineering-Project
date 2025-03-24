from django.db import models
from django.urls import reverse  # enables retrieval of url information
from django.db.models import UniqueConstraint  # constrains fields to unique values
from django.db.models.functions import Lower  # returns lower case value of field
from django.contrib.auth.models import AbstractUser
from django.db import models
from collectables.models import Collectable
from riddles.models import Riddle

class CustomUser(AbstractUser):
    """Extending AbstractUser in order to add points to a basic user"""
    completed_riddles = models.ManyToManyField(Riddle, blank=True)

    current_points = models.IntegerField(default=0)
    all_time_points = models.IntegerField(
        default=0
    )  # 2 types of points for the leaderboard

    selected_task = models.ForeignKey(
        "tasks.Tasks", null=True, blank=True, on_delete=models.SET_NULL
    )
    task_assign_date = models.DateField(null=True, blank=True)
    all_time_points = models.IntegerField(default=0) #2 types of points for the leaderboard
    # Collectable cards owned by user
    collectables_owned = models.ManyToManyField(Collectable, blank=True)
    

    def __str__(self):
        return self.username
