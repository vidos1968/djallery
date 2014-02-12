# Create your views here.
#-*-coding:utf8-*-

from django.shortcuts import render_to_response
from models import ImageItem, GalleryGroup
from django.conf import settings
from os import listdir, chdir, rename

from re import match, sub
from models import ImageItem

def _img_renamer():
    chdir(settings.MEDIA_ROOT + "gallery/")
    for i in listdir("."):
        if match(r"^.*thumb.*$", i):
            continue

        if match(r"^.*[Jj][Pp][Gg]$", i):
            try:
                img = ImageItem.objects.get(img = "gallery/" + i)
            except ImageItem.DoesNotExist:
                rename(i, i + ".zzz")
                continue

            print img.img.name
            new_name = sub(r"[Jj][Pp](E|e|)[Gg]$", "jpg", i)
            print "->" + new_name
            rename(i, new_name)
            img.img.name = sub(r"[Jj][Pp](E|e|)[Gg]$", "jpg", img.img.__str__())
            img.save()


def all_albums(request):
    """Показывает альбомы"""

    groups = GalleryGroup.objects.all()
    albums = []

    for g in groups:
        cover = ImageItem.objects.all().filter(group = g)
        cover = cover[0]
        albums.append({"id": g.id, "caption": g.name, "cover": cover.img.name})

    return render_to_response("albums.html", {'album_list': albums})

def all_images(request):
    """ subj ;-) """
    img = ImageItem.objects.all()
    return render_to_response("gallery.html", {'images': img })    

def image(request, img_id):
    """ show image with id == img_id """
    img = ImageItem.objects.get(id=img_id)
    return render_to_response("image.html", {'images': img})

def image_group(request, group):
    """ show all images placed in group 'group' """
    grp = GalleryGroup.objects.get( id = group )
    img = ImageItem.objects.filter(group = grp)
    return render_to_response("gallery.html", {'images': img, 'caption': grp.name,})

