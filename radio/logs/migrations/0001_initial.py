
from south.db import db
from django.db import models
from radio.logs.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Entry'
        db.create_table('radio_logs_entry', (
            ('id', models.AutoField(primary_key=True)),
            ('artist', d51fields.ForeignKey(orm['library.Artist'], instantiate_fn=instant_artist)),
            ('album', d51fields.ForeignKey(orm['library.Album'], js_methods=['match_artist_and_startswith'], instantiate_fn=instant_album)),
            ('track', d51fields.ForeignKey(orm['library.Track'], js_methods=['match_album_and_startswith'], instantiate_fn=instant_track)),
            ('genre', models.ForeignKey(orm['library.Genre'])),
            ('submitted', models.DateTimeField(auto_now_add=True)),
            ('is_rotation', models.BooleanField()),
            ('dj', models.ForeignKey(orm['station.DJ'])),
            ('show', models.ForeignKey(orm['station.Show'], null=True, blank=True)),
        ))
        db.send_create_signal('logs', ['Entry'])
        
        # Adding model 'Request'
        db.create_table('radio_logs_request', (
            ('id', models.AutoField(primary_key=True)),
            ('what', models.CharField(max_length=255)),
            ('when', models.DateTimeField(auto_now_add=True)),
            ('who', models.CharField(max_length=255, null=True, blank=True)),
            ('ip', models.IPAddressField()),
        ))
        db.send_create_signal('logs', ['Request'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Entry'
        db.delete_table('radio_logs_entry')
        
        # Deleting model 'Request'
        db.delete_table('radio_logs_request')
        
    
    
    models = {
        'library.artist': {
            'Meta': {'ordering': "['name']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'library.track': {
            'Meta': {'ordering': "['name']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'logs.entry': {
            'album': ('d51fields.ForeignKey', ["orm['library.Album']"], {'js_methods': "['match_artist_and_startswith']", 'instantiate_fn': 'instant_album'}),
            'artist': ('d51fields.ForeignKey', ["orm['library.Artist']"], {'instantiate_fn': 'instant_artist'}),
            'dj': ('models.ForeignKey', ["orm['station.DJ']"], {}),
            'genre': ('models.ForeignKey', ["orm['library.Genre']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'is_rotation': ('models.BooleanField', [], {}),
            'show': ('models.ForeignKey', ["orm['station.Show']"], {'null': 'True', 'blank': 'True'}),
            'submitted': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'track': ('d51fields.ForeignKey', ["orm['library.Track']"], {'js_methods': "['match_album_and_startswith']", 'instantiate_fn': 'instant_track'})
        },
        'library.genre': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'logs.request': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'ip': ('models.IPAddressField', [], {}),
            'what': ('models.CharField', [], {'max_length': '255'}),
            'when': ('models.DateTimeField', [], {'auto_now_add': 'True'}),
            'who': ('models.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        },
        'station.show': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'station.dj': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'library.album': {
            'Meta': {'ordering': "['name']"},
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        }
    }
    
    complete_apps = ['logs']
