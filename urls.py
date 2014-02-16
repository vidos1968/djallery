# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.views.generic.simple import direct_to_template
from views import all_images, image, image_group, all_albums

urlpatterns = patterns('',
    # put into your_project.urls.py next line
    # (r'^gallery/$', include('gallery.urls')),
    (r'^$', all_albums),
    (r'^image/(?P<img_id>.*)/$', image),
    (r'^group/(?P<group>.*)/$', image_group),
)
