# Generated by Django 3.0.7 on 2020-07-29 21:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0012_auto_20200729_2213'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cars',
            old_name='car_purchased',
            new_name='purchased',
        ),
    ]
