
from south.db import db
from django.db import models, connection
from radio.library.models import *

class Migration:
    rename_tables = [
        'artist',
        'album',
        'track',
        'label',
        'genre',
    ]
    rename_template = ('radio_library_%s', 'library_%s')

    def forwards(self, orm):
        "Write your forwards migration here"
        [db.rename_table(*[i%model for i in self.rename_template]) for model in self.rename_tables] 
 
    def backwards(self, orm):
        "Write your backwards migration here"
        rename_template = self.rename_template
        rename_template.reverse()
        [db.rename_table(*[i%model for i in rename_template]) for model in self.rename_tables] 
    
    models = {
        'library.label': {
            'Meta': {'ordering': "['name']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.genre': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.track': {
            'Meta': {'ordering': "['name']"},
            'album': ('models.ForeignKey', ["orm['library.Album']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.artist': {
            'Meta': {'ordering': "['name']"},
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        },
        'library.album': {
            'Meta': {'ordering': "['name']"},
            'artist': ('models.ForeignKey', ["orm['library.Artist']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'})
        }
    }
    
    complete_apps = ['library']
