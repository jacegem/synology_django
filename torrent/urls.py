from django.conf.urls import url

from . import views

app_name = 'torrent'

urlpatterns = [
    # ex: /torrent/
    url(r'^$', views.index, name='index'),
    # ex: /torrent/collect/
    url(r'^collect/$', views.collect, name='collect'),
    # ex: /torrent/rss/
    url(r'^rss/$', views.rss, name='rss'),
]