# Generated by Django 5.0.3 on 2024-05-08 21:38

import cloudinary.models
import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('forum', '0002_alter_post_content'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('date_posted', models.DateTimeField(auto_now_add=True)),
                ('image', cloudinary.models.CloudinaryField(default='https://res.cloudinary.com/dmpxni4ku/image/upload/v1714992400/default_question_image_vie1nx.webp', max_length=255, verbose_name='image')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
