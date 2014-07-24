# -*- encoding: utf-8 -*-

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt

from geral.models import Categoria, ImagemOferta, Oferta, Log


def home(request):
    return render(request, "home.html", {})

def modal(request):
    return