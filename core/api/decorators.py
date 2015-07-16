# -*- encoding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from models import ApiUser

def valida_token(funcao):
    def _wrap(*args, **kwargs):
        request = args[0]
        email, token = request.META['HTTP_AUTHORIZATION'].split(' ')
        try:
            usuario = ApiUser.objects.get(email=email, token=token)
        except ObjectDoesNotExist:
            return HttpResponse('Credencial não valida', status=401)

        kwargs['usuario'] = usuario
        return funcao(request, *args, **kwargs)
    return _wrap