# Generated by Django 5.0.3 on 2024-05-24 06:23

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0016_taskbid_expected_delivery_time_measurement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='accepted_bid',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='accepted_for_task', to='dashboard.taskbid'),
        ),
    ]
