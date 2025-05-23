# Generated by Django 5.1.1 on 2024-11-14 05:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('booking', '0002_delete_appointmentbooking'),
        ('client', '0005_companyprofile'),
        ('staff', '0002_staffprofile_delete_clientstaff'),
    ]

    operations = [
        migrations.CreateModel(
            name='AppointmentBooking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('time_slot', models.TimeField()),
                ('selected_date', models.DateField()),
                ('name', models.CharField(max_length=500)),
                ('email', models.EmailField(max_length=254)),
                ('phone', models.CharField(max_length=20)),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_related_client', to='client.clientprofile')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_related_service', to='staff.staffprofile')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointment_related_staff', to='staff.staffprofile')),
            ],
        ),
    ]
