# Generated by Django 3.0.7 on 2020-06-20 13:35

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
            name='Builds',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=150)),
                ('total', models.FloatField()),
                ('private', models.BooleanField(default=False)),
                ('views', models.IntegerField(default=0)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Cars',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('make', models.CharField(max_length=30)),
                ('model', models.CharField(max_length=30)),
                ('trim', models.CharField(max_length=45)),
                ('year', models.CharField(max_length=4)),
                ('price', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Domains',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('domain', models.CharField(max_length=50)),
                ('price_element', models.CharField(max_length=50)),
                ('attr', models.CharField(choices=[('1', 'id'), ('2', 'class')], default='1', max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='EngineCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='ExteriorCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='InteriorCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='RunningCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50)),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Running',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('price', models.FloatField(default=0)),
                ('purchased', models.BooleanField(default=False)),
                ('build_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='builds.Builds')),
                ('running_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='builds.RunningCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Interior',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('price', models.FloatField(default=0)),
                ('purchased', models.BooleanField(default=False)),
                ('build_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='builds.Builds')),
                ('interior_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='builds.InteriorCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Exterior',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('price', models.FloatField(default=0)),
                ('purchased', models.BooleanField(default=False)),
                ('build_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='builds.Builds')),
                ('exterior_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='builds.ExteriorCategory')),
            ],
        ),
        migrations.CreateModel(
            name='Engine',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('link', models.URLField()),
                ('price', models.FloatField(default=0)),
                ('purchased', models.BooleanField(default=False)),
                ('build_parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='builds.Builds')),
                ('engine_category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='builds.EngineCategory')),
            ],
        ),
        migrations.AddField(
            model_name='builds',
            name='car',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='builds.Cars'),
        ),
        migrations.AddField(
            model_name='builds',
            name='engine_parts',
            field=models.ManyToManyField(to='builds.Engine'),
        ),
        migrations.AddField(
            model_name='builds',
            name='exterior_parts',
            field=models.ManyToManyField(to='builds.Exterior'),
        ),
        migrations.AddField(
            model_name='builds',
            name='interior_parts',
            field=models.ManyToManyField(to='builds.Interior'),
        ),
        migrations.AddField(
            model_name='builds',
            name='running_gear_parts',
            field=models.ManyToManyField(to='builds.Running'),
        ),
    ]
