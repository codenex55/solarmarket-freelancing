# Generated by Django 5.0.3 on 2024-04-04 17:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0006_alter_task_timestamp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='timestamp',
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
