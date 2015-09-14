# -*- encoding: utf-8 -*-
import hashlib
from datetime import date, datetime, timedelta

from django.db import models
from django.conf import settings

from lojas.models import Shopping
from signals import apiuser_post_save

from utils.models import BaseModel


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


class ApiSession(BaseModel):
    user = models.ForeignKey(ApiUser, related_name='sessoes', verbose_name=u'Usuário da API')
    inicio = models.DateTimeField(u'Início', auto_now_add=True)
    fim = models.DateTimeField(u'Fim', null=True)

    class Meta:
        verbose_name = u'Sessão da API'
        verbose_name_plural = u'Sessões da API'

    def __unicode__(self):
        return '%s - %s' % (self.user, self.inicio)

    @classmethod
    def finaliza_sessoes_abertas(cls, usuario):
        abertas = cls.objects.filter(user=usuario, fim__isnull=True)
        for a in abertas:
            deveria_expirar = a.inicio + timedelta(minutes=settings.TEMPO_MAXIMO_SESSAO_API)
            if datetime.now() >= deveria_expirar:
                a.fim = deveria_expirar
                a.save()

    @classmethod
    def cria_sessao(cls, usuario):
        cls.finaliza_sessoes_abertas(usuario)
        try:
            tem_sessao = cls.objects.get_or_none(user=usuario, fim__isnull=True)
        except:
            tem_sessao = cls.objects.filter(user=usuario, fim__isnull=True).latest('id')

        if tem_sessao:
            sessao = tem_sessao
        else:
            sessao = cls.objects.create(user=usuario)

        return sessao


class ApiLog(models.Model):
    AUTENTICACAO = 0
    CONSUMO = 1

    TIPO = (
        (AUTENTICACAO, u'Autenticação'),
        (CONSUMO, u'Consumo de dados')
    )

    sessao = models.ForeignKey(ApiSession, related_name='logs', verbose_name=u'Sessão do usuário')
    texto = models.CharField(u'Text', blank=True, null=True, max_length=255)
    tipo = models.IntegerField(u'Tipo', blank=False, null=True)

    class Meta:
        verbose_name = u'Log da API'
        verbose_name_plural = u'Logs da API'

    def __unicode__(self):
        return u'log da sessão %s' % self.sessao

    @classmethod
    def cria_log(cls, sessao, texto, tipo):
        cls.objects.create(sessao=sessao, texto=texto[:254], tipo=tipo)


models.signals.post_save.connect(apiuser_post_save, sender=ApiUser)