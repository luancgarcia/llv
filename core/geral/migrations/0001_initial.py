# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Categoria'
        db.create_table(u'geral_categoria', (
            (u'editorialmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['utils.EditorialModel'], unique=True, primary_key=True)),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=100, null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=150)),
            ('default', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal(u'geral', ['Categoria'])

        # Adding model 'Oferta'
        db.create_table(u'geral_oferta', (
            (u'editorialmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['utils.EditorialModel'], unique=True, primary_key=True)),
            ('loja', self.gf('django.db.models.fields.related.ForeignKey')(blank=True, related_name='ofertas', null=True, to=orm['lojas.Loja'])),
            ('nome', self.gf('django.db.models.fields.CharField')(max_length=200, null=True)),
            ('slug', self.gf('django.db.models.fields.SlugField')(unique=True, max_length=250)),
            ('descricao', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('evento', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('texto_promocional', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
            ('preco_inicial', self.gf('django.db.models.fields.CharField')(max_length=70, null=True)),
            ('preco_final', self.gf('django.db.models.fields.CharField')(max_length=70, null=True)),
            ('desconto', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal(u'geral', ['Oferta'])

        # Adding unique constraint on 'Oferta', fields ['loja', 'slug']
        db.create_unique(u'geral_oferta', ['loja_id', 'slug'])

        # Adding model 'ImagemOferta'
        db.create_table(u'geral_imagemoferta', (
            (u'editorialmodel_ptr', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['utils.EditorialModel'], unique=True, primary_key=True)),
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
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'preco_final': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'preco_inicial': ('django.db.models.fields.CharField', [], {'max_length': '70', 'null': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'unique': 'True', 'max_length': '250'}),
            'texto_promocional': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'})
        },
        u'lojas.loja': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Loja', '_ormbases': [u'utils.EditorialModel']},
            u'editorialmodel_ptr': ('django.db.models.fields.related.OneToOneField', [], {'to': u"orm['utils.EditorialModel']", 'unique': 'True', 'primary_key': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'})
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