from django.db import models
from django.conf import settings
from collectables.models import Collectable

class Item(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    carbo_score = models.IntegerField()  # Sustainability contribution
    image = models.ImageField(upload_to='items/')  # Optional: image for UI


class UserInventory(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    purchased_items = models.ManyToManyField(Item, blank=True)
    unlocked_buildings = models.ManyToManyField(Collectable, blank=True)

    def __str__(self):
        return f"{self.user.username}'s Inventory"