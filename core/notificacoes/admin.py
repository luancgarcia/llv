# -*- encoding: utf-8 -*-

from django.contrib import admin
from django.db.models import Q

from notificacoes.models import Notificacao, Solicitacao


class NotificacaoAdmin(admin.ModelAdmin):
    exclude = ['publicada']
    list_filter = ['lida','resolvida']
    list_display = ['solicitante', 'responsavel', 'oferta', 'lida', 'resolvida',
                    'enviada_mkt', 'enviada_lojista']
    list_editable = ['lida']

    def queryset(self, request):
        qs = super(NotificacaoAdmin, self).queryset(request)
        perfil = request.user.perfil.get()
        # print perfil, perfil.id
        if perfil and not perfil.is_adm:
            qs = qs.filter(Q(solicitante=perfil) | Q(responsavel=perfil))
        return qs


class SolicitacaoAdmin(admin.ModelAdmin):
    exclude = ['publicada']
    list_filter = ['loja__shopping', 'enviada', 'respondida']
    list_display = ['nome', 'email', 'loja', 'enviada', 'respondida']

    def queryset(self, request):
        qs = super(SolicitacaoAdmin, self).queryset(request)
        perfil = request.user.perfil.get()
        if not perfil.is_adm:
            qs = qs.filter(loja=perfil.loja)
        return qs


admin.site.register(Notificacao, NotificacaoAdmin)
admin.site.register(Solicitacao, SolicitacaoAdmin)
