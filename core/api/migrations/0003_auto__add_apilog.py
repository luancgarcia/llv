# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'ApiLog'
        db.create_table(u'api_apilog', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('sessao', self.gf('django.db.models.fields.related.ForeignKey')(related_name='logs', to=orm['api.ApiSession'])),
        ))
        db.send_create_signal(u'api', ['ApiLog'])


    def backwards(self, orm):
        # Deleting model 'ApiLog'
        db.delete_table(u'api_apilog')


    models = {
        u'api.apilog': {
            'Meta': {'object_name': 'ApiLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sessao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'to': u"orm['api.ApiSession']"})
        },
        u'api.apisession': {
            'Meta': {'object_name': 'ApiSession'},
            'fim': ('django.db.models.fields.DateTimeField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessoes'", 'to': u"orm['api.ApiUser']"})
        },
        u'api.apiuser': {
            'Meta': {'object_name': 'ApiUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'shopping': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'tokens'", 'to': u"orm['lojas.Shopping']"}),
            'token': ('django.db.models.fields.CharField', [], {'max_length': '64'})
        },
        u'lojas.shopping': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Shopping'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_multiplan': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'})
        }
    }

    complete_apps = ['api']