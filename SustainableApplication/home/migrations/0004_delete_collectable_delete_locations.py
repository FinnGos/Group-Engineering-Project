# Generated by Django 5.1.5 on 2025-03-13 10:20

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0003_collectable_locations'),
    ]

    operations = [
        migrations.DeleteModel(
            name='Collectable',
        ),
        migrations.DeleteModel(
            name='Locations',
        ),
    ]
