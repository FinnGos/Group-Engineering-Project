# Generated by Django 5.1.6 on 2025-03-21 14:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('unlockables', '0004_mapslot'),
    ]

    operations = [
        migrations.AddField(
            model_name='item',
            name='item_type',
            field=models.CharField(choices=[('building', 'Building'), ('sustainable', 'Sustainable Item')], default='sustainable', max_length=20),
        ),
        migrations.AddField(
            model_name='item',
            name='x_position',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='item',
            name='y_position',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='mapslot',
            name='is_unlocked',
            field=models.BooleanField(default=False),
        ),
    ]
