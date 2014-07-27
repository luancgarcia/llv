# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Shopping'
        db.create_table(u'geral_shopping', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_criacao', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('data_atualizacao', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('publicada', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=150)),
            ('id_multiplan', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'geral', ['Shopping'])

        # Adding model 'Categoria'
        db.create_table(u'geral_categoria', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_criacao', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('data_atualizacao', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('publicada', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=150)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'geral', ['Categoria'])

        # Adding model 'Oferta'
        db.create_table(u'geral_oferta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_criacao', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('data_atualizacao', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('publicada', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('loja', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ofertas', null=True, to=orm['lojas.Loja'])),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=200, null=True, blank=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(max_length=250, unique=True, null=True, blank=True)),
            ('descricao', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('evento', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('texto_promocional', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('preco_inicial', self.gf('django.db.models.fields.CharField')(max_length=70, null=True)),
            ('preco_final', self.gf('django.db.models.fields.CharField')(max_length=70, null=True)),
            ('desconto', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('tipo', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('texto_link', self.gf('django.db.models.fields.CharField')(max_length='140', null=True)),
        ))
        db.send_create_signal(u'geral', ['Oferta'])

        # Adding unique constraint on 'Oferta', fields ['loja', 'slug']
        db.create_unique(u'geral_oferta', ['loja_id', 'slug'])

        # Adding model 'ImagemOferta'
        db.create_table(u'geral_imagemoferta', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_criacao', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('data_atualizacao', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('ordem', self.gf('django.db.models.fields.PositiveIntegerField')(default=1)),
            ('oferta', self.gf('django.db.models.fields.related.ForeignKey')(related_name='imagens', to=orm['geral.Oferta'])),
            ('imagem', self.gf('django.db.models.fields.files.ImageField')(max_length=100, null=True, blank=True)),
            ('principal', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('vertical', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'geral', ['ImagemOferta'])

        # Adding model 'Log'
        db.create_table(u'geral_log', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('data_criacao', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('data_atualizacao', self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, blank=True)),
            ('oferta', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='logs', null=True, to=orm['geral.Oferta'])),
            ('acao', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'geral', ['Log'])


    def backwards(self, orm):
        # Removing unique constraint on 'Oferta', fields ['loja', 'slug']
        db.delete_unique(u'geral_oferta', ['loja_id', 'slug'])

        # Deleting model 'Shopping'
        db.delete_table(u'geral_shopping')

        # Deleting model 'Categoria'
        db.delete_table(u'geral_categoria')

        # Deleting model 'Oferta'
        db.delete_table(u'geral_oferta')

        # Deleting model 'ImagemOferta'
        db.delete_table(u'geral_imagemoferta')

        # Deleting model 'Log'
        db.delete_table(u'geral_log')


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
            'Meta': {'object_name': 'ImagemOferta'},
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