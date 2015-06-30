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
    """ Фотоальбом """
    name = models.CharField( _(u"Name"), max_length = 120 )

    def __unicode__(self):
        return u"%s" % (self.name)

    def get_absolute_url(self):
        return u'/gallery/album/%d/' % self.id

    def cover(self, size=(300,300), crop=True):
        photo = Photo.objects.filter(group=self, album_cover=True) or\
           Photo.objects.filter(group=self)

        return photo[0].img

    class Meta:
        verbose_name = u"Фото альбом"
        verbose_name_plural = u"Фото альбомы"


class Photo(models.Model):
    img = models.FileField(upload_to = up_pth, verbose_name=_(u"File"))
    alt = models.CharField(_(u"Short description"), max_length=63)
    group = models.ForeignKey('Album', verbose_name=_(u"Album"))
    description = models.TextField(_(u"Description"), blank=True)
    album_cover = models.BooleanField(default=False, blank=True)

    def get_anchor(self):
        return "photo_%d" % self.pk

    def get_absolute_url(self):
        return "%s#%s" % (self.group.get_absolute_url(), self.get_anchor())

    def image_thumb(self):
        ''' for admin site '''
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
