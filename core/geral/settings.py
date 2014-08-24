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

FALE_CONOSCO = ['jonatas.cd@gmail.com','rachelrubia@gmail.com','marcusribeirooo@gmail.com']
EMAIL_FROM = "jonatas.cd@gmail.com"

EMAIL_HOST = "smtp.gmail.com"
EMAIL_HOST_USER = "jonatas.cd@gmail.com"
EMAIL_HOST_PASSWORD = 'yourpassword'
EMAIL_PORT = 587
EMAIL_USE_TLS = True

# SITE_URL = "https://apps.facebook.com/llv-dev/"
# SITE_URL = "https://jonatascd.pythonanywhere.com/"
SITE_URL = "http://llv.liquidacaolapisvermelho.com.br"

STATIC_ROOT = os.path.join(PROJECT_DIR, 'static')
# STATIC_URL = '/static/'
STATIC_URL = '%s%s' % (SITE_URL, '/static/')

MEDIA_ROOT = os.path.join(PROJECT_DIR, 'media')
# MEDIA_URL = '/media/'
MEDIA_URL = '%s%s' % (SITE_URL, '/media/')

STATICFILES_DIRS = (
    # os.path.join(BASE_DIR, "static"),
)

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

FACEBOOK_APP_ID = "698128933600347"
FACEBOOK_APP_SECRET = "af6ed6874f6e259644ad69b62b8ffc4f"

WSDL_URL = 'http://wiseit.multiplan.com.br:8080/WebService2/services/wiseitws?wsdl'

COMPARTILHADAS_PASTA = os.path.join(MEDIA_ROOT, 'compartilhar')
COMPARTILHADAS_URL = SITE_URL+'media/compartilhar/'


try:
    from custom_settings import *
except ImportError:
    pass
