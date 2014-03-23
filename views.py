# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from models import Photo, Album
from django.conf import settings
from os import listdir, chdir, rename

from re import match, sub
from models import Photo


def all_albums(request):
    """Показывает альбомы"""

    albums = Album.objects.all()

    for g in albums:
        g.cover = g.cover()

    return render_to_response("gallery/albums.html", {'album_list': albums})

def all_images(request):
    """ subj ;-) """
    img = Photo.objects.all()
    return render_to_response("gallery.html", {'images': img })    

def image(request, img_id):
    """ show image with id == img_id """
    img = Photo.objects.get(id=img_id)
    return render_to_response("image.html", {'images': img})

def album_photos(request, album_id):
    """ show all images placed in group 'group' """
    album = Album.objects.get( id = album_id )
    img = Photo.objects.filter(group = album)
    return render_to_response("gallery/album_photos.html", {'images': img, 'caption': album.name,})

