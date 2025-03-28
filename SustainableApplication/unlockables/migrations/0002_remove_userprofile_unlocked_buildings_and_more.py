# Generated by Django 5.1.6 on 2025-03-20 19:20

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collectables', '0001_initial'),
        ('unlockables', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='unlocked_buildings',
        ),
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.CreateModel(
            name='UserInventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('purchased_items', models.ManyToManyField(blank=True, to='unlockables.item')),
                ('unlocked_buildings', models.ManyToManyField(blank=True, to='collectables.collectable')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='Building',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
