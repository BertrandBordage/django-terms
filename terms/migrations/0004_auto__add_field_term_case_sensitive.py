# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Term.case_sensitive'
        db.add_column('terms_term', 'case_sensitive',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Term.case_sensitive'
        db.delete_column('terms_term', 'case_sensitive')


    models = {
        'terms.term': {
            'Meta': {'ordering': "(u'name',)", 'object_name': 'Term'},
            'case_sensitive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'definition': ('django.db.models.fields.TextField', [], {'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '200', 'blank': 'True'})
        }
    }

    complete_apps = ['terms']