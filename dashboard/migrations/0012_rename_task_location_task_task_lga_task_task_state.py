# Generated by Django 5.0.3 on 2024-04-21 04:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0011_privatechat_privatemessage_delete_employerbookmarked'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='task_location',
            new_name='task_lga',
        ),
        migrations.AddField(
            model_name='task',
            name='task_state',
            field=models.CharField(default='Abak', max_length=100),
            preserve_default=False,
        ),
    ]