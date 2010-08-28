# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Changing field 'Track.album'
        db.alter_column('library_track', 'album_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Album']))

        # Adding field 'Album.image_large'
        db.add_column('library_album', 'image_large', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Album.image_medium'
        db.add_column('library_album', 'image_medium', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Album.image_small'
        db.add_column('library_album', 'image_small', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True), keep_default=False)

        # Adding field 'Album.mbid'
        db.add_column('library_album', 'mbid', self.gf('django.db.models.fields.CharField')(max_length=36, null=True, blank=True), keep_default=False)

        # Adding field 'Album.status'
        db.add_column('library_album', 'status', self.gf('django.db.models.fields.IntegerField')(default=0), keep_default=False)

        # Changing field 'Album.artist'
        db.alter_column('library_album', 'artist_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['library.Artist']))


    def backwards(self, orm):
        
        # Changing field 'Track.album'
        db.alter_column('library_track', 'album_id', self.gf('models.ForeignKey')(orm['library.Album']))

        # Deleting field 'Album.image_large'
        db.delete_column('library_album', 'image_large')

        # Deleting field 'Album.image_medium'
        db.delete_column('library_album', 'image_medium')

        # Deleting field 'Album.image_small'
        db.delete_column('library_album', 'image_small')

        # Deleting field 'Album.mbid'
        db.delete_column('library_album', 'mbid')

        # Deleting field 'Album.status'
        db.delete_column('library_album', 'status')

        # Changing field 'Album.artist'
        db.alter_column('library_album', 'artist_id', self.gf('models.ForeignKey')(orm['library.Artist']))


    models = {
        'library.album': {
            'Meta': {'ordering': "['name']", 'object_name': 'Album'},
            'artist': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.Artist']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'image_large': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_medium': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'image_small': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'mbid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        'library.artist': {
            'Meta': {'ordering': "['name']", 'object_name': 'Artist'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'library.genre': {
            'Meta': {'object_name': 'Genre'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'library.label': {
            'Meta': {'ordering': "['name']", 'object_name': 'Label'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        },
        'library.track': {
            'Meta': {'ordering': "['name']", 'object_name': 'Track'},
            'album': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['library.Album']"}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['library']
