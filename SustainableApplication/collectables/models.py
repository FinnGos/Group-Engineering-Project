"""Defines entities for database"""

from django.db import models

# Create your models here.
class Collectable(models.Model):
    """Model for in app collectables, storing their names and associated images"""

    #TODO standardise max_length
    name = models.CharField(max_length=200)
    image = models.ImageField(upload_to="media/", default="placeholder.jpg")
    fact = models.CharField(max_length=1000, default="")

    def __str__(self):
        return self.name

