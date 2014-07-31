# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from geral.models import Categoria, ImagemOferta, Oferta, Log
from lojas.models import Loja

def home(request):
    destaques = Oferta.destaques_prontos()
    eventos = Oferta.eventos_prontos()
    total_destaques = len(destaques)
    total_eventos = len(eventos)

    contexto = {'lojas': Loja.objects.all(),
                'destaques': destaques,
                'eventos': eventos,
                'ofertas': Oferta.ofertas_prontas()}
    return render(request, "home.html", contexto)

def modal(request):
    return