# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, url


urlpatterns = patterns('',
    url(r'grid/$',
        'html.views.html_grid',
        name='html_grid'),

   	url(r'home/$',
        'html.views.html_home',
        name='html_home'),
)
