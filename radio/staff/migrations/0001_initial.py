
from south.db import db
from django.db import models
from radio.staff.models import *

class Migration:
    
    def forwards(self, orm):
        
        # Adding model 'Role'
        db.create_table('staff_role', (
            ('id', models.AutoField(primary_key=True)),
            ('title', models.CharField(max_length=255)),
            ('description', models.CharField(max_length=255)),
            ('email', models.EmailField(null=True, blank=True)),
            ('phone', models.CharField(max_length=40, null=True, blank=True)),
            ('weight', models.PositiveIntegerField()),
        ))
        db.send_create_signal('staff', ['Role'])
        
        # Adding model 'StaffRoleRelation'
        db.create_table('staff_staffrolerelation', (
            ('id', models.AutoField(primary_key=True)),
            ('user', models.ForeignKey(orm['auth.User'])),
            ('role', models.ForeignKey(orm.Role)),
        ))
        db.send_create_signal('staff', ['StaffRoleRelation'])
        
        # Adding ManyToManyField 'StaffRoleRelation.schedule'
        db.create_table('staff_staffrolerelation_schedule', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('staffrolerelation', models.ForeignKey(orm.StaffRoleRelation, null=False)),
            ('schedule', models.ForeignKey(orm['station.Schedule'], null=False))
        ))
        
    
    
    def backwards(self, orm):
        
        # Deleting model 'Role'
        db.delete_table('staff_role')
        
        # Deleting model 'StaffRoleRelation'
        db.delete_table('staff_staffrolerelation')
        
        # Dropping ManyToManyField 'StaffRoleRelation.schedule'
        db.delete_table('staff_staffrolerelation_schedule')
        
    
    
    models = {
        'auth.user': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'station.schedule': {
            '_stub': True,
            'id': ('models.AutoField', [], {'primary_key': 'True'})
        },
        'staff.role': {
            'Meta': {'ordering': "['weight']"},
            'description': ('models.CharField', [], {'max_length': '255'}),
            'email': ('models.EmailField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'phone': ('models.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'title': ('models.CharField', [], {'max_length': '255'}),
            'weight': ('models.PositiveIntegerField', [], {})
        },
        'staff.staffrolerelation': {
            'id': ('models.AutoField', [], {'primary_key': 'True'}),
            'role': ('models.ForeignKey', ["orm['staff.Role']"], {}),
            'schedule': ('models.ManyToManyField', ["orm['station.Schedule']"], {}),
            'user': ('models.ForeignKey', ["orm['auth.User']"], {})
        }
    }
    
    complete_apps = ['staff']
