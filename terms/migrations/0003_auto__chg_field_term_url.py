# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'Term.url'
        db.alter_column('terms_term', 'url', self.gf('django.db.models.fields.CharField')(default='', max_length=200))

    def backwards(self, orm):

        # Changing field 'Term.url'
        db.alter_column('terms_term', 'url', self.gf('django.db.models.fields.CharField')(max_length=200, null=True))

    models = {
        'terms.term': {
            'Meta': {'ordering': "('name',)", 'object_name': 'Term'},
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['terms']