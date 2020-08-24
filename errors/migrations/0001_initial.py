# Generated by Django 3.0.7 on 2020-08-23 23:42

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Issue',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(choices=[('1', 'bug'), ('2', 'duplicate'), ('3', 'enhancement'), ('4', 'wont fix'), ('5', 'question'), ('6', 'other')], default='1', max_length=11)),
                ('issue_open', models.BooleanField(default=True)),
                ('issue_location', models.CharField(choices=[('1', 'Home'), ('2', 'Create Build'), ('3', 'Edit Build'), ('4', 'Delete Build'), ('5', 'Builds Searching'), ('7', 'Updating Profile'), ('8', 'Changing Password'), ('9', 'Account Deactivation'), ('10', 'Other')], default='10', max_length=20)),
                ('priority', models.CharField(choices=[('1', 'Low'), ('2', 'Medium'), ('3', 'High'), ('4', 'Critical'), ('5', 'New')], default='5', max_length=8)),
                ('description', models.TextField()),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]