# Generated by Django 5.1.1 on 2024-09-23 10:11

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='availabletime',
            name='date_object',
        ),
        migrations.DeleteModel(
            name='AvailableDates',
        ),
        migrations.DeleteModel(
            name='AvailableTime',
        ),
    ]
