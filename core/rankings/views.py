# -*- encoding: utf-8 -*-
from django.shortcuts import render
from django.contrib.admin.views.decorators import staff_member_required

from models import Ponto
from lojas.models import Shopping

@staff_member_required
def ranking_index(request):
    dados = []
    for s in Shopping.objects.all():
        dados.append({'nome': s.nome,
                      'lojas': [p.to_dict() for p in Ponto.dez_mais(s.id)]})

    return render(request, "geral.html", {'shoppings': dados})
