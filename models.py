# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _
from re import sub

def up_pth(instance, filename):
    """Upload path with needed filenames"""
    i = instance.img.name
    name = sub("\ ", "_", i)
    name = sub(r"[Jj][Pp](E|e|)[Gg]$", "jpg", name)
    return u"gallery/%s" % ( name ) 

class Album( models.Model ):
    """ Что-то вроде фотоальбома. Группа изображений """
    name = models.CharField( _(u"Name"), max_length = 120 )

    def __unicode__(self):
        return u"%s" % (self.name)

    class Meta:
        verbose_name = u"Фото альбом"
        verbose_name_plural = u"Фото альбомы"

class Photo( models.Model ):
    """ Photo ;-) """
    img = models.FileField( upload_to = up_pth )
    alt = models.CharField( _(u"Short description"), max_length = 63 )
    group = models.ForeignKey( 'Album', verbose_name=_(u"Album") )
    description = models.TextField(_(u"Description"))

    def image_img(self):
        from templatetags import gallery_extras
        if self.img:
            return u'<img src="%s" width="100" />' %self.img.url
        else:
            return '(none)'

    image_img.short_description = _(u"Thumb")
    image_img.allow_tags = True

    def __unicode__( self ):
        return u"%s -- %s" % (self.alt, self.group)

    class Meta:
        verbose_name = _(u"Photo")
        verbose_name_plural = _(u"Photos")

