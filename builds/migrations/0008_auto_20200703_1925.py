# Generated by Django 3.0.7 on 2020-07-03 18:25

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('builds', '0007_auto_20200624_0031'),
    ]

    operations = [
        migrations.AlterField(
            model_name='builds',
            name='dislikes',
            field=models.ManyToManyField(blank=True, related_name='builds_dislikes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='builds',
            name='engine_parts',
            field=models.ManyToManyField(blank=True, to='builds.Engine'),
        ),
        migrations.AlterField(
            model_name='builds',
            name='exterior_parts',
            field=models.ManyToManyField(blank=True, to='builds.Exterior'),
        ),
        migrations.AlterField(
            model_name='builds',
            name='interior_parts',
            field=models.ManyToManyField(blank=True, to='builds.Interior'),
        ),
        migrations.AlterField(
            model_name='builds',
            name='likes',
            field=models.ManyToManyField(blank=True, related_name='builds_likes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='builds',
            name='running_gear_parts',
            field=models.ManyToManyField(blank=True, to='builds.Running'),
        ),
    ]
