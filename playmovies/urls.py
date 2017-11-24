from django.conf.urls import url
from . import views

app_name = 'playmovies'


urlpatterns = [
    # url(r'^$', views.MovieListView.as_view(), name='allmovies'),
    url(r'^$', views.datewiseWebsite, name='allmovies'),
    url(r'^tvseries/$', views.datewiseWebsiteForTv, name='tvseries'),
    url(r'^movies/(?P<pk>\d+)/$', views.MovieDetailView.as_view(), name='moviedetail'),
    url(r'^tvseries/(?P<pk>\d+)/(?P<year>[0-9]{4})/(?P<month>[0-9]{2})/(?P<day>[0-9]{2})/$', views.TVSeriesDetailView, name='tvseriesdetail'),
]