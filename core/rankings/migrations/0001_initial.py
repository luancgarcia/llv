# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Intervalo'
        db.create_table(u'rankings_intervalo', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_criacao', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('data_atualizacao', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('inicio', self.gf('django.db.models.fields.DateField')()),
            ('fim', self.gf('django.db.models.fields.DateField')()),
        ))
        db.send_create_signal(u'rankings', ['Intervalo'])


    def backwards(self, orm):
        # Deleting model 'Intervalo'
        db.delete_table(u'rankings_intervalo')


    models = {
        u'rankings.intervalo': {
            'Meta': {'object_name': 'Intervalo'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fim': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {})
        }
    }

    complete_apps = ['rankings']