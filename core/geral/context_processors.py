# -*- encoding: utf-8 -*-
from django.conf import settings

def context(request):
    '''
    Define um contexto de variaveis acessíveis em todas as views.
    '''
    return {'SITE_URL': settings.SITE_URL,
            'STATIC_URL': settings.STATIC_URL,}
