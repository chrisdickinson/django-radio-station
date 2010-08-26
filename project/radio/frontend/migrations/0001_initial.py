
from south.db import db
from django.db import models
from radio.frontend.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Ad'
        db.create_table('frontend_ad', (
            ('id', models.AutoField(primary_key=True)),
            ('name', models.CharField(max_length=255)),
            ('image', models.ImageField()),
            ('link', models.URLField()),
            ('start_date', models.DateField()),
            ('end_date', models.DateField()),
        ))
        db.send_create_signal('frontend', ['Ad'])
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Ad'
        db.delete_table('frontend_ad')
        
    
    
    models = {
        'frontend.ad': {
            'Meta': {'db_table': "'frontend_ad'"},
            'end_date': ('models.DateField', [], {}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'image': ('models.ImageField', [], {}),
            'link': ('models.URLField', [], {}),
            'name': ('models.CharField', [], {'max_length': '255'}),
            'start_date': ('models.DateField', [], {})
        }
    }
    
    complete_apps = ['frontend']
