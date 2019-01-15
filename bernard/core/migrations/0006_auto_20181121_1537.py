# Generated by Django 2.1.2 on 2018-11-21 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0005_auto_20181118_1859'),
    ]

    operations = [
        migrations.AddField(
            model_name='driver',
            name='phone',
            field=models.CharField(blank=True, max_length=30),
        ),
        migrations.AddField(
            model_name='driver',
            name='travel_mode',
            field=models.IntegerField(choices=[(0, 'driving'), (1, 'bicycling')], default=0),
        ),
    ]