# Generated by Django 5.1.5 on 2025-02-24 18:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0002_remove_tasks_lat_location_remove_tasks_long_location_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tasks',
            name='location',
        ),
        migrations.AddField(
            model_name='tasks',
            name='location_id',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
