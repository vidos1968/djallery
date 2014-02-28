# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from PIL import Image
from re import sub, match
from gallery.models import Album, Photo
import os

# Регистрируем новую библиотеку тегов
register = template.Library()

def _add_thumb(s, ext="thumb"):
    """
    Изменяет строку (имя файла, URL), содержащую имя файла изображения,
    вставляя 'thumb' перед расширением имени файла (которое изменяется
    на '.jpg'
    """
    if match(r"^.*\."+ext+"\..*$", s):
        return s + "z"

    parts = s.split(".")
    parts.insert(-1, ext)
    if parts[-1].lower() not in ['jpeg', 'jpg']:
        parts[-1] = 'jpg'
    return ".".join(parts)

@register.simple_tag
def thumb(imgname, size = 300):
    """Return thumb filename.
    Вся заморочь в том, что Photo из models.py возвращает путь сохранения что-то вроде 'gallery/imagename.ext'
    Поэтому чтобы проверить существование файла нужно в начало добавить MEDIA_ROOT (тоесть расположение медиафайлов на ФС)
    В шаблон же возвращать необходимо MEDIA_URL + имя_необходимого_файла """
    fullpath = settings.MEDIA_ROOT + str(imgname)
    thumb = _add_thumb(str(imgname), ext="thumb"+str(size))

    if os.access(thumb, os.F_OK):
        return thumb
    else:
        if os.access(fullpath, os.F_OK):
            img = Image.open(fullpath)
            img.thumbnail((size, size), Image.ANTIALIAS)
            img.save(_add_thumb(fullpath, ext="thumb"+str(size)), 'JPEG')
            return settings.MEDIA_URL + _add_thumb(str(imgname), ext="thumb"+str(size))
        else:
            return settings.MEDIA_URL + "broken.jpg"


def album(context):
    """Показывает альбомы"""

    from gallery.views import album_cover

    groups = Album.objects.all()
    images = []
    
    for g in groups:
        cover = album_cover(g)
        images.append({"id": g.id, "caption": g.name, "cover": cover})

    context['images'] = images
    return context
register.inclusion_tag("gallery/top_images.html", takes_context=True)(album)
