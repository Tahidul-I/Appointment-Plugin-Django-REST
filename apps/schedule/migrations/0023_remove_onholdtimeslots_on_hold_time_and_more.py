# Generated by Django 5.1.1 on 2024-11-07 08:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('schedule', '0022_basetimeslot'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='onholdtimeslots',
            name='on_hold_time',
        ),
        migrations.AddField(
            model_name='onholdtimeslots',
            name='created_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='onholdtimeslots',
            name='on_hold',
            field=models.BooleanField(default=False),
        ),
    ]
