
from south.db import db
from django.db import models
from radio.station.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Schedule'
        db.create_table('radio_station_schedule', (
            ('id', models.AutoField(primary_key=True)),
            ('start_date', models.DateField()),
            ('end_date', models.DateField()),
        ))
        db.send_create_signal('station', ['Schedule'])
        
        # Adding model 'Show'
        db.create_table('radio_station_show', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
            ('slug', models.SlugField(unique=True)),
            ('special_program', models.BooleanField()),
            ('active', models.BooleanField()),
            ('date_added', models.DateTimeField()),
            ('image', models.ImageField()),
            ('blurb', models.CharField(max_length=255)),
            ('description', models.TextField(null=True, blank=True)),
        ))
        db.send_create_signal('station', ['Show'])
        
        # Adding model 'Spot'
        db.create_table('radio_station_spot', (
            ('id', models.AutoField(primary_key=True)),
            ('day_of_week', models.IntegerField()),
            ('repeat_every', models.IntegerField()),
            ('offset', models.PositiveIntegerField()),
            ('dj', models.ForeignKey(orm.DJ)),
            ('show', models.ForeignKey(orm.Show)),
            ('schedule', models.ForeignKey(orm.Schedule)),
        ))
        db.send_create_signal('station', ['Spot'])
        
        # Adding model 'DJ'
        db.create_table('radio_station_dj', (
            ('id', models.AutoField(primary_key=True)),
            ('user', models.OneToOneField(orm['auth.User'])),
            ('slug', models.SlugField(unique=True)),
            ('display_name', models.CharField(max_length=255)),
            ('summary', models.TextField()),
            ('description', models.TextField()),
        ))
        db.send_create_signal('station', ['DJ'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Schedule'
        db.delete_table('radio_station_schedule')
        
        # Deleting model 'Show'
        db.delete_table('radio_station_show')
        
        # Deleting model 'Spot'
        db.delete_table('radio_station_spot')
        
        # Deleting model 'DJ'
        db.delete_table('radio_station_dj')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'station.schedule': {
            'Meta': {'db_table': "'radio_station_schedule'"},
            'end_date': ('models.DateField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'start_date': ('models.DateField', [], {})
        },
        'station.dj': {
            'Meta': {'db_table': "'radio_station_dj'"},
            'description': ('models.TextField', [], {}),
            'display_name': ('models.CharField', [], {'max_length': '255'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'slug': ('models.SlugField', [], {'unique': 'True'}),
            'summary': ('models.TextField', [], {}),
            'user': ('models.OneToOneField', ["orm['auth.User']"], {})
        },
        'station.spot': {
            'Meta': {'db_table': "'radio_station_spot'"},
            'day_of_week': ('models.IntegerField', [], {}),
            'dj': ('models.ForeignKey', ["orm['station.DJ']"], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'offset': ('models.PositiveIntegerField', [], {}),
            'repeat_every': ('models.IntegerField', [], {}),
            'schedule': ('models.ForeignKey', ["orm['station.Schedule']"], {}),
            'show': ('models.ForeignKey', ["orm['station.Show']"], {})
        },
        'station.show': {
            'Meta': {'db_table': "'radio_station_show'"},
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
