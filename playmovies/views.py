# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic import ListView, DetailView
# django project name is adleads, replace adleads with your project name
from playmovies.models import Actor, Director, Writer, Producer, Genre, Movie, Day, Website, TVSeries
from datetime import date, datetime
from django.shortcuts import get_object_or_404

# playmovies UI views
class MovieListView(ListView):
    model = Movie
    template_name = 'playmovies/movie_list.html'


class MovieDetailView(DetailView):
    model = Movie
    template_name = "playmovies/movie_detail.html"


def datewiseWebsite(request):
    if request.method == 'POST':
        print(request.POST.get('date'))
        querydate = datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
        website = Website.objects.get(day=Day.objects.get(day=querydate))
        print(website)
    else:
        today = Day.objects.get(day=date.today())
        # today = get_object_or_404(Day, day=date.today())
        website = Website.objects.get(day=today)
        # website = Website.objects.filter(day=Day(day=date(2017,11,20)))
        print("hello", website)
    return render(request, 'playmovies/movie_list.html', {'website': website})


def datewiseWebsiteForTv(request):
    if request.method == 'POST':
        print(request.POST.get('date'))
        querydate = datetime.strptime(request.POST.get('date'), '%Y-%m-%d')
        website = Website.objects.get(day=Day.objects.get(day=querydate))
        print(website)
    else:
        today = Day.objects.get(day=date.today())
        # today = get_object_or_404(Day, day=date.today())
        website = Website.objects.get(day=today)
        # website = Website.objects.filter(day=Day(day=date(2017,11,20)))
        # print("hello", website)
    return render(request, 'playmovies/tvseries_list.html', {'website': website})

def tvserieslist(request):
    tvseries = TVSeries.objects.all()
    return render(request, 'playmovies/tvseries_list.html', {'tvseries': tvseries})

# class TVSeriesDetailView(DetailView):
#     model = TVSeries
#     template_name = "playmovies/tvseries_detail.html"


def TVSeriesDetailView(request, pk, year=None, month=None, day=None):
    mydate = year+'-'+month+'-'+day
    tvseries_id = TVSeries.objects.get(pk=pk)
    tvSeriesAll = TVSeries.objects.filter(name=tvseries_id.name, date=datetime.strptime(mydate, '%Y-%m-%d'))

    tvSeasonAll = [i.season for i in tvSeriesAll]

    print(tvSeriesAll)
    print(tvseries_id.name)
    print(int(year))
    return render(request, 'playmovies/tvseries_detail.html', {'tvseries':tvseries_id, 'tvSeasonAll':tvSeasonAll})
