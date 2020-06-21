# Generated by Django 3.0.7 on 2020-06-21 18:10

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('builds', '0002_auto_20200620_1623'),
    ]

    operations = [
        migrations.AddField(
            model_name='builds',
            name='dislikes',
            field=models.ManyToManyField(related_name='builds_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='builds',
            name='likes',
            field=models.ManyToManyField(related_name='builds_likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
