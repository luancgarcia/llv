# -*- encoding: utf-8 -*-
import simplejson as json

from django.http import HttpResponse

from geral.models import Oferta, Shopping


def retorno(dados, tipo):
    if tipo and tipo.lower() == 'xml':
        return HttpResponse(json.dumps(dados), content_type="text/xml")
    else:
        return HttpResponse(json.dumps(dados), content_type="application/json")

def ofertas(request):
    slug = request.GET.get('slug', None)
    tipo = request.GET.get('type', None)
    dados = {'error': None, 'error_message': None}
    if not slug:
        dados.update({'error': 'Shopping não informado',
                      'error_message': 'Favor informe a slug do shopping. Ex. barra-shopping'})
    else:
        shopping = Shopping.objects.get(slug=slug)
        dados.update({'ofertas': Oferta.prontos_api(shopping=shopping.id)})
    return retorno(dados, tipo)
