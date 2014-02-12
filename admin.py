#-*-coding:utf8-*-

from django.contrib import admin
from models import ImageItem, GalleryGroup

class ImageItemAdmin(admin.ModelAdmin):
    # Вариант с предопросмотром изображений
    # -- необходимо решить, как отображать уменьшенную копию изображения
    # -- иначе страница долго грузится
    #
    list_display = ('image_img', 'alt', 'description', 'group', )

    #list_display = ('alt', 'description', 'group', )
    list_filter = ('group',)
    ordering = ['group']

class GalleryGroupAdmin(admin.ModelAdmin):
    list_display = ('name',)

admin.site.register(ImageItem, ImageItemAdmin)
admin.site.register(GalleryGroup, GalleryGroupAdmin)
