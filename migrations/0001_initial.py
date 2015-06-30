# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Album'
        db.create_table('gallery_album', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=120)),
        ))
        db.send_create_signal('gallery', ['Album'])

        # Adding model 'Photo'
        db.create_table('gallery_photo', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('img', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('alt', self.gf('django.db.models.fields.CharField')(max_length=63)),
            ('group', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['gallery.Album'])),
            ('description', self.gf('django.db.models.fields.TextField')(blank=True)),
        ))
        db.send_create_signal('gallery', ['Photo'])


    def backwards(self, orm):
        # Deleting model 'Album'
        db.delete_table('gallery_album')

        # Deleting model 'Photo'
        db.delete_table('gallery_photo')


    models = {
        'gallery.album': {
            'Meta': {'object_name': 'Album'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '120'})
        },
        'gallery.photo': {
            'Meta': {'object_name': 'Photo'},
            'alt': ('django.db.models.fields.CharField', [], {'max_length': '63'}),
            'description': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['gallery.Album']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'img': ('django.db.models.fields.files.FileField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['gallery']