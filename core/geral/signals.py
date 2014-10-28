# -*- encoding: utf-8 -*-

'''
Módulo de signals da app `geral`.
'''

from notificacoes.models import Notificacao

def cria_envia_notificacao(sender, instance, created, **kwargs):
    oferta = instance
    if oferta and oferta.status < 1:
        n, created = Notificacao.objects.get_or_create(oferta=oferta,
                                                       solicitante=oferta.autor)
        if n:
            n.oferta = oferta
            n.responsavel = oferta.marketing_responsavel
            n.save()
            n.notifica_criacao()
        pass

def completa_slug(sender, instance, created, **kwargs):
    item = instance
    if item and item.slug and not item.slug.endswith('%s'%item.id):
        item.slug = '%s-%s' % (item.slug, item.id)
        item.save()