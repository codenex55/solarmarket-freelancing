# Generated by Django 5.0.3 on 2024-04-04 20:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0007_alter_task_timestamp'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Category',
            new_name='TaskCategory',
        ),
    ]