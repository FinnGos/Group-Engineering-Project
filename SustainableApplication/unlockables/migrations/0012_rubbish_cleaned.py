# Generated by Django 5.1.6 on 2025-03-22 11:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unlockables', '0011_rubbish'),
    ]

    operations = [
        migrations.AddField(
            model_name='rubbish',
            name='cleaned',
            field=models.BooleanField(default=False),
        ),
    ]
