
from south.db import db
from django.db import models, connection
from radio.logs.models import *

class Migration:
    rename_tables = [
        'entry',
    ]
    rename_template = ('radio_logs_%s', 'logs_%s')

    def forwards(self, orm):
        "Write your forwards migration here"
        [db.rename_table(*[i%model for i in self.rename_template]) for model in self.rename_tables] 
 
    def backwards(self, orm):
        "Write your backwards migration here"
        rename_template = self.rename_template
        rename_template.reverse()
        [db.rename_table(*[i%model for i in rename_template]) for model in self.rename_tables] 
    
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
