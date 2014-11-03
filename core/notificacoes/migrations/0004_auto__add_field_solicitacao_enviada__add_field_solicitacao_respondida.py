# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Solicitacao.enviada'
        db.add_column(u'notificacoes_solicitacao', 'enviada',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)

        # Adding field 'Solicitacao.respondida'
        db.add_column(u'notificacoes_solicitacao', 'respondida',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Solicitacao.enviada'
        db.delete_column(u'notificacoes_solicitacao', 'enviada')

        # Deleting field 'Solicitacao.respondida'
        db.delete_column(u'notificacoes_solicitacao', 'respondida')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        u'geral.categoria': {
            'Meta': {'ordering': "['nome']", 'unique_together': "(('shopping', 'slug'),)", 'object_name': 'Categoria'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'imagem': ('django.db.models.fields.files.ImageField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True'}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sazonal': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shopping': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'categorias'", 'null': 'True', 'to': u"orm['lojas.Shopping']"}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '150'})
        },
        u'geral.oferta': {
            'Meta': {'ordering': "['-data_aprovacao', 'nome']", 'unique_together': "(('loja', 'slug'),)", 'object_name': 'Oferta'},
            'autor': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['geral.Perfil']", 'null': 'True'}),
            'categoria': ('django.db.models.fields.related.ManyToManyField', [], {'blank': 'True', 'related_name': "'ofertas'", 'null': 'True', 'symmetrical': 'False', 'to': u"orm['geral.Categoria']"}),
            'data_aprovacao': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'desconto': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'descricao': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'evento': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'fim': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'genero': ('django.db.models.fields.IntegerField', [], {'default': '3', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'inicio': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'loja': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'ofertas'", 'null': 'True', 'to': u"orm['lojas.Loja']"}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True'}),
            'preco_final': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'preco_inicial': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '8', 'decimal_places': '2', 'blank': 'True'}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'shopping': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['lojas.Shopping']", 'null': 'True', 'blank': 'True'}),
            'slug': ('django.db.models.fields.SlugField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'texto_link': ('django.db.models.fields.CharField', [], {'max_length': "'140'", 'null': 'True', 'blank': 'True'}),
            'texto_promocional': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'tipo': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        },
        u'geral.perfil': {
            'Meta': {'object_name': 'Perfil'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'loja': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'usuarios'", 'null': 'True', 'to': u"orm['lojas.Loja']"}),
            'shopping': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'usuarios'", 'null': 'True', 'to': u"orm['lojas.Shopping']"}),
            'tipo': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'perfil'", 'to': u"orm['auth.User']"})
        },
        u'lojas.loja': {
            'Meta': {'ordering': "['nome']", 'object_name': 'Loja'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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
        u'notificacoes.notificacao': {
            'Meta': {'object_name': 'Notificacao'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'enviada_lojista': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'enviada_mkt': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lida': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'mensagem': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'oferta': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'notificacoes'", 'null': 'True', 'to': u"orm['geral.Oferta']"}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'resolvida': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'responsavel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'responsavel'", 'null': 'True', 'to': u"orm['geral.Perfil']"}),
            'solicitante': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'solicitante'", 'null': 'True', 'to': u"orm['geral.Perfil']"})
        },
        u'notificacoes.solicitacao': {
            'Meta': {'object_name': 'Solicitacao'},
            'data_atualizacao': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'data_criacao': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'email': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'enviada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lida': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'loja': ('django.db.models.fields.related.ForeignKey', [], {'blank': 'True', 'related_name': "'solicitacoes'", 'null': 'True', 'to': u"orm['lojas.Loja']"}),
            'mensagem': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'nome': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True'}),
            'publicada': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'respondida': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['notificacoes']