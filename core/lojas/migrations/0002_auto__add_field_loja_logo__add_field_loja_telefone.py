# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Loja.logo'
        db.add_column(u'lojas_loja', 'logo',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True),
                      keep_default=False)

        # Adding field 'Loja.telefone'
        db.add_column(u'lojas_loja', 'telefone',
                      self.gf('django.db.models.fields.CharField')(max_length=100, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Loja.logo'
        db.delete_column(u'lojas_loja', 'logo')

        # Deleting field 'Loja.telefone'
        db.delete_column(u'lojas_loja', 'telefone')


    models = {
        u'lojas.loja': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Loja', '_ormbases': [u'utils.EditorialModel']},
            u'editorialmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['utils.EditorialModel']", 'unique': 'True', 'primary_key': 'True'}),
            'logo': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
        },
        u'utils.editorialmodel': {
            'Meta': {'object_name': 'EditorialModel'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['lojas']