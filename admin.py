# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Photo, Album

class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image_thumb', 'description', 'alt', 'group', )

    list_filter = ('group',)
    ordering = ['group']

class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
