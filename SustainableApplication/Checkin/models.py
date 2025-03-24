"""Defines entities for database"""

from django.db import models


class Location(models.Model):
    """Model for locations, storing distance informations for check-in"""
    #id = models. AutoField(primary_key= True)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField(help_text="Radius in meters for check-in accuracy") # Distance within which check-in is valid

    def __str__(self):
        return self.name