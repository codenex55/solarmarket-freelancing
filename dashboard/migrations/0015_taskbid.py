# Generated by Django 5.0.3 on 2024-04-22 20:19

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_employer_bookmarked_freelancers_and_more'),
        ('dashboard', '0014_remove_task_task_images_taskfile'),
    ]

    operations = [
        migrations.CreateModel(
            name='TaskBid',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bid_amount', models.DecimalField(decimal_places=2, max_digits=10)),
                ('expected_delivery_time', models.CharField(max_length=50)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('freelancer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.freelancer')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='bids', to='dashboard.task')),
            ],
        ),
    ]
