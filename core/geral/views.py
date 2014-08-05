# -*- encoding: utf-8 -*-

import os
from PIL import Image

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse
from django.conf import settings

from utils.functions import jsonResponse

from geral.models import Categoria, ImagemOferta, Oferta, Log, Mascara
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

@csrf_exempt
def modal_share(request, id_item):
    if not request.is_ajax():
        raise Http404

    item = Oferta.objects.get(id=id_item)
    imagem = item.imagens.all()[:1].get()
    contexto = {'item': item.to_dict(modal=True),
                'imagem_url': imagem.img_376x376.url,
                'imagem_id': imagem.id,
                'mascaras': Mascara.serializado()}

    return render(request, "modais/share.html", contexto)

@csrf_exempt
def mesclar(request):
    imagem_id = request.POST.get('imagem_id', None)
    mascara_id = request.POST.get('mascara_id', None)
    id_item = request.POST.get('id_item', None)

    if not all([imagem_id,mascara_id,id_item]):
        raise Http404

    item = Oferta.objects.get(id=id_item)
    imagem = ImagemOferta.objects.get(id=imagem_id)
    mascara = Mascara.objects.get(id=mascara_id)

    background_arquivo = '%s%s' % (settings.PROJECT_DIR, imagem.img_376x376.url)
    background = Image.open(background_arquivo)
    foreground_arquivo = '%s%s' % (settings.PROJECT_DIR, mascara.img_376x376.url)
    foreground = Image.open(foreground_arquivo)
    background.paste(foreground, (0, 0), foreground)

    arquivo = '%s_%s_%s.png' % (id_item, imagem_id, mascara_id)
    destino = os.path.join(settings.COMPARTILHADAS_PASTA, arquivo)
    destino_url = '%s%s' % (settings.COMPARTILHADAS_URL, arquivo)

    try:
        background.save(destino)
    except Exception, e:
        raise e

    item_dict = item.to_dict(modal=True)
    contexto = {'titulo': item_dict['titulo'],
                'descricao': item_dict['chamada_promocional'],
                'imagem': destino_url}

    Log.regitra_acao(item,Log.COMPARTILHADA)

    return jsonResponse(contexto)
