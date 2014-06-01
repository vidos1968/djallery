# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from PIL import Image
from re import sub, match
from ..models import Album, Photo
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

@register.simple_tag
def thumb_square(imgname, size=300):
    """Return thumb filename.
       отличается тем, что создаёт квадратное превью """
    fullpath = settings.MEDIA_ROOT + str(imgname)
    thumb = _add_thumb(str(imgname), ext="thumb"+str(size))

    if os.access(thumb, os.F_OK) and not settings.DEBUG:
        return thumb
    else:
        if os.access(fullpath, os.F_OK):
            img = Image.open(fullpath)

            # square crop
            s = min(img.size[0], img.size[1])
            d = (max(img.size[0], img.size[1]) - s)/2

            vo = ho = 0 # vertical and horisontal offset
            if img.size[0] > img.size[1]:
                ho = d
            else:
                vo = d
            img = img.crop((ho,vo,ho+s,vo+s))

            # do thumb
            img.thumbnail((size,size), Image.ANTIALIAS)
            img.save(_add_thumb(fullpath, ext="thumb"+str(size)), 'JPEG')
            return settings.MEDIA_URL + _add_thumb(str(imgname), ext="thumb"+str(size))
        else:
            return settings.MEDIA_URL + "broken.jpg"


@register.inclusion_tag("gallery/top_images.html", takes_context=True)
def latest_images(context, count=3):
    """Показывает последние добавленные изображения"""

    context['images'] = Photo.objects.all().order_by('-id')[:count]
    return context
