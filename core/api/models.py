# -*- encoding: utf-8 -*-
import hashlib
from datetime import date

from django.db import models

from lojas.models import Shopping
from signals import apiuser_post_save


class ApiUser(models.Model):
    shopping = models.ManyToManyField(Shopping, related_name='tokens', verbose_name=u'Shopping')
    nome = models.CharField(u'Nome', max_length=255)
    email = models.EmailField('E-mail', unique=True)
    token = models.CharField('Token', max_length=64, null=False)

    class Meta:
        verbose_name = u'Usuário de API'
        verbose_name_plural = u'Usuários da API'

    def __unicode__(self):
        return '%s (%s)' % (self.nome, self.email)

    @classmethod
    def create_token(cls, parametro):
        '''
        Gera token de cada usuário com acesso à API
        Deve ser usado apenas ao criar e campo não deve ser atualizado mais, em tempo algum.
        '''
        base_token = '%s@%s' % (parametro, date.today())
        return hashlib.sha256(base_token).hexdigest()

    # todo: criar método para notificar usuário que chave foi criada


class ApiSession(models.Model):
    user = models.ForeignKey(ApiUser, related_name='sessoes', verbose_name=u'Usuário da API')
    inicio = models.DateTimeField(u'Início', auto_now_add=True)
    fim = models.DateTimeField(u'Fim', null=True)

    class Meta:
        verbose_name = u'Sessão da API'
        verbose_name_plural = u'Sessões da API'

    def __unicode__(self):
        return '%s - %s' % (self.user, self.inicio)

    #Todo: criar método pra reportar tempo passado desde o inicio
    #Todo: terminar a sessão ou expirar o tempo, fechar sessão e gravar fim


class ApiLog(models.Model):
    sessao = models.ForeignKey(ApiSession, related_name='logs', verbose_name=u'Sessão do usuário')
    texto = models.CharField(u'Text', blank=True, null=True, max_length=255)

    class Meta:
        verbose_name = u'Log da API'
        verbose_name_plural = u'Logs da API'

    def __unicode__(self):
        return u'log da sessão %s' % self.sessao


models.signals.post_save.connect(apiuser_post_save, sender=ApiUser)