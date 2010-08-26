
from south.db import db
from django.db import models
from radio.library.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Label'
        db.create_table('radio_library_label', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
        ))
        db.send_create_signal('library', ['Label'])
        
        # Adding model 'Track'
        db.create_table('radio_library_track', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
            ('album', models.ForeignKey(orm.Album)),
        ))
        db.send_create_signal('library', ['Track'])
        
        # Adding model 'Genre'
        db.create_table('radio_library_genre', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
        ))
        db.send_create_signal('library', ['Genre'])
        
        # Adding model 'Artist'
        db.create_table('radio_library_artist', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
        ))
        db.send_create_signal('library', ['Artist'])
        
        # Adding model 'Album'
        db.create_table('radio_library_album', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
            ('artist', models.ForeignKey(orm.Artist)),
        ))
        db.send_create_signal('library', ['Album'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Label'
        db.delete_table('radio_library_label')
        
        # Deleting model 'Track'
        db.delete_table('radio_library_track')
        
        # Deleting model 'Genre'
        db.delete_table('radio_library_genre')
        
        # Deleting model 'Artist'
        db.delete_table('radio_library_artist')
        
        # Deleting model 'Album'
        db.delete_table('radio_library_album')
        
    
    
    models = {
        'library.label': {
            'Meta': {'ordering': "['name']", 'db_table': "'radio_library_label'"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.genre': {
            'Meta': {'db_table': "'radio_library_genre'"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.track': {
            'Meta': {'ordering': "['name']", 'db_table': "'radio_library_track'"},
            'album': ('models.ForeignKey', ["orm['library.Album']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.artist': {
            'Meta': {'ordering': "['name']", 'db_table': "'radio_library_artist'"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.album': {
            'Meta': {'ordering': "['name']", 'db_table': "'radio_library_album'"},
            'artist': ('models.ForeignKey', ["orm['library.Artist']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['library']
