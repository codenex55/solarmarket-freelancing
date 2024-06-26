# Generated by Django 5.0.3 on 2024-05-30 14:45

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dashboard', '0034_alter_employernotification_notification_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='employernotification',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.privatemessage'),
        ),
        migrations.AddField(
            model_name='freelancernotification',
            name='message',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='dashboard.privatemessage'),
        ),
    ]
