
from south.db import db
from django.db import models
from radio.events.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Event'
        db.create_table('radio_events_event', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(unique=True, max_length=255)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('weight', models.IntegerField(default=0, null=True, blank=True)),
            ('location', models.ForeignKey(orm.Location, null=True, blank=True)),
            ('blurb', models.TextField()),
            ('content', models.TextField()),
            ('date', models.DateField()),
            ('time_start', models.TimeField()),
            ('time_end', models.TimeField(null=True, blank=True)),
        ))
        db.send_create_signal('events', ['Event'])
        
        # Adding model 'Location'
        db.create_table('radio_events_location', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(unique=True, max_length=255)),
            ('slug', models.SlugField(unique=True, max_length=255)),
            ('address_line_1', models.CharField(max_length=255, null=True, blank=True)),
            ('address_line_2', models.CharField(max_length=255, null=True, blank=True)),
            ('state', USStateField(null=True, blank=True)),
            ('zip', models.CharField(max_length=255, null=True, blank=True)),
            ('phone', models.CharField(max_length=255, null=True, blank=True)),
            ('blurb', models.TextField()),
        ))
        db.send_create_signal('events', ['Location'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Event'
        db.delete_table('radio_events_event')
        
        # Deleting model 'Location'
        db.delete_table('radio_events_location')
        
    
    
    models = {
        'events.event': {
            'Meta': {'db_table': "'radio_events_event'"},
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
            'Meta': {'db_table': "'radio_events_location'"},
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
