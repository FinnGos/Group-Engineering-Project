# Generated by Django 5.1.6 on 2025-03-21 16:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unlockables', '0008_alter_useritem_x_alter_useritem_y'),
    ]

    operations = [
        migrations.AddField(
            model_name='building',
            name='x',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='building',
            name='y',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
