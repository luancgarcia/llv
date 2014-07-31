# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from geral.models import Categoria, ImagemOferta, Oferta, Log
from lojas.models import Loja

def home(request):
    contexto = {'lojas': Loja.objects.all()}
    return render(request, "home.html", contexto)

def modal(request):
    return