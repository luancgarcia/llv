# -*- encoding: utf-8 -*-

import xadmin
xadmin.autodiscover()

from django.conf.urls import patterns, include, url

# from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'core.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^html/', include('html.urls')),

    url(r'^admin/', include(xadmin.site.urls)),
)
