# -*- coding: utf-8 -*-

from django.contrib import admin
from models import Photo, Album


class PhotoInline(admin.TabularInline):
    model = Photo
    extra = 0
    readonly_fields = ('image_thumb',)
    fields = [ 'image_thumb', 'img', 'alt', 'album_cover', ]


class PhotoAdmin(admin.ModelAdmin):
    list_display = ('image_thumb', 'description', 'alt', 'group', )

    list_filter = ('group',)
    ordering = ['group']


class AlbumAdmin(admin.ModelAdmin):
    list_display = ('name',)
    inlines = (PhotoInline, )


admin.site.register(Photo, PhotoAdmin)
admin.site.register(Album, AlbumAdmin)
