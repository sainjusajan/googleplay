# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 19:39
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playmovies', '0006_movie_movieimage'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='releaseDate',
            field=models.CharField(default='', max_length=50),
            preserve_default=False,
        ),
    ]
