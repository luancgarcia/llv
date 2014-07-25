# -*- encoding: utf-8 -*-

from django.shortcuts import render


def html_grid(request):
    return render(request, 'grid.html', {})

def html_home(request):
    return render(request, 'home.html', {})

def html_modal_produtos(request):
    return render(request, 'modais/produto.html')

def html_modal_destaque(request):
    return render(request, 'modais/destaque.html')

def html_modal_evento(request):
    return render(request, 'modais/evento.html')

def html_modal_share(request):
    return render(request, 'modais/share.html')