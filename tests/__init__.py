"""
This file demonstrates writing tests using the unittest module. These will pass
when you run "manage.py test".

Replace this with more appropriate tests for your application.
"""

from django.test import TestCase
from django.test.client import Client
from django.core.urlresolvers import reverse
from ..models import *
from django.core.files.uploadedfile import SimpleUploadedFile

class AlbumTest(TestCase):
    def setUp(self):
        from os.path import abspath, dirname, join

        self.client = Client()

        for i in range(5):
            a = Album(name = u"Test album #%d" % i)
            a.save()

            for i in range(3):
                pwd = abspath(dirname(__file__))
                img = open(join(pwd, "fixtures/test_image.jpg"))
                p = Photo(
                    img = SimpleUploadedFile(img.name, img.read()),
                    alt = u"alternative text",
                    description = u"description text",
                    group = a
                )
                p.save()


        self.photos = Photo.objects.all()
        self.albums = Album.objects.all()

    def test_album_list_page(self):
        response = self.client.get(reverse("all_albums"))
        self.assertEqual(response.status_code, 200)

    def test_album_url(self):
        for a in self.albums:
            resp = self.client.get(a.get_absolute_url())
            self.assertEqual(resp.status_code, 200)

    def test_album_cover(self):
        for a in self.albums:
            print a.cover()
