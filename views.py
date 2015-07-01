# -*- coding: utf-8 -*-
from django.views.generic import ListView, DetailView
from models import Album, Photo


class AlbumDetail(DetailView):
    model = Album
    queryset = Album.objects.all().prefetch_related('photo_set')


class AlbumList(ListView):
    model = Album
