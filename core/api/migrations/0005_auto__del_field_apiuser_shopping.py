# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'ApiUser.shopping'
        db.delete_column(u'api_apiuser', 'shopping_id')

        # Adding M2M table for field shopping on 'ApiUser'
        m2m_table_name = db.shorten_name(u'api_apiuser_shopping')
        db.create_table(m2m_table_name, (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('apiuser', models.ForeignKey(orm[u'api.apiuser'], null=False)),
            ('shopping', models.ForeignKey(orm[u'lojas.shopping'], null=False))
        ))
        db.create_unique(m2m_table_name, ['apiuser_id', 'shopping_id'])


    def backwards(self, orm):
        # Adding field 'ApiUser.shopping'
        db.add_column(u'api_apiuser', 'shopping',
                      self.gf('django.db.models.fields.related.ForeignKey')(default='', related_name='tokens', to=orm['lojas.Shopping']),
                      keep_default=False)

        # Removing M2M table for field shopping on 'ApiUser'
        db.delete_table(db.shorten_name(u'api_apiuser_shopping'))


    models = {
        u'api.apilog': {
            'Meta': {'object_name': 'ApiLog'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'sessao': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'logs'", 'to': u"orm['api.ApiSession']"})
        },
        u'api.apisession': {
            'Meta': {'object_name': 'ApiSession'},
            'fim': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'sessoes'", 'to': u"orm['api.ApiUser']"})
        },
        u'api.apiuser': {
            'Meta': {'object_name': 'ApiUser'},
            'email': ('django.db.models.fields.EmailField', [], {'unique': 'True', 'max_length': '75'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'shopping': ('django.db.models.fields.related.ManyToManyField', [], {'related_name': "'tokens'", 'symmetrical': 'False', 'to': u"orm['lojas.Shopping']"}),
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