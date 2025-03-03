from django.core.management.base import BaseCommand
from tasks.models import Tasks
from Checkin.models import Location


class Command(BaseCommand):
    """Allows us to run this file to sync tasks with locations in the database"""

    help = "Creates tasks for locations in the database"

    def handle(self, *args, **kwargs):
        # fetch locations from the databse
        locations = Location.objects.using("location_db").all()
        created_count = 0
        existing_count = 0

        for location in locations:
            task, created = Tasks.objects.get_or_create(
                task_name=f"Task at {location.name}",
                location_id=location.id,
                defaults={
                    "reward": 10,  # default reward
                    "target": 100,  # default target
                },
            )
            if created:
                created_count += 1
                self.stdout.write(
                    self.style.SUCCESS(f"Created task for {location.name}")
                )
            else:
                existing_count += 1
                self.stdout.write(
                    self.style.WARNING(f"Task for {location.name} already exists")
                )

        self.stdout.write(
            self.style.SUCCESS(
                f"\nSummary: {created_count} tasks created, {existing_count} tasks already existed."
            )
        )
