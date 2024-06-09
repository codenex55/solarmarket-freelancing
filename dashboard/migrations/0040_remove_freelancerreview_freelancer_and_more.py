# Generated by Django 5.0.3 on 2024-06-09 07:10

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_employer_bookmarked_freelancers_and_more'),
        ('dashboard', '0039_alter_freelancerreview_task'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freelancerreview',
            name='freelancer',
        ),
        migrations.RemoveField(
            model_name='freelancerreview',
            name='reviewer',
        ),
        migrations.RemoveField(
            model_name='freelancerreview',
            name='task',
        ),
        migrations.CreateModel(
            name='TaskReview',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('star_rating', models.IntegerField(blank=True, null=True)),
                ('review', models.TextField(blank=True, null=True)),
                ('rated', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('employer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.employer')),
                ('task', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='dashboard.task')),
            ],
        ),
        migrations.DeleteModel(
            name='EmployerReview',
        ),
        migrations.DeleteModel(
            name='FreelancerReview',
        ),
    ]