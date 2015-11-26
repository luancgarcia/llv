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

    # password reset
    url(r'^user/password/reset/$',
        'django.contrib.auth.views.password_reset',
        {'post_reset_redirect': '/user/password/reset/done/'},
        name="password_reset"),
    url(r'^user/password/reset/done/$',
        'django.contrib.auth.views.password_reset_done',
        name='password_reset_done'),
    url(r'^user/password/reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$',
        'django.contrib.auth.views.password_reset_confirm',
        {'post_reset_redirect': '/user/password/done/'},
        name='password_reset_confirm'),
    url(r'^user/password/done/$',
        'django.contrib.auth.views.password_reset_complete',
        name='password_reset_complete'),

    # url(r'^recuperar_login/', 'admin.views.recuperar_login', name='admin_login_recover'),

    url(r'^ribeirao-preto-shopping/', 'geral.views.ribeirao', name='ribeirao'),
    url(r'^diamondmall-shopping/', 'geral.views.diamond', name='diamond'),

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
    # relatórios ofertas
    url(r'^relatorios/ofertas_mais_vistas/(?P<shopping_id>\d+)/$', 'geral.views.ofertas_mais_vistas',
        name='ofertas_mais_vistas'),
    url(r'^relatorios/ofertas_mais_curtidas/(?P<shopping_id>\d+)/$',
        'geral.views.ofertas_mais_curtidas', name='ofertas_mais_curtidas'),
    url(r'^relatorios/ofertas_mais_compartilhadas/(?P<shopping_id>\d+)/$',
        'geral.views.ofertas_mais_compartilhadas', name='ofertas_mais_compartilhadas'),

    # relatórios destaques
    url(r'^relatorios/destaques_mais_vistos/(?P<shopping_id>\d+)/$',
        'geral.views.destaques_mais_vistos',
        name='destaques_mais_vistos'),
    url(r'^relatorios/destaques_mais_curtidos/(?P<shopping_id>\d+)/$',
        'geral.views.destaques_mais_curtidos', name='destaques_mais_curtidos'),
    url(r'^relatorios/destaques_mais_compartilhados/(?P<shopping_id>\d+)/$',
        'geral.views.destaques_mais_compartilhados', name='destaques_mais_compartilhados'),

    # relatórios eventos
    url(r'^relatorios/eventos_mais_vistos/(?P<shopping_id>\d+)/$',
        'geral.views.eventos_mais_vistos', name='eventos_mais_vistos'),
    url(r'^relatorios/eventos_mais_curtidos/(?P<shopping_id>\d+)/$',
        'geral.views.eventos_mais_curtidos', name='eventos_mais_curtidos'),
    url(r'^relatorios/eventos_mais_compartilhados/(?P<shopping_id>\d+)/$',
        'geral.views.eventos_mais_compartilhados', name='eventos_mais_compartilhados'),

    # relatórios categorias
    url(r'^relatorios/categorias_mais_vistas/(?P<shopping_id>\d+)/$',
        'geral.views.categorias_mais_vistas', name='categorias_mais_vistas'),

    # api webservice
    # url(r'^api/ofertas/(?P<slug>[\w-]+)$', 'api.views.ofertas', name='api_ofertas'),
    url(r'^api/ofertas/$', 'api.views.ofertas', name='api_ofertas'),
    url(r'^api/shoppings/$', 'api.views.shoppings', name='api_shopping'),

    url(r'^ranking/$', 'rankings.views.ranking_index', name='ranking_index'),

    url(r'^ajax_command/(?P<command>[\w_-]+)/$',
        'notificacoes.views.ajax_command', name='ajax_command'),
    url(r'^force/command/(?P<comando>[\w_-]+)/$',
        'notificacoes.views.command', name='command'),

    url(r'^(?P<slug>[\w-]+)/$', 'geral.views.home', name='home'),
    url(r'^$', 'geral.views.index', name='index'),
)

if settings.DEBUG:
    urlpatterns += patterns('django.views.static',
        (r'media/(?P<path>.*)', 'serve', {'document_root': settings.MEDIA_ROOT, 'show_indexes': True}),
    )
