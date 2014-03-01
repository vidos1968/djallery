# -*- coding: utf-8 -*-

from django.shortcuts import render_to_response
from models import Photo, Album
from django.conf import settings
from os import listdir, chdir, rename

from re import match, sub
from models import Photo

def _img_renamer():
    chdir(settings.MEDIA_ROOT + "gallery/")
    for i in listdir("."):
        if match(r"^.*thumb.*$", i):
            continue

        if match(r"^.*[Jj][Pp][Gg]$", i):
            try:
                img = Photo.objects.get(img = "gallery/" + i)
            except Photo.DoesNotExist:
                rename(i, i + ".zzz")
                continue

            print img.img.name
            new_name = sub(r"[Jj][Pp](E|e|)[Gg]$", "jpg", i)
            print "->" + new_name
            rename(i, new_name)
            img.img.name = sub(r"[Jj][Pp](E|e|)[Gg]$", "jpg", img.img.__str__())
            img.save()

def album_cover(album, size=(320,320)):
    """
    Creates or find album cover
    @return cover filename
    """

    from PIL import Image
    from os.path import join, isfile

    tsize = size[0]/1
    tsize = (tsize,tsize)

    cover_filename = "album_" + str(album.id) + ".cover.jpg"
    fullpath = join(settings.MEDIA_ROOT, cover_filename)

    cover = Image.new("RGBA", size, 0)

    if isfile(cover_filename) and not settings.DEBUG:
        return cover_filename

    offset = 0
    images = Photo.objects.filter(group=album)

    if len(images) > 3:
        images = images[0:3]

    for i in images:
        # используя i.img.name можно наткнуться на UnicodeEncodeError
        # с русскими именами файлов.
        # преобразование объекта в строку даёт нужный результат
        i = Image.open(settings.MEDIA_ROOT + str(i.img))

        # подгоняем миниатюры под квадрат
        # изображение растягивается так, чтобы меньшая сторона
        # полностью заполнила пространство
        if i.size[0] > i.size[1]:
            i.thumbnail((tsize[0]*2,tsize[0]), Image.ANTIALIAS)
        else:
            i.thumbnail((tsize[0],tsize[0]*2), Image.ANTIALIAS)

        # средняя ширина изображения
        wmiddle = size[0]/len(images)
        x = (i.size[0]-wmiddle)/2

        i = i.crop((x,0,x+wmiddle,size[1]))

        cover.paste(i, (offset,0))
        offset += wmiddle

    cover.save(fullpath)
    return cover_filename


def all_albums(request):
    """Показывает альбомы"""

    groups = Album.objects.all()
    albums = []

    for g in groups:
        cover = album_cover(g)
        albums.append({"id": g.id, "caption": g.name, "cover": cover})

    return render_to_response("albums.html", {'album_list': albums})

def all_images(request):
    """ subj ;-) """
    img = Photo.objects.all()
    return render_to_response("gallery.html", {'images': img })    

def image(request, img_id):
    """ show image with id == img_id """
    img = Photo.objects.get(id=img_id)
    return render_to_response("image.html", {'images': img})

def image_group(request, group):
    """ show all images placed in group 'group' """
    grp = Album.objects.get( id = group )
    img = Photo.objects.filter(group = grp)
    return render_to_response("gallery.html", {'images': img, 'caption': grp.name,})

