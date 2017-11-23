# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin
from .models import Actor, Director, Producer, Writer, Genre, Movie, Day, Website, TVEpisode, TVSeason, TVSeries


admin.site.register(Actor)
admin.site.register(Director)
admin.site.register(Producer)
admin.site.register(Writer)
admin.site.register(Genre)
admin.site.register(Movie)
admin.site.register(Day)
admin.site.register(Website)
admin.site.register(TVSeries)
admin.site.register(TVSeason)
admin.site.register(TVEpisode)