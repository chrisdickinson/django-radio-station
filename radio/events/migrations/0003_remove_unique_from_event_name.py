
from south.db import db
from django.db import models
from radio.events.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Changing field 'Event.name'
        db.alter_column('events_event', 'name', models.CharField(max_length=255))
        
    
    
    def backwards(self, orm):
        
        # Changing field 'Event.name'
        db.alter_column('events_event', 'name', models.CharField(max_length=255, unique=True))
        
    
    
    models = {
        'events.event': {
            'Meta': {'ordering': "['-date','-time_start']"},
            'blurb': ('models.TextField', [], {}),
            'content': ('models.TextField', [], {}),
            'date': ('models.DateField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'location': ('models.ForeignKey', ["orm['events.Location']"], {'null': 'True', 'blank': 'True'}),
            'name': ('models.CharField', [], {'max_length': '255'}),
            'slug': ('models.SlugField', [], {'unique': 'True', 'max_length': '255'}),
            'time_end': ('models.TimeField', [], {'null': 'True', 'blank': 'True'}),
            'time_start': ('models.TimeField', [], {}),
            'weight': ('models.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'})
        },
        'events.location': {
            'Meta': {'ordering': "['name']"},
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
