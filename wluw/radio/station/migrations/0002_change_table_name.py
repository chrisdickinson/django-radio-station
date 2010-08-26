
from south.db import db
from django.db import models, connection
from radio.station.models import *

class Migration:
    rename_tables = [
        'schedule',
        'dj',
        'spot',
        'show',
    ]
    rename_template = ('radio_station_%s', 'station_%s')

    def forwards(self, orm):
        "Write your forwards migration here"
        [db.rename_table(*[i%model for i in self.rename_template]) for model in self.rename_tables] 
 
    def backwards(self, orm):
        "Write your backwards migration here"
        rename_template = self.rename_template
        rename_template.reverse()
        [db.rename_table(*[i%model for i in rename_template]) for model in self.rename_tables] 
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'station.schedule': {
            'end_date': ('models.DateField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('models.DateField', [], {})
        },
        'station.dj': {
            'description': ('models.TextField', [], {}),
            'display_name': ('models.CharField', [], {'max_length': '255'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True'}),
            'summary': ('models.TextField', [], {}),
            'user': ('models.OneToOneField', ["orm['auth.User']"], {})
        },
        'station.spot': {
            'day_of_week': ('models.IntegerField', [], {}),
            'dj': ('models.ForeignKey', ["orm['station.DJ']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'offset': ('models.PositiveIntegerField', [], {}),
            'repeat_every': ('models.IntegerField', [], {}),
            'schedule': ('models.ForeignKey', ["orm['station.Schedule']"], {}),
            'show': ('models.ForeignKey', ["orm['station.Show']"], {})
        },
        'station.show': {
            'active': ('models.BooleanField', [], {}),
            'blurb': ('models.CharField', [], {'max_length': '255'}),
            'date_added': ('models.DateTimeField', [], {}),
            'description': ('models.TextField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ImageField', [], {}),
            'name': ('models.CharField', [], {'max_length': '255'}),
            'schedule': ('models.ManyToManyField', ["orm['station.Schedule']"], {'through': 'Spot'}),
            'slug': ('models.SlugField', [], {'unique': 'True'}),
            'special_program': ('models.BooleanField', [], {})
        }
    }
    
    complete_apps = ['station']
