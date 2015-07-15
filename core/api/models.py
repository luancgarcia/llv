# -*- encoding: utf-8 -*-
import hashlib
from datetime import datetime

from django.db import models

from lojas.models import Shopping


class ApiUser(models.Model):
    shopping = models.ForeignKey(Shopping, related_name='tokens', verbose_name=u'Shopping')
    nome = models.CharField(u'Nome', max_length=255)
    email = models.EmailField('E-mail', unique=True)
    token = models.CharField('Token', max_length=64, editable=False)

    @classmethod
    def create_token(cls, slug_shopping):
        '''
        Gera token de cada usuário com acesso à API
        Deve ser usado apenas ao criar e campo não deve ser atualizado mais, em tempo algum.
        '''
        base_token = '%s@%s' % (slug_shopping, datetime.now())
        return hashlib.sha256(base_token).hexdigest()


class ApiSession(models.Model):
    user = models.ForeignKey(ApiUser, related_name='sessoes', verbose_name=u'Usuário da API')
    inicio = models.DateTimeField(u'Início', auto_now_add=True)
    fim = models.DateTimeField(u'Fim')

    #Todo:
    # - criar método pra reportar tempo passado desde o inicio
    # - terminar a sessão ou expirar o tempo, fechar sessão e gravar fim


class ApiLog(models.Model):
    sessao = models.ForeignKey(ApiSession, related_name='logs', verbose_name=u'Sessão do usuário')