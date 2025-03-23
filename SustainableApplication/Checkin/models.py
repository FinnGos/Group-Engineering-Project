"""Defines entities for database"""

from django.db import models

"""""
class Riddle(models.Model):
    id = models.AutoField(primary_key= True)
    question = models.TextField()
    answer = models.CharField(max_length=255)
"""

class Location(models.Model):
    """Model for locations, storing distance informations for check-in"""
    #id = models. AutoField(primary_key= True)
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField(help_text="Radius in meters for check-in accuracy") # Distance within which check-in is valid
    #riddle = models.OneToOneField(Riddle, on_delete=models.CASCADE) # Unique riddle per location

    def __str__(self):
        return self.name