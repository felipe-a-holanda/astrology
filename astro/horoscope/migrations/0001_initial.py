# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Ephemeris',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sun', models.FloatField(verbose_name='Sun')),
                ('moon', models.FloatField(verbose_name='Moon')),
                ('mercury', models.FloatField(verbose_name='Mercury')),
                ('venus', models.FloatField(verbose_name='Venus')),
                ('mars', models.FloatField(verbose_name='Mars')),
                ('jupiter', models.FloatField(verbose_name='Jupiter')),
                ('saturn', models.FloatField(verbose_name='Saturn')),
                ('uranus', models.FloatField(verbose_name='Uranus')),
                ('neptune', models.FloatField(verbose_name='Neptune')),
                ('pluto', models.FloatField(verbose_name='Pluto')),
                ('mean_node', models.FloatField()),
                ('true_node', models.FloatField()),
                ('mean_apog', models.FloatField()),
                ('oscu_apog', models.FloatField()),
                ('earth', models.FloatField()),
                ('chiron', models.FloatField()),
                ('pholus', models.FloatField()),
                ('ceres', models.FloatField()),
                ('pallas', models.FloatField()),
                ('juno', models.FloatField()),
                ('vesta', models.FloatField()),
                ('intp_apog', models.FloatField()),
                ('intp_perg', models.FloatField()),
            ],
            options={
                'verbose_name': 'ephemeris',
                'verbose_name_plural': 'ephemeris',
            },
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=256)),
                ('date', models.DateTimeField()),
                ('ephemeris', models.OneToOneField(related_name='event', to='horoscope.Ephemeris')),
            ],
            options={
                'verbose_name': 'event',
                'verbose_name_plural': 'events',
            },
        ),
        migrations.CreateModel(
            name='Houses',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('house_1', models.FloatField()),
                ('house_2', models.FloatField()),
                ('house_3', models.FloatField()),
                ('house_4', models.FloatField()),
                ('house_5', models.FloatField()),
                ('house_6', models.FloatField()),
                ('house_7', models.FloatField()),
                ('house_8', models.FloatField()),
                ('house_9', models.FloatField()),
                ('house_10', models.FloatField()),
                ('house_11', models.FloatField()),
                ('house_12', models.FloatField()),
            ],
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('city', models.CharField(max_length=512)),
                ('state', models.CharField(max_length=512)),
                ('country', models.CharField(max_length=512)),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
            ],
            options={
                'verbose_name': 'location',
                'verbose_name_plural': 'locations',
            },
        ),
        migrations.AddField(
            model_name='event',
            name='houses',
            field=models.OneToOneField(related_name='event', to='horoscope.Houses'),
        ),
        migrations.AddField(
            model_name='event',
            name='location',
            field=models.ForeignKey(related_name='events', to='horoscope.Location', null=True),
        ),
        migrations.AddField(
            model_name='event',
            name='user',
            field=models.ForeignKey(related_name='events', to='profiles.UserProfile', null=True),
        ),
    ]
