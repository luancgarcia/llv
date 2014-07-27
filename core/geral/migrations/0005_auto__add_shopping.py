# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shopping'
        db.create_table(u'geral_shopping', (
            (u'editorialmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['utils.EditorialModel'], unique=True, primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=150)),
            ('id_multiplan', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'geral', ['Shopping'])


    def backwards(self, orm):
        # Deleting model 'Shopping'
        db.delete_table(u'geral_shopping')


    models = {
        u'geral.categoria': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Categoria', '_ormbases': [u'utils.EditorialModel']},
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'editorialmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['utils.EditorialModel']", 'unique': 'True', 'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'geral.imagemoferta': {
            'Meta': {'object_name': 'ImagemOferta', '_ormbases': [u'utils.EditorialModel']},
            u'editorialmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['utils.EditorialModel']", 'unique': 'True', 'primary_key': 'True'}),
            'imagem': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'oferta': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imagens'", 'to': u"orm['geral.Oferta']"}),
            'principal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'vertical': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'geral.log': {
            'Meta': {'ordering': "['data_criacao']", 'object_name': 'Log'},
            'acao': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'oferta': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'logs'", 'null': 'True', 'to': u"orm['geral.Oferta']"})
        },
        u'geral.oferta': {
            'Meta': {'ordering': "['nome']", 'unique_together': "(('loja', 'slug'),)", 'object_name': 'Oferta', '_ormbases': [u'utils.EditorialModel']},
            'desconto': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descricao': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'editorialmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['utils.EditorialModel']", 'unique': 'True', 'primary_key': 'True'}),
            'evento': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'loja': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ofertas'", 'null': 'True', 'to': u"orm['lojas.Loja']"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'preco_final': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'preco_inicial': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'texto_link': ('django.db.models.fields.CharField', [], {'max_length': "'140'", 'null': 'True'}),
            'texto_promocional': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'geral.shopping': {
            'Meta': {'object_name': 'Shopping', '_ormbases': [u'utils.EditorialModel']},
            u'editorialmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['utils.EditorialModel']", 'unique': 'True', 'primary_key': 'True'}),
            'id_multiplan': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'lojas.loja': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Loja', '_ormbases': [u'utils.EditorialModel']},
            u'editorialmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['utils.EditorialModel']", 'unique': 'True', 'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        },
        u'utils.editorialmodel': {
            'Meta': {'object_name': 'EditorialModel'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['geral']