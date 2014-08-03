# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse

from geral.models import Categoria, ImagemOferta, Oferta, Log
from lojas.models import Loja


def slice_oferta(total_destaques, total_eventos):
    total_destaques = total_destaques * 4
    total_eventos = total_eventos * 2
    return 32 - total_destaques - total_eventos

def home(request):
    destaques = Oferta.destaques_prontos()
    eventos = Oferta.eventos_prontos()

    ofertas = Oferta.ofertas_prontas()
    ofertas = ofertas[:slice_oferta(len(destaques),len(eventos))]


    contexto = {'lojas': Loja.objects.all(),
                'destaques': destaques,
                'ultimo_destaque_id': destaques[::-1][0]['id'],
                'eventos': eventos,
                'ultimo_evento_id': eventos[::-1][0]['id'],
                'ofertas': ofertas,
                'ultima_oferta_id': ofertas[::-1][0]['id']}
    return render(request, "home.html", contexto)

@csrf_exempt
def mais_ofertas(request):
    ultimo_destaque = request.POST.get('ultimo_destaque')
    ultimo_evento = request.GET.get('ultimo_evento')
    ultima_oferta = request.GET.get('ultima_oferta')
    if not any([ultimo_destaque,ultimo_evento,ultima_oferta]):
        raise Http404
    return

def modal(request, tipo, id_item):
    return
