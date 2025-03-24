from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now

class Building(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="buildings/")  # Normal image
    locked_image = models.ImageField(upload_to="buildings/")  # Blacked-out image
    sustainability_score = models.IntegerField()
    x = models.IntegerField(null=True, blank=True)  # Allow null values
    y = models.IntegerField(null=True, blank=True)  # Allow null values
    size = models.IntegerField(default=30)

    def __str__(self):
        return self.name

class UserBuilding(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    unlocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.building.name}"

class Item(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="items/")
    sustainability_score = models.IntegerField()
    price = models.IntegerField(default=0)
    max_quantity = models.IntegerField(default=5)  # Limit how many a user can buy
    size = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name

class UserItem(models.Model):
    useritem = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    x = models.IntegerField(null=True, blank=True)  # Allow null values
    y = models.IntegerField(null=True, blank=True)  # Allow null values
    size = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.useritem.username} - {self.item.name} at ({self.x}, {self.y})"

class Rubbish(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="rubbish/")  # Store images in a 'rubbish/' folder
    x = models.IntegerField()
    y = models.IntegerField()
    sustainability_score = models.IntegerField(default=-2)


class UserRubbish(models.Model):
    useritem = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Rubbish, on_delete=models.CASCADE)
    cleaned = models.BooleanField(default=False)
    clean_cost = models.IntegerField(default=5)  # Cost to clean up the rubbish
    cleaned_at = models.DateTimeField(null=True, blank=True)  # Track when it was cleaned

    def should_respawn(self):
        """Check if rubbish should reappear after 3 days and deduct sustainability points."""
        if self.cleaned and self.cleaned_at:
            # If the rubbish has been cleaned and 2 days have passed
            if (now() - self.cleaned_at).days >= 2:
                # Respawn the rubbish (set cleaned to False)
                self.cleaned = False
                self.cleaned_at = None

                if self.item:
                    self.useritem.all_time_points += self.item.sustainability_score
                    self.useritem.save()

                # Save the updated Rubbish object
                self.save()

                return True
        return False 