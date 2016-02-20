# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-02-20 15:38
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('alpacastats', '0003_track_event'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='active_track',
            field=models.BooleanField(default=False),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='track',
            name='event',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='alpacastats.Event'),
        ),
    ]
