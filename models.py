# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from re import sub

# Global path
GALLERY_DIR = 'gallery'

def up_pth(instance, filename):
    """Upload path with needed filenames"""
    from os.path import join

    i = instance.img.name
    name = sub("\ ", "_", i)
    name = sub(r"[Jj][Pp](E|e|)[Gg]$", "jpg", name)
    return join(GALLERY_DIR, name )

class Album( models.Model ):
    """ Что-то вроде фотоальбома. Группа изображений """
    name = models.CharField( _(u"Name"), max_length = 120 )

    def __unicode__(self):
        return u"%s" % (self.name)

    def cover(self, size=(300,300)):
        """
        Creates or find album cover
        @return cover filename
        """

        from PIL import Image
        from os.path import join, isfile

        tsize = size[0]/1
        tsize = (tsize,tsize)

        images = Photo.objects.filter(group=self)
        cover_filename = "%03d-%s.cover_%02d.jpg" % (self.id,
            self.name.encode('utf-8').replace(' ', '_'),
            len(images))
        cover_filename = join(GALLERY_DIR, cover_filename)
        fullpath = join(settings.MEDIA_ROOT, cover_filename)

        cover = Image.new("RGBA", size, 0)

        if isfile(cover_filename) and not settings.DEBUG:
            return cover_filename

        offset = 0

        if len(images) > 3:
            images = images[0:3]

        for i in images:
            # используя i.img.name можно наткнуться на UnicodeEncodeError
            # с русскими именами файлов.
            # преобразование объекта в строку даёт нужный результат
            if isfile(join(settings.MEDIA_ROOT, str(i.img))):
                i = Image.open(settings.MEDIA_ROOT + str(i.img))
            else:
                break

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

        cover.save(fullpath, "JPEG", quality=80, optimize=True, progressive=True)
        return cover_filename

    class Meta:
        verbose_name = u"Фото альбом"
        verbose_name_plural = u"Фото альбомы"

class Photo( models.Model ):
    """ Photo ;-) """
    img = models.FileField( upload_to = up_pth, verbose_name=_(u"File") )
    alt = models.CharField( _(u"Short description"), max_length = 63 )
    group = models.ForeignKey( 'Album', verbose_name=_(u"Album") )
    description = models.TextField(_(u"Description"))

    def image_thumb(self):
        from easy_thumbnails.files import get_thumbnailer

        size = (150, 150)
        options = {'size': size, 'crop': True}
        thumb_url = get_thumbnailer(self.img).get_thumbnail(options).url

        if self.img:
            return '<img src="%s" width="%dpx" />' %(thumb_url, size[0])
        else:
            return '(none)'

    image_thumb.short_description = _(u"Thumb")
    image_thumb.allow_tags = True

    def __unicode__( self ):
        return u"%s -- %s" % (self.alt, self.group)

    class Meta:
        verbose_name = _(u"Photo")
        verbose_name_plural = _(u"Photos")

