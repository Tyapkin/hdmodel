# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Rooms'
        db.create_table('hyperdrive_rooms', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('department', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True, null=True)),
            ('spots', self.gf('django.db.models.fields.IntegerField')(max_length=5, blank=True, null=True)),
        ))
        db.send_create_signal('hyperdrive', ['Rooms'])

        # Adding model 'Users'
        db.create_table('hyperdrive_users', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=64, blank=True, null=True)),
            ('paycheck', self.gf('django.db.models.fields.IntegerField')(max_length=5, blank=True, null=True)),
            ('date_joined', self.gf('django.db.models.fields.DateField')(blank=True, null=True)),
        ))
        db.send_create_signal('hyperdrive', ['Users'])


    def backwards(self, orm):
        # Deleting model 'Rooms'
        db.delete_table('hyperdrive_rooms')

        # Deleting model 'Users'
        db.delete_table('hyperdrive_users')


    models = {
        'hyperdrive.rooms': {
            'Meta': {'object_name': 'Rooms'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'blank': 'True', 'null': 'True'})
        },
        'hyperdrive.users': {
            'Meta': {'object_name': 'Users'},
            'date_joined': ('django.db.models.fields.DateField', [], {'blank': 'True', 'null': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'blank': 'True', 'null': 'True'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'blank': 'True', 'null': 'True'})
        }
    }

    complete_apps = ['hyperdrive']