# Generated by Django 3.0.7 on 2020-07-29 21:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0011_builds_price_hidden'),
    ]

    operations = [
        migrations.AddField(
            model_name='cars',
            name='car_purchased',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='cars',
            name='price',
            field=models.FloatField(default=0),
        ),
    ]
