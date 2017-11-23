from django.conf.urls import url
from . import views

app_name = 'playmovies'


urlpatterns = [
    # url(r'^$', views.MovieListView.as_view(), name='allmovies'),
    url(r'^$', views.datewiseWebsite, name='allmovies'),
    url(r'^tvseries/$', views.episodeList, name='tvseries'),
    url(r'^movies/(?P<pk>\d+)/$', views.MovieDetailView.as_view(), name='moviedetail'),
]