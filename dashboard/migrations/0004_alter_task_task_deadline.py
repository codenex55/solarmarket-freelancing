# Generated by Django 5.0.3 on 2024-04-04 16:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0003_task_task_deadline'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='task_deadline',
            field=models.DateTimeField(),
        ),
    ]
