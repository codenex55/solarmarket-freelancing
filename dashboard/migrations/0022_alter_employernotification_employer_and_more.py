# Generated by Django 5.0.3 on 2024-05-27 07:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_employer_bookmarked_freelancers_and_more'),
        ('dashboard', '0021_remove_freelancernotification_employer_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employernotification',
            name='employer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.employer'),
        ),
        migrations.AlterField(
            model_name='freelancernotification',
            name='freelancer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.freelancer'),
        ),
    ]