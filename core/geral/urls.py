# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'core.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^html/', include('html.urls')),

    url(r'^admin/', include(admin.site.urls)),

    url(r'^modais/produto',
        'html.views.html_modal_produtos',
        name='html_modal_produtos'),

    url(r'^modais/destaque',
        'html.views.html_modal_destaque',
        name='html_modal_destaque'),

    url(r'^modais/evento',
        'html.views.html_modal_evento',
        name='html_modal_evento'),

    url(r'^modais/share',
        'html.views.html_modal_share',
        name='html_modal_share'),

    url(r'^$', 'geral.views.home', name='home'),
)
