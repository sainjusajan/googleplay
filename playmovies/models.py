# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.utils.timezone import now
import datetime


class Actor(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=70, default='')

    def __str__(self):
        return self.name

class Director(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=70, default='')
    
    def __str__(self):
        return self.name

class Producer(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=70, default='')
    
    def __str__(self):
        return self.name

class Writer(models.Model):
    name = models.CharField(max_length=50)
    url = models.CharField(max_length=70, default='')
    
    def __str__(self):
        return self.name

class Genre(models.Model):
    name = models.CharField(max_length=20)
    url = models.CharField(max_length=70, default='')
    
    def __str__(self):
        return self.name

class Movie(models.Model):
    name = models.CharField(max_length=50)
    poster = models.CharField(max_length=200)
    length = models.CharField(max_length=10)
    releaseDate = models.CharField(max_length=50, default='')
    genre = models.ManyToManyField(Genre)
    rating = models.CharField(max_length=4)
    n_raters = models.CharField(max_length=15)
    trailer = models.CharField(max_length=200)
    description = models.TextField(default='')
    actors = models.ManyToManyField(Actor)
    directors = models.ManyToManyField(Director)
    producers = models.ManyToManyField(Producer)
    writers = models.ManyToManyField(Writer)
    url = models.CharField(max_length=100, default='')
    date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.name + " for " + str(self.date)



class TVEpisode(models.Model):
    number = models.CharField(max_length=15)
    name = models.CharField(max_length=50, default='')
    description = models.TextField()
    # trailer = models.CharField(max_length=200)
    poster = models.CharField(max_length=200)
    url = models.CharField(max_length=50)
    cost = models.CharField(max_length=10)

    def __str__(self):
        return self.name


class TVSeason(models.Model):
    name = models.CharField(max_length=50)
    episodes = models.ManyToManyField(TVEpisode)
    cost = models.CharField(max_length=10)
    url = models.CharField(max_length=200, default='')

    def __str__(self):
        return self.name


class TVSeries(models.Model):
    name = models.CharField(max_length=50, default='')
    description = models.TextField(default='')
    url = models.CharField(max_length=200)
    rating = models.CharField(max_length=4)
    n_raters = models.CharField(max_length=15, default='')
    category = models.ManyToManyField(Genre)
    releaseDate = models.CharField(max_length=10)
    poster = models.CharField(max_length=200)
    season = models.ForeignKey(TVSeason)
    date = models.DateField(default=datetime.date.today())

    def __str__(self):
        return self.name + " " + self.season.name + " for " + str(self.date)


class Day(models.Model):
    day = models.DateField()
    movies = models.ManyToManyField(Movie)
    tvseries = models.ManyToManyField(TVSeries)
    def __str__(self):
        return str(self.day)



class Website(models.Model):
    day = models.ForeignKey(Day)

    def __str__(self):
        return "Website for " + str(self.day)
