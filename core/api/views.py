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
    id_multiplan = request.GET.get('id_multiplan', None)
    tipo = request.GET.get('type', None)
    dados = {'error': None, 'error_message': None}
    if not slug and not id_multiplan:
        dados.update({'error': 'Shopping não informado',
                      'error_message': 'Favor informe a slug do shopping ou id do shopping na '
                                       'Multiplan'})
    elif id_multiplan:
        dados.update({'ofertas': Oferta.prontos_api(id_multiplan=id_multiplan)})
    else:
        shopping = Shopping.objects.get(slug=slug)
        dados.update({'ofertas': Oferta.prontos_api(shopping=shopping.id)})
    return retorno(dados, tipo)

def shoppings(request):
    slug = request.GET.get('slug', None)
    nome = request.GET.get('nome', None)
    dados = {'error': u'Shopping não encontrado'}
    if not slug and not nome:
        dados = {'shoppings': [s.to_api() for s in Shopping.objects.all()]}
    elif slug:
        try:
            mall = Shopping.objects.get(slug=slug)
            dados = mall.to_api()
        except ObjectDoesNotExist:
            pass
    elif nome:
        malls = Shopping.objects.filter(nome__icontains=nome)
        if malls:
            dados = {'shoppings': [s.to_api() for s in malls]}
    return retorno(dados, 'json')