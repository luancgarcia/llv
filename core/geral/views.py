# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

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
                'eventos': eventos,
                'ofertas': ofertas}
    return render(request, "home.html", contexto)

def modal(request):
    return