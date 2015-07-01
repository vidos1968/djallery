# -*- coding: utf-8 -*-

from django.conf.urls import patterns, url
from views import AlbumList, AlbumDetail

urlpatterns = patterns('',
    url(r'^$', AlbumList.as_view(), name='all_albums'),
    url(r'^album/(?P<pk>.*)/$', AlbumDetail.as_view()),
)
