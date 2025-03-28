"""Defines entities for database"""

from django.db import models


class Collectable(models.Model):
    """Model for in app collectables, storing their names and associated images"""

    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to="media/", default="placeholder.jpg")
    fact = models.CharField(max_length=1000, default="")



    def __str__(self):
        return self.name

