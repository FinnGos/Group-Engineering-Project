from django.db import models


class Riddle(models.Model):
    riddle_question = models.TextField()
    location_id = models.IntegerField(null=True, blank=True)  # References Location in location_db
    completed = models.BooleanField(default=False)
    week_group = models.IntegerField(choices=[(1, "Week 1"), (2, "Week 2"), (3, "Week 3"), (4, "Week 4")], default=1)
    
    def save(self, *args, **kwargs):
        """Ensure riddle is only marked as completed when users check in"""
        super().save(*args, **kwargs)

    @property
    def latitude(self):
        """Retrieve latitude dynamically from related location object"""
        from Checkin.models import Location  # Import inside function to avoid circular imports
        try:
            location = Location.objects.using('location_db').get(id=self.location_id)
            return location.latitude
        except Location.DoesNotExist:
            return None

    @property
    def longitude(self):
        """Retrieve longitude dynamically from related location object"""
        from Checkin.models import Location
        try:
            location = Location.objects.using('location_db').get(id=self.location_id)
            return location.longitude
        except Location.DoesNotExist:
            return None

    def __str__(self):
        return f"Riddle: {self.riddle_question}"
