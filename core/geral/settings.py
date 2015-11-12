"""
Django settings for core project.

For more information on this file, see
https://docs.djangoproject.com/en/1.6/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.6/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
BASE_DIR = os.path.dirname(os.path.dirname(__file__))
PROJECT_DIR = os.path.abspath(os.path.dirname('%s/../../' % os.path.dirname(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.6/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'p2woyo504e(rah%6cn9l57-4j69)kj+!k!l6&e12!v9e%@2j*d'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

TEMPLATE_DEBUG = True

ALLOWED_HOSTS = []

MANAGERS = ADMINS = (
    ('Jonatas C Damasceno', 'jonatas.cd@gmail.com'),
    ('Rachel Rubia', 'rachelrubia@gmail.com'),
    ('Marcus Ribeiro', 'marcusribeirooo@gmail.com'),
)

FALE_CONOSCO = ['jonatas.cd@gmail.com', 'rachelrubia@gmail.com',
                'marcusribeirooo@gmail.com']
NOTIFICACAO = ['jonatas.cd@gmail.com', 'llv@kinda.com.br']

EMAIL_FROM = "noreply@liquidacaolapisvermelho.com.br"

EMAIL_BACKEND = 'django_smtp_ssl.SSLEmailBackend'
EMAIL_HOST = "llv.weblocal.com.br"
EMAIL_HOST_USER = "noreply@liquidacaolapisvermelho.com.br"
EMAIL_HOST_PASSWORD = 'llv2014'
EMAIL_PORT = 465
EMAIL_USE_TLS = True

# SITE_URL = "https://apps.facebook.com/llv-dev/"
SITE_URL = "https://www.liquidacaolapisvermelho.com.br"
SHARE_URL = "http://www.liquidacaolapisvermelho.com.br"
#SHARE_URL = "http://liquidacaolapisvermelho.com.br"
# SITE_URL = "http://localhost:8989"

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
# STATIC_URL = '/static/'
STATIC_URL = '%s%s' % (SITE_URL, '/static/')

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
# MEDIA_URL = '/media/'
MEDIA_URL = '%s%s' % (SITE_URL, '/media/')

STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, "static"),
)

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        'LOCATION': '127.0.0.1:11211',
    }
}

STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
#    'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Application definition
INSTALLED_APPS = (
    'bootstrap_admin',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'geral',
    'html',
    'lojas',
    'utils',
    'notificacoes',
    'api',
    'rankings',
    'imagekit',

    'south',
    'crispy_forms'
)

MIDDLEWARE_CLASSES = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    # 'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    # 'django.middleware.clickjacking.XFrameOptionsMiddleware',
)

ROOT_URLCONF = 'geral.urls'

WSGI_APPLICATION = 'geral.wsgi.application'


# Database
# https://docs.djangoproject.com/en/1.6/ref/settings/#databases

DATABASES = {
    'default': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'llv',
       'USER': '',
       'PASSWORD': '',
       'HOST': '',
       'PORT': '',
   },
   'mysql-inno-init': {
       'ENGINE': 'django.db.backends.mysql',
       'NAME': 'llv',
       'USER': '',
       'PASSWORD': '',
       'HOST': '',
       'PORT': '',
       'OPTIONS': {
           'init_command': 'SET storage_engine=INNODB',
       },
   },
}

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_DIR, 'core/templates'),
)

TEMPLATE_CONTEXT_PROCESSORS = (
    "django.contrib.auth.context_processors.auth",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.core.context_processors.request",
    "django.core.context_processors.i18n",
    "django.core.context_processors.media",
    "django.core.context_processors.static",
    "django.contrib.messages.context_processors.messages",
    "geral.context_processors.context",
)

# Internationalization
# https://docs.djangoproject.com/en/1.6/topics/i18n/

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_L10N = True

USE_TZ = False

DECIMAL_SEPARATOR = ','
THOUSAND_SEPARATOR = '.'
USE_THOUSAND_SEPARATOR = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.6/howto/static-files/

AUTH_PROFILE_MODULE = 'geral.Perfil'

FACEBOOK_APP_ID = "705413109545842"
FACEBOOK_APP_SECRET = "f8b13cf59845de6b51226d8da6f8c1a9"

WSDL_URL = 'http://wiseit.multiplan.com.br:8080/WebService2/services/wiseitws?wsdl'

COMPARTILHADAS_PASTA = os.path.join(MEDIA_ROOT, 'compartilhar')
COMPARTILHADAS_URL = SHARE_URL+'/media/compartilhar/'

# secure proxy SSL header and secure cookies
SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# session expire at browser close
SESSION_EXPIRE_AT_BROWSER_CLOSE = True

# wsgi scheme
os.environ['wsgi.url_scheme'] = 'https'

FONTE_FOLDER = os.path.join(STATIC_ROOT, 'fonts')
FONTE_SHARE = '%s/%s' % (FONTE_FOLDER, 'Arial.ttf')

TEMPO_MAXIMO_SESSAO_API = 10 # em minutos

try:
    from custom_settings import *
except ImportError:
    pass
