
from south.db import db
from django.db import models
from radio.library.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding field 'Album.image_url'
        db.add_column('library_album', 'image_url', models.CharField(max_length=255, null=True, blank=True))
        
    
    
    def backwards(self, orm):
        
        # Deleting field 'Album.image_url'
        db.delete_column('library_album', 'image_url')
        
    
    
    models = {
        'library.label': {
            'Meta': {'ordering': "['name']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.album': {
            'Meta': {'ordering': "['name']"},
            'artist': ('models.ForeignKey', ["orm['library.Artist']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image_url': ('models.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.genre': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.artist': {
            'Meta': {'ordering': "['name']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.track': {
            'Meta': {'ordering': "['name']"},
            'album': ('models.ForeignKey', ["orm['library.Album']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['library']
