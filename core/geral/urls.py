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

    url(r'^$', 'geral.views.home', name='home'),
)
