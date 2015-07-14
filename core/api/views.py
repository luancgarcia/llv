# -*- encoding: utf-8 -*-
import simplejson as json

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from geral.models import Oferta
from lojas.models import Shopping


def retorno(dados, tipo):
    if tipo and tipo.lower() == 'xml':
        return HttpResponse(json.dumps(dados), content_type="text/xml")
    else:
        return HttpResponse(json.dumps(dados), content_type="application/json")

def ofertas(request):
    slug = request.GET.get('slug', None)
    id_shopping = request.GET.get('id_shopping', None)
    tipo = request.GET.get('type', None)
    dados = {'error': None, 'error_message': None}
    if not slug and not id_shopping:
        dados.update({'error': 'Shopping não informado',
                      'error_message': 'Favor informe a slug do shopping ou id do shopping na '
                                       'Multiplan'})
    elif id_shopping:
        shopping = Shopping.objects.get(id_multiplan=id_shopping)
        dados.update({'ofertas': Oferta.prontos_api(shopping=shopping.id)})
    else:
        shopping = Shopping.objects.get(slug=slug)
        dados.update({'ofertas': Oferta.prontos_api(shopping=shopping.id)})
    return retorno(dados, tipo)

def shopping(request, slug):
    if not slug:
        dados = {'error': u'Slug não informado'}
    try:
        mall = Shopping.objects.get(slug=slug)
        dados = mall.to_api()
    except ObjectDoesNotExist:
        dados = {'error': u'Shopping não encontrado'}
    return retorno(dados, 'json')