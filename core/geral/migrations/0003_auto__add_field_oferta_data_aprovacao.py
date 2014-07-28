# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Oferta.data_aprovacao'
        db.add_column(u'geral_oferta', 'data_aprovacao',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Oferta.data_aprovacao'
        db.delete_column(u'geral_oferta', 'data_aprovacao')


    models = {
        u'geral.categoria': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Categoria'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'default': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'geral.imagemoferta': {
            'Meta': {'ordering': "['oferta', 'ordem']", 'object_name': 'ImagemOferta'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagem': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'oferta': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'imagens'", 'to': u"orm['geral.Oferta']"}),
            'ordem': ('django.db.models.fields.PositiveIntegerField', [], {'default': '1'}),
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
            'Meta': {'ordering': "['nome']", 'unique_together': "(('loja', 'slug'),)", 'object_name': 'Oferta'},
            'data_aprovacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desconto': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descricao': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'evento': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loja': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ofertas'", 'null': 'True', 'to': u"orm['lojas.Loja']"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'preco_final': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'preco_inicial': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'texto_link': ('django.db.models.fields.CharField', [], {'max_length': "'140'", 'null': 'True'}),
            'texto_promocional': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'geral.shopping': {
            'Meta': {'object_name': 'Shopping'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_multiplan': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '150'})
        },
        u'lojas.loja': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Loja'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
        }
    }

    complete_apps = ['geral']