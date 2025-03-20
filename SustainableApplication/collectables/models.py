"""Defines entities for database"""

from django.db import models


class CollectableManager(models.Manager):
    """
    Overwrites model manager for Collectable
    So specific objects can be accessed using their details
    """

    def get_by_name(self, card_name):
        """Gets objects with matching name"""
        return super().get_queryset().filter(name=card_name)

class Collectable(models.Model):
    """Model for in app collectables, storing their names and associated images"""

    name = models.CharField(max_length=200, unique=True)
    image = models.ImageField(upload_to="media/", default="placeholder.jpg")
    fact = models.CharField(max_length=1000, default="")
    # Sets model manager
    objects = CollectableManager()



    def __str__(self):
        return self.name

