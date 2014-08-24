# -*- encoding: utf-8 -*-

from django.contrib import admin

from notificacoes.models import Notificacao, Solicitacao


admin.site.register(Notificacao)
admin.site.register(Solicitacao)
