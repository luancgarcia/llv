# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from models import Intervalo, Ponto
from lojas.models import Shopping

@staff_member_required
def ranking_index(request):
    dados = []
    intervalo = Intervalo.objects.latest('id')
    for s in Shopping.objects.all():
        pontos = Ponto.dez_mais(s.id, intervalo.id)
        dados.append({'nome': s.nome,
                      'lojas': [p.to_dict() for p in pontos]})

    return render(request, "geral.html", {'shoppings': dados, 'intervalo': intervalo})
