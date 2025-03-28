from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Collectable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, unique=True)),
                ('image', models.ImageField(default='placeholder.jpg', upload_to='media/')),
                ('fact', models.CharField(default='', max_length=1000)),
            ],
        ),
    ]
