# Generated by Django 3.0.7 on 2020-06-20 15:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('builds', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='engine',
            name='build_parent',
        ),
        migrations.RemoveField(
            model_name='exterior',
            name='build_parent',
        ),
        migrations.RemoveField(
            model_name='interior',
            name='build_parent',
        ),
        migrations.RemoveField(
            model_name='running',
            name='build_parent',
        ),
    ]
