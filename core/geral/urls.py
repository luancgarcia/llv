# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url

from django.contrib import admin
from django.conf import settings
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'core.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    # url(r'^html/', include('html.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^modais/(?P<tipo>[\w-]+)/(?P<id_item>\d+)/$',
        'geral.views.modal',
        name='modal'),

    url(r'^compartilhar/(?P<id_item>\d+)/$',
        'geral.views.modal_share',
        name='modal_share'),

    url(r'^curtir/$', 'geral.views.curtir', name='curtir'),
    url(r'^descurtir/$', 'geral.views.descurtir', name='descurtir'),
    url(r'^mesclar/$', 'geral.views.mesclar', name='mesclar'),

    # url(r'^modais/destaque/(?P<id_item>\d+)/$',
    #     'geral.views.modal',
    #     name='modal_destaque'),

    # url(r'^modais/evento/(?P<id_item>\d+)/$',
    #     'geral.views.modal',
    #     name='modal_evento'),

    # url(r'^modais/share',
    #     'html.views.html_modal_share',
    #     name='html_modal_share'),

    url(r'^admin/orderedmove/(?P<direction>up|down)/(?P<model_type_id>\d+)/(?P<model_id>\d+)/$', 'utils.views.admin_move_ordered_model', name="admin-move"),

    url(r'^mais_ofertas/$', 'geral.views.mais_ofertas', name='mais_ofertas'),

    url(r'^categoria/(?P<categoria>[\w-]+)/$', 'geral.views.home_com_filtro', name='home_categoria'),
    url(r'^genero/(?P<genero>[\w]+)/$', 'geral.views.home_com_filtro', name='home_genero'),
    url(r'^loja/(?P<loja>[\w-]+)/$', 'geral.views.home_com_filtro', name='home_loja'),
    url(r'^preco/(?P<preco>\d+)/$', 'geral.views.home_com_filtro', name='home_preco'),
    url(r'^desconto/(?P<desconto>\d+)/$', 'geral.views.home_com_filtro', name='home_desconto'),

    url(r'^solicitar_loja/$', 'geral.views.solicitar_loja', name='solicitar_loja'),

    url(r'^$', 'geral.views.home', name='home'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
