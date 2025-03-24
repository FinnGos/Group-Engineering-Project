from django.db import models
# Create your models here.
# Important: After defining your models, run the migrations again to aply the changes to the database:
# Python manage.py makemigrations
# Python manage.py migrate
# To verify the database: .tables  (Should show tables only from the new database)
# Important: Since we have more then one database, and I didnt use an automative router, make sure to direct correct database

"""""
class Riddle(models.Model):
    id = models.AutoField(primary_key= True)
    question = models.TextField()
    answer = models.CharField(max_length=255)
"""

class Location(models.Model):
    name = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()
    radius = models.FloatField(help_text="Radius in meters for check-in accuracy") # Distance within which check-in is valid

    def __str__(self):
        return self.name