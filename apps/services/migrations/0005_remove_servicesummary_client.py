# Generated by Django 5.1.1 on 2024-09-24 06:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0004_clientservices_currency_clientservices_image_url'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='servicesummary',
            name='client',
        ),
    ]
