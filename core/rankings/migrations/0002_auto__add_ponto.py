# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Ponto'
        db.create_table(u'rankings_ponto', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_criacao', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('data_atualizacao', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('intervalo', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pontos', to=orm['rankings.Intervalo'])),
            ('loja', self.gf('django.db.models.fields.related.ForeignKey')(related_name='pontos', to=orm['lojas.Loja'])),
            ('produtos', self.gf('django.db.models.fields.IntegerField')()),
            ('fotos', self.gf('django.db.models.fields.IntegerField')()),
            ('likes', self.gf('django.db.models.fields.IntegerField')()),
            ('shares', self.gf('django.db.models.fields.IntegerField')()),
            ('desconto_30', self.gf('django.db.models.fields.IntegerField')()),
            ('desconto_50', self.gf('django.db.models.fields.IntegerField')()),
            ('desconto_70', self.gf('django.db.models.fields.IntegerField')()),
            ('desconto_100', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal(u'rankings', ['Ponto'])


    def backwards(self, orm):
        # Deleting model 'Ponto'
        db.delete_table(u'rankings_ponto')


    models = {
        u'lojas.loja': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Loja'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'id_multilan': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'logo': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shopping': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'lojas'", 'to': u"orm['lojas.Shopping']"}),
            'slug': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'telefone': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'})
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
        },
        u'rankings.intervalo': {
            'Meta': {'object_name': 'Intervalo'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'fim': ('django.db.models.fields.DateField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {})
        },
        u'rankings.ponto': {
            'Meta': {'object_name': 'Ponto'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desconto_100': ('django.db.models.fields.IntegerField', [], {}),
            'desconto_30': ('django.db.models.fields.IntegerField', [], {}),
            'desconto_50': ('django.db.models.fields.IntegerField', [], {}),
            'desconto_70': ('django.db.models.fields.IntegerField', [], {}),
            'fotos': ('django.db.models.fields.IntegerField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'intervalo': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pontos'", 'to': u"orm['rankings.Intervalo']"}),
            'likes': ('django.db.models.fields.IntegerField', [], {}),
            'loja': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'pontos'", 'to': u"orm['lojas.Loja']"}),
            'produtos': ('django.db.models.fields.IntegerField', [], {}),
            'shares': ('django.db.models.fields.IntegerField', [], {})
        }
    }

    complete_apps = ['rankings']