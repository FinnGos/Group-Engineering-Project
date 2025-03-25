from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.utils.timezone import now

class Building(models.Model):
    """Model for the buildings that will display on the campus map
        Each building has a name, their unlocked image, their locked image,
        how much they contribute to the sustainability score, x and y coords 
        for their placement on the map, and their size in pixels     
    """
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
    """Model for user's buildings so that each user can have their own
        buildings that acts independantly, so when one person unlocks 
        the building it only shows on their map. This has the username of
        their respective user, the building that it is associated with, and
        if they are unlocked or not
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    building = models.ForeignKey(Building, on_delete=models.CASCADE)
    unlocked = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username} - {self.building.name}"

class Item(models.Model):
    """Model for the items in the shop so that the users can purchase them.
        This includes the name of the item, the image for the item, the
        contribution for campus cred, the price of the item, the maximum
        quantity that the user is allowed to purchase, and the size of the 
        image."""
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="items/")
    sustainability_score = models.IntegerField()
    price = models.IntegerField(default=0)
    max_quantity = models.IntegerField(default=5)  # Limit how many a user can buy
    size = models.PositiveIntegerField(default=30)

    def __str__(self):
        return self.name

class UserItem(models.Model):
    """Model for the user's item in their inventory, these will be displayed
        on the user's map. This includes the id of the user, the id of the 
        associated item, the x and y coords of the item on the user's map,
        and the size of the image on the user's map
    """
    useritem = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    x = models.IntegerField(null=True, blank=True)  # Allow null values
    y = models.IntegerField(null=True, blank=True)  # Allow null values
    size = models.PositiveIntegerField()


    def __str__(self):
        return f"{self.useritem.username} - {self.item.name} at ({self.x}, {self.y})"

class Rubbish(models.Model):
    """Model for the rubbish that can be cleaned on the user's map. This
        includes the name of the rubbish, the image for the rubbish, the x 
        and y coords for the placement of each rubbish on the map, and 
        how much the rubbish contributes to the campus creds.
    """
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to="rubbish/")  # Store images in a 'rubbish/' folder
    x = models.IntegerField()
    y = models.IntegerField()
    sustainability_score = models.IntegerField(default=-2)


class UserRubbish(models.Model):
    """Model for the user's individual rubbish so that if a user cleans up
        their it only affects the user's map. This include the id for the 
        user, the rubbish id, a boolean if the rubbish was cleaned, how
        much it costs to clean the rubbish, and when the rubbish was
        cleaned to calculate when it needs to re-appear
        """
    useritem = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    item = models.ForeignKey(Rubbish, on_delete=models.CASCADE)
    cleaned = models.BooleanField(default=False)
    clean_cost = models.IntegerField(default=5)  # Cost to clean up the rubbish
    cleaned_at = models.DateTimeField(null=True, blank=True)  # Track when it was cleaned

    def should_respawn(self):
        """Check if rubbish should reappear after 3 days and deduct sustainability points."""
        if self.cleaned and self.cleaned_at:
            # If the rubbish has been cleaned and 3 days have passed
            if (now() - self.cleaned_at).days >= 3:
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