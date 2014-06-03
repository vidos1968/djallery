# -*- coding: utf-8 -*-

from django import template
from django.conf import settings
from PIL import Image
from re import sub, match
from ..models import Album, Photo
import os

# Регистрируем новую библиотеку тегов
register = template.Library()

@register.inclusion_tag("gallery/top_images.html", takes_context=True)
def latest_images(context, count=3):
    """Показывает последние добавленные изображения"""

    context['images'] = Photo.objects.all().order_by('-id')[:count]
    return context
