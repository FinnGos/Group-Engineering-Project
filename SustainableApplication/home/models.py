from django.db import models
from django.urls import reverse  # enables retrieval of url information
from django.db.models import UniqueConstraint  # constrains fields to unique values
from django.db.models.functions import Lower  # returns lower case value of field
from django.contrib.auth.models import AbstractUser
from django.db import models

# IMPORTANT: remember to makemigrations and migrate when you make changes to the models
# Create your models here.


class CustomUser(AbstractUser):
    """Extending AbstractUser in order to add points to a basic user"""

    current_points = models.IntegerField(default=0)
    all_time_points = models.IntegerField(default=0) #2 types of points for the leaderboard

    def __str__(self):
        return self.username
