# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse

from utils.functions import jsonResponse

from geral.models import Categoria, ImagemOferta, Oferta, Log
from lojas.models import Loja


def slice_oferta(total_destaques, total_eventos):
    total_destaques = total_destaques * 4
    total_eventos = total_eventos * 2
    return 32 - total_destaques - total_eventos

def ultimo_id(lista):
    ultimo_id = 0
    for i in lista:
        if i['id'] > ultimo_id:
            ultimo_id = int(i['id'])
    return ultimo_id if ultimo_id > 0 else ''

def home(request):
    destaques = Oferta.prontos(tipo=Oferta.DESTAQUE)

    eventos = Oferta.prontos(tipo=Oferta.EVENTO)

    ofertas = Oferta.prontos()
    ofertas = ofertas[:slice_oferta(len(destaques),len(eventos))]

    contexto = {'lojas': Loja.objects.all(),
                'destaques': destaques,
                'ultimo_destaque_id': ultimo_id(destaques),
                'eventos': eventos,
                'ultimo_evento_id': ultimo_id(eventos),
                'ofertas': ofertas,
                'ultima_oferta_id': ultimo_id(ofertas)}
    return render(request, "home.html", contexto)

@csrf_exempt
def mais_ofertas(request):
    ultimo_destaque = request.POST.get('ultimo_destaque', None)
    ultimo_evento = request.POST.get('ultimo_evento', None)
    ultima_oferta = request.POST.get('ultima_oferta', None)

    if not all([ultimo_destaque,ultimo_evento,ultima_oferta]):
        contexto = {}
    else:
        destaques = Oferta.prontos(tipo=Oferta.DESTAQUE, from_id=ultimo_destaque)

        eventos = Oferta.prontos(tipo=Oferta.EVENTO, from_id=ultimo_evento)

        ofertas = Oferta.prontos(from_id=ultima_oferta)
        ofertas = ofertas[:slice_oferta(len(destaques),len(eventos))]

        contexto = {'lojas': Loja.objects.all(),
                    'destaques': destaques,
                    'ultimo_destaque_id': ultimo_id(destaques),
                    'eventos': eventos,
                    'ultimo_evento_id': ultimo_id(eventos),
                    'ofertas': ofertas,
                    'ultima_oferta_id': ultimo_id(ofertas)}

    return render(request, "home-part.html", contexto)

def modal(request, tipo, id_item):
    contexto = {}
    if not tipo in ['oferta','destaque','evento']:
        raise Http404

    nome_template = "modais/%s.html" % tipo

    item = Oferta.objects.get_or_none(id=id_item)
    if item:
        Log.regitra_acao(item, Log.CLIQUE)
        contexto[tipo] = item.to_dict(modal=True)

    if not contexto:
        raise Http404

    return render(request, nome_template, contexto)

@csrf_exempt
def curtir(request):
    id_item = request.POST.get('id_item')
    if not id_item and not request.is_ajax():
        raise Http404

    item = Oferta.objects.get(id=id_item)
    Log.objects.create(acao=Log.CURTIDA,oferta=item)

    return jsonResponse({'total': item.total_curtido})
