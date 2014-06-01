# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic import ListView
from views import *
from models import *

urlpatterns = patterns('',
    url(r'^$', ListView.as_view(model=Album), name='all_albums'),
    (r'^album/(?P<pk>.*)/$', album_photos),
)
