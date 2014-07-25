# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'grid/$',
        'html.views.html_grid',
        name='html_grid'),

    url(r'home/$',
        'html.views.html_home',
        name='html_home'),

    url(r'^home/modais/produto',
        'html.views.html_modal_produtos',
        name='html_modal_produtos'),

    url(r'^home/modais/destaque',
        'html.views.html_modal_destaque',
        name='html_modal_destaque'),

    url(r'^home/modais/evento',
        'html.views.html_modal_evento',
        name='html_modal_evento'),

    url(r'^home/modais/share',
        'html.views.html_modal_share',
        name='html_modal_share'),
)
