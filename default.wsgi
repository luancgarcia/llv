#!/home/liquidacaolapisv/public_html/.virtualenvs/llv/bin/activate
import os
import sys
import site

site_packages = '/home2/liquidacaolapisv/public_html/.virtualenvs/llv/lib/python2.7/site-packages'
site.addsitedir(os.path.abspath(site_packages))

sys.path.insert(0, '/home2/liquidacaolapisv/public_html/llv/core')
sys.path.insert(0, '/home2/liquidacaolapisv/public_html/llv/core/geral')
sys.path.insert(0, '/home2/liquidacaolapisv/public_html/.virtualenvs/llv/lib/python2.7/site-packages')

os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
