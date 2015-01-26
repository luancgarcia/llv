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

    url(r'^modal/(?P<tipo>[\w-]+)/(?P<slug_item>[\w-]+)/$',
        'geral.views.modal_slug', name='modal_slug'),

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

    url(r'^(?P<slug>[\w-]+)/categoria/(?P<categoria>[\w-]+)/$',
        'geral.views.home_com_filtro', name='home_categoria'),
    url(r'^(?P<slug>[\w-]+)/genero/(?P<genero>[\w]+)/$',
        'geral.views.home_com_filtro', name='home_genero'),
    url(r'^(?P<slug>[\w-]+)/loja/(?P<loja>[\w-]+)/$',
        'geral.views.home_com_filtro', name='home_loja'),
    url(r'^(?P<slug>[\w-]+)/preco/(?P<preco>\d+)/$',
        'geral.views.home_com_filtro', name='home_preco'),
    url(r'^(?P<slug>[\w-]+)/desconto/(?P<desconto>\d+)/$',
        'geral.views.home_com_filtro', name='home_desconto'),

    url(r'^solicitar_loja/$',
        'geral.views.solicitar_loja', name='solicitar_loja'),
    url(r'^modal_fb_login/$', 'geral.views.modal_fb_login',
        name='modal_fb_login'),
    url(r'^modal_fb_login_chrome_ios/$', 'geral.views.modal_fb_login_chrome_ios',
        name='modal_fb_login_chrome_ios'),

    url(r'^relatorios/$', 'geral.views.relatorios_index', name='relatorios_index'),
    url(r'^relatorios/(?P<shopping_id>\d+)/$', 'geral.views.relatorios', name='relatorios'),
    url(r'^relatorios/lojas_mais_vistas/(?P<shopping_id>\d+)/$', 'geral.views.lojas_mais_vistas',
        name='lojas_mais_vistas'),
    url(r'^relatorios/lojas_mais_solicitadas/(?P<shopping_id>\d+)/$',
        'geral.views.lojas_mais_solicitadas', name='lojas_mais_solicitadas'),
    url(r'^relatorios/ofertas_mais_vistas/(?P<shopping_id>\d+)/$', 'geral.views.ofertas_mais_vistas',
        name='ofertas_mais_vistas'),
    url(r'^relatorios/ofertas_mais_curtidas/(?P<shopping_id>\d+)/$',
        'geral.views.ofertas_mais_curtidas', name='ofertas_mais_curtidas'),
    url(r'^relatorios/ofertas_mais_compartilhadas/(?P<shopping_id>\d+)/$',
        'geral.views.ofertas_mais_compartilhadas', name='ofertas_mais_compartilhadas'),

    url(r'^(?P<slug>[\w-]+)/$', 'geral.views.home', name='home'),
    url(r'^$', 'geral.views.index', name='index'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
