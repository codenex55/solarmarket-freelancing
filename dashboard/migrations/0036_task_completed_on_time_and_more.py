# Generated by Django 5.0.3 on 2024-06-01 20:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0035_employernotification_message_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='completed_on_time',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='taskbid',
            name='completed_within_budget',
            field=models.BooleanField(default=False),
        ),
    ]