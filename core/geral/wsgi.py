"""
WSGI config for core project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/howto/deployment/wsgi/
"""

#!/home/liquidacaolapisv/public_html/.virtualenvs/llv/bin/activate
import os
import sys
import site

site_packages = '/home/liquidacaolapisv/public_html/.virtualenvs/llv/lib/python2.7/site-packages'
site.addsitedir(os.path.abspath(site_packages))

sys.path.insert(0, '/home/liquidacaolapisv/public_html/llv/core')
sys.path.insert(0, '/home/liquidacaolapisv/public_html/llv/core/geral')
sys.path.insert(0, '/home/liquidacaolapisv/public_html/.virtualenvs/llv/lib/python2.7/site-packages')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "core.geral.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
