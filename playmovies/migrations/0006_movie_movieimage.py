# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-16 18:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playmovies', '0005_auto_20171115_1706'),
    ]

    operations = [
        migrations.AddField(
            model_name='movie',
            name='movieImage',
            field=models.ImageField(default='', upload_to='movies/%Y/%m/%d'),
        ),
    ]
