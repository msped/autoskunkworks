# Generated by Django 3.0.7 on 2020-06-21 21:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0003_auto_20200621_1910'),
    ]

    operations = [
        migrations.AddField(
            model_name='builds',
            name='dislike_count',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='builds',
            name='like_count',
            field=models.IntegerField(default=1),
        ),
    ]
