# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Books'
        db.create_table('hyperdrive_books', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('b_title', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('author', self.gf('django.db.models.fields.CharField')(max_length=64, null=True, blank=True)),
            ('isbn', self.gf('django.db.models.fields.IntegerField')(max_length=5, null=True, blank=True)),
            ('number_of_pages', self.gf('django.db.models.fields.IntegerField')(max_length=5, null=True, blank=True)),
        ))
        db.send_create_signal('hyperdrive', ['Books'])


    def backwards(self, orm):
        # Deleting model 'Books'
        db.delete_table('hyperdrive_books')


    models = {
        'hyperdrive.books': {
            'Meta': {'object_name': 'Books'},
            'author': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'b_title': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'isbn': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'number_of_pages': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        'hyperdrive.rooms': {
            'Meta': {'object_name': 'Rooms'},
            'department': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spots': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        },
        'hyperdrive.users': {
            'Meta': {'object_name': 'Users'},
            'date_joined': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'null': 'True', 'blank': 'True'}),
            'paycheck': ('django.db.models.fields.IntegerField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['hyperdrive']