
from south.db import db
from django.db import models, connection
from radio.events.models import *

class Migration:
    rename_tables = [
        'event',
        'location',
    ]
    rename_template = ('radio_events_%s', 'events_%s')


    def forwards(self, orm):
        "Write your forwards migration here"
        [db.rename_table(*[i%model for i in self.rename_template]) for model in self.rename_tables]
 
    def backwards(self, orm):
        "Write your backwards migration here"
        rename_template = self.rename_template
        rename_template.reverse()
        [db.rename_table(*[i%model for i in rename_template]) for model in self.rename_tables] 
    
    
    models = {
        'events.event': {
            'blurb': ('models.TextField', [], {}),
            'content': ('models.TextField', [], {}),
            'date': ('models.DateField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'location': ('models.ForeignKey', ["orm['events.Location']"], {'null': 'True', 'blank': 'True'}),
            'name': ('models.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'time_end': ('models.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_start': ('models.TimeField', [], {}),
            'weight': ('models.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'events.location': {
            'address_line_1': ('models.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'address_line_2': ('models.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'blurb': ('models.TextField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'name': ('models.CharField', [], {'unique': 'True', 'max_length': '255'}),
            'phone': ('models.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'state': ('USStateField', [], {'null': 'True', 'blank': 'True'}),
            'zip': ('models.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'})
        }
    }
    
    complete_apps = ['events']
