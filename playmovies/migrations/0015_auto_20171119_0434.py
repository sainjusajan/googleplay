# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-11-19 04:34
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('playmovies', '0014_auto_20171119_0403'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='poster',
            field=models.CharField(max_length=350),
        ),
    ]
