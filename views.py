# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response, get_object_or_404
from django.http import Http404

from models import *

def album_photos(request, pk):
    """ show all images placed in group 'group' """
    a = get_object_or_404(Album, id=pk)
    p = Photo.objects.filter(group=a)

    return render_to_response("gallery/photo_list.html", {
        'photos': p,
        'caption': a.name,
   })
