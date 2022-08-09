# Generated by Django 3.2.7 on 2022-05-01 00:16

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0015_builds_qrcode'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cars',
            name='year',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1900), django.core.validators.MaxValueValidator(2022)]),
        ),
    ]