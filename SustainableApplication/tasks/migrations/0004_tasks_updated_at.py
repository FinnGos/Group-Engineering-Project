# Generated by Django 5.1.5 on 2025-03-03 14:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('tasks', '0003_remove_tasks_location_tasks_location_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='tasks',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
