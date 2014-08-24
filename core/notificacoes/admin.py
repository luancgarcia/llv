# -*- encoding: utf-8 -*-

from django.contrib import admin

from notificacoes.models import Notificacao, Solicitacao


class NotificacaoAdmin(admin.ModelAdmin):
    list_filter = ['lida','resolvida']
    list_display = ['oferta','lida','resolvida','enviada_mkt','enviada_lojista']
    list_editable = ['lida']


class SolicitacaoAdmin(admin.ModelAdmin):
    list_filter = ['loja__shopping']


admin.site.register(Notificacao, NotificacaoAdmin)
admin.site.register(Solicitacao, SolicitacaoAdmin)
