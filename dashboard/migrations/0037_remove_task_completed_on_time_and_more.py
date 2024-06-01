# Generated by Django 5.0.3 on 2024-06-01 20:57

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0036_task_completed_on_time_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='completed_on_time',
        ),
        migrations.AddField(
            model_name='taskbid',
            name='completed_on_time',
            field=models.BooleanField(default=False),
        ),
    ]
