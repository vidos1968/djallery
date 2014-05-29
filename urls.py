# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from views import all_images, image, album_photos, all_albums

urlpatterns = patterns('',
    url(r'^$', all_albums, name='all_albums'),
    (r'^image/(?P<img_id>.*)/$', image),
    (r'^album/(?P<album_id>.*)/$', album_photos),
)
