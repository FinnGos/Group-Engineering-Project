# Generated by Django 5.1.6 on 2025-03-20 21:44

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('unlockables', '0002_remove_userprofile_unlocked_buildings_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userinventory',
            name='unlocked_buildings',
        ),
    ]
