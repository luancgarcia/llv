# -*- encoding: utf-8 -*-
from django.core.exceptions import ObjectDoesNotExist
from django.http import HttpResponse

from models import ApiUser, ApiSession

def valida_token(funcao):
    def _wrap(*args, **kwargs):
        request = args[0]
        email, token = request.META['HTTP_AUTHORIZATION'].split(' ')
        try:
            usuario = ApiUser.objects.get(email=email, token=token)
            sessao = ApiSession.cria_sessao(usuario)
        except ObjectDoesNotExist:
            return HttpResponse('Credencial invalida', status=401)

        kwargs['usuario'] = usuario
        kwargs['sessao'] = sessao
        return funcao(request, *args, **kwargs)
    return _wrap