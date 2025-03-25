from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('collectables', '0001_initial'),
        ('home', '0005_customuser_selected_task_customuser_task_assign_date'),
    ]

    """operations = [
        migrations.AddField(
            model_name='customuser',
            name='collectables_owned',
            field=models.ManyToManyField(blank=True, to='collectables.collectable'),
        ),
    ]"""
