# Generated by Django 5.0.3 on 2024-05-27 07:24

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0005_remove_employer_bookmarked_freelancers_and_more'),
        ('dashboard', '0020_freelancernotification'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='freelancernotification',
            name='employer',
        ),
        migrations.AddField(
            model_name='freelancernotification',
            name='freelancer',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.freelancer'),
        ),
        migrations.AlterField(
            model_name='freelancernotification',
            name='notification_category',
            field=models.CharField(choices=[('review', 'review'), ('hired', 'hired'), ('due date', 'due date')], max_length=50),
        ),
        migrations.CreateModel(
            name='EmployerNotification',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('notification_category', models.CharField(choices=[('review', 'review'), ('bid', 'bid'), ('task expiring', 'task expiring')], max_length=50)),
                ('read', models.BooleanField(default=False)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('employer', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='accounts.employer')),
            ],
        ),
    ]
