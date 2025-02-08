from django.db import models
from django.urls import reverse  # enables retrieval of url information
from django.db.models import UniqueConstraint  # constrains fields to unique values
from django.db.models.functions import Lower  # returns lower case value of field
from django.contrib.auth.models import AbstractUser
from django.db import models

# IMPORTANT: remember to makemigrations and migrate when you make changes to the models
# Create your models here.


# I don't know what should be in each model please change accordingly
class Locations(models.Model):
    """model associated with a location"""

    name = models.CharField(max_length=200, unique=True)

    # method to return name of location
    def __str__(self):
        return self.name


class Collectable(models.Model):
    """model associated with a collectable item"""

    name = models.CharField(max_length=200, unique=True)

    def __str__(self):
        return self.name


class CustomUser(AbstractUser):
    """Custom user extends djangos abstract user which is a baseling user model.
    this allows us to add more fields that are associated with a user"""

    points = models.IntegerField(default=0)

    def __str__(self):
        return self.username
