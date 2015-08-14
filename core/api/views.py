# -*- encoding: utf-8 -*-
import simplejson as json

from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist

from geral.models import Oferta
from lojas.models import Shopping
from decorators import valida_token


def retorno(dados, tipo):
    if tipo and tipo.lower() == 'xml':
        return HttpResponse(json.dumps(dados), content_type="text/xml")
    else:
        return HttpResponse(json.dumps(dados), content_type="application/json")

@valida_token
def ofertas(request, *args, **kwargs):
    tipo = request.GET.get('type', None)
    if request.method != 'GET':
        dados = {'error': u'Método inválido', 'error_message': u'Método não permitido nesse serviço'}
    else:
        slug = request.GET.get('slug', None)
        id_multiplan = request.GET.get('id_multiplan', None)
        id_multiplan = int(id_multiplan) if id_multiplan else None
        from_id = request.GET.get('ultimo_id', None)
        dados = {'error': None, 'error_message': None}
        ofertas = ultimo_id = None
        if not slug and not id_multiplan:
            dados.update({'error': 'Shopping não informado',
                          'error_message': 'Favor informe a slug do shopping ou id do shopping na '
                                           'Multiplan'})
        elif id_multiplan or slug:
            usuario = kwargs.get('usuario', None)
            ids_do_usuario = [int(s.id_multiplan) for s in usuario.shopping.all()]
            slugs_do_usuario = [s.slug for s in usuario.shopping.all()]
            tem_acesso = True

            if id_multiplan and id_multiplan not in ids_do_usuario:
                tem_acesso = False
            if slug and slug not in slugs_do_usuario:
                tem_acesso = False

            if not tem_acesso:
                dados.update({'error': 'Sem acesso ao shopping',
                              'error_message': 'Sua perfil não tem acesso a dados desse shopping'})

                return retorno(dados, tipo)
        elif id_multiplan:
            if from_id:
                ofertas, ultimo_id = Oferta.prontos_api(id_multiplan=id_multiplan,from_id=from_id)
            else:
                ofertas, ultimo_id = Oferta.prontos_api(id_multiplan=id_multiplan)
        else:
            shopping = Shopping.objects.get(slug=slug)
            ofertas, ultimo_id = Oferta.prontos_api(id_multiplan=shopping.id_multiplan)

        dados.update({'ofertas': ofertas, 'ultimo_id': ultimo_id})
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