# -*- encoding: utf-8 -*-

import os
from PIL import Image

from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404, HttpResponse
from django.conf import settings

from utils.functions import jsonResponse

from geral.models import Categoria, ImagemOferta, Oferta, Log, Mascara, Sazonal
from lojas.models import Loja


def slice_oferta(total_destaques=0, total_eventos=0):
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

    mais_paginas = True if len(ofertas) > 14 else False

    contexto = {'destaques': destaques,
                'ultimo_destaque_id': [int(d['id']) for d in destaques],
                'eventos': eventos,
                'ultimo_evento_id': [int(e['id']) for e in eventos],
                'ofertas': ofertas,
                'ultima_oferta_id': [int(o['id']) for o in ofertas],
                'categorias': Categoria.publicadas_com_oferta(),
                'mais_paginas': mais_paginas,
                'lojas': Loja.publicadas_com_oferta(),
                'lojas_splash': Loja.publicadas_sem_oferta(),
                'sazonal': Sazonal.atual()}
    return render(request, "home.html", contexto)

def home_com_filtro(request, *args, **kwargs):
    tipo = kwargs.keys()[0]
    slug = kwargs.get(tipo)

    if tipo == 'categoria':
        destaques, ofertas, eventos = home_por_categoria(slug)
    elif tipo == 'genero':
        destaques, ofertas, eventos = home_por_genero(slug)
    elif tipo == 'loja':
        destaques, ofertas, eventos = home_por_loja(slug)
    elif tipo == 'preco':
        destaques, ofertas, eventos = home_por_preco(slug)
    else:
        destaques, ofertas, eventos = home_por_desconto(slug)

    mais_paginas = True if len(ofertas) > 14 else False

    contexto = {'destaques': destaques,
                'ultimo_destaque_id': [int(d['id']) for d in destaques],
                'eventos': eventos,
                'ultimo_evento_id': [int(e['id']) for e in eventos],
                'ofertas': ofertas,
                'ultima_oferta_id': [int(o['id']) for o in ofertas],
                'categorias': Categoria.publicadas_com_oferta(),
                'mais_paginas': mais_paginas,
                'lojas': Loja.publicadas_com_oferta(),
                'lojas_splash': Loja.publicadas_sem_oferta()}
    return render(request, "home.html", contexto)

def destaques_ofertas_eventos(items):
    destaques = items.filter(tipo=Oferta.DESTAQUE)
    destaques = [d.to_dict() for d in destaques]

    eventos = items.filter(tipo=Oferta.EVENTO)
    eventos = [e.to_dict() for e in eventos]

    ofertas = items.filter(tipo=Oferta.OFERTA)
    ofertas = [o.to_dict() for o in ofertas]
    ofertas = ofertas[:slice_oferta(len(destaques),len(eventos))]

    return destaques, ofertas, eventos

def home_por_categoria(slug):
    categoria = Categoria.objects.filter(slug=slug,shopping_id=1).get()
    items = Oferta.objects.filter(status=Oferta.PUBLICADO,
                                  categoria=categoria)
    return destaques_ofertas_eventos(items)

def categoria(request, categoria):
    categoria = Categoria.objects.filter(slug=categoria,shopping_id=1).get()
    items = Oferta.objects.filter(status=Oferta.PUBLICADO,
                                  categoria=categoria)
    destaques, ofertas, eventos = destaques_ofertas_eventos(items)
    mais_paginas = True if len(ofertas) > 14 else False

    contexto = {'destaques': destaques,
                'ultimo_destaque_id': [int(d['id']) for d in destaques],
                'eventos': eventos,
                'ultimo_evento_id': [int(e['id']) for e in eventos],
                'ofertas': ofertas,
                'ultima_oferta_id': [int(o['id']) for o in ofertas],
                'categorias': Categoria.publicadas_com_oferta(),
                'mais_paginas': mais_paginas,
                'lojas': Loja.publicadas_com_oferta(),
                'lojas_splash': Loja.publicadas_sem_oferta()}
    return render(request, "home.html", contexto)

def home_por_genero(slug):
    if slug == 'masculino':
        genero = 0
    elif slug == 'feminino':
        genero = 1
    elif slug == 'infantil':
        genero = 2
    else:
        genero = 3

    items = Oferta.objects.filter(status=Oferta.PUBLICADO,
                                  genero=genero)
    return destaques_ofertas_eventos(items)

def home_por_loja(id_loja):
    loja = Loja.objects.filter(id=id_loja).get()
    items = Oferta.objects.filter(status=Oferta.PUBLICADO,
                                  loja=loja)
    return destaques_ofertas_eventos(items)

def home_por_preco(preco):
    items = Oferta.objects.filter(status=Oferta.PUBLICADO)
    if preco == '301':
        items.filter(preco_final__gte='301')
    elif preco == '300':
        items.filter(preco_final__lte='300',preco_final__gte='101')
    elif preco == '100':
        items.filter(preco_final__lte='100',preco_final__gte='51')
    elif preco == '50':
        item.filter(preco_final__lte='50',preco_final__gte='31')
    else:
        items.filter(preco_final__lte='30')

    return destaques_ofertas_eventos(items)

def home_por_desconto(porcentagem):
    items = Oferta.objects.filter(status=Oferta.PUBLICADO)
    if porcentagem == '30':
        items.filter(desconto__lte='30')
    elif porcentagem == '50':
        items.filter(desconto__gte='31',desconto__lte='50')
    else:
        items.filter(desconto__gte='51',desconto__lte='70')

    return destaques_ofertas_eventos(items)

@csrf_exempt
def mais_ofertas(request):
    ultimo_destaque = request.POST.get('ultimo_destaque', None)
    ultimo_evento = request.POST.get('ultimo_evento', None)
    ultima_oferta = request.POST.get('ultima_oferta', None)

    destaques = eventos = ofertas = []
    total_destaques = total_eventos = 0
    if ultimo_destaque:
        ids_destaques = [int(i) for i in ultimo_destaque.split(', ')]
        destaques = Oferta.objects.filter(tipo=Oferta.DESTAQUE,
                                          status=Oferta.PUBLICADO)\
                                  .exclude(id__in=ids_destaques)
        total_destaques = len(destaques)
    if ultimo_evento:
        ids_eventos = [int(i) for i in ultimo_evento.split(', ')]
        eventos = Oferta.objects.filter(tipo=Oferta.EVENTO,
                                        status=Oferta.PUBLICADO)\
                                .exclude(id__in=ids_eventos)
        total_eventos = len(eventos)
    if ultima_oferta:
        ids_ofertas = [int(i) for i in ultima_oferta.split(', ')]
        ofertas = Oferta.objects.filter(tipo=Oferta.OFERTA,
                                        status=Oferta.PUBLICADO)\
                                .exclude(id__in=ids_ofertas)
        ofertas = [o.to_dict() for o in ofertas]
        if total_destaques or total_eventos:
            ofertas = ofertas[:slice_oferta(len(destaques),len(eventos))]

    mais_paginas = True
    if not ofertas or len(ofertas) < 14:
        mais_paginas = False

    contexto = {'destaques': destaques,
                'ultimo_destaque_id': [int(d['id']) for d in ofertas],
                'eventos': eventos,
                'ultimo_evento_id': [int(e['id']) for e in eventos],
                'ofertas': ofertas,
                'ultima_oferta_id': [int(o['id']) for o in ofertas],
                'mais_paginas': mais_paginas}

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

    if not imagem_id and not mascara_id:
        raise Http404

    item = imagem = mascara= None
    if id_item:
        item = Oferta.objects.get(id=id_item)
    if imagem_id:
        imagem = ImagemOferta.objects.get(id=imagem_id)
    if mascara_id:
        mascara = Mascara.objects.get(id=mascara_id)

    if not item or not imagem:
        raise Http404

    if imagem and mascara:
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
    else:
        destino_url = imagem.img_376x376.url

    item_dict = item.to_dict(modal=True)
    contexto = {'titulo': item_dict['titulo'],
                'descricao': item_dict['chamada_promocional'],
                'imagem': destino_url}

    Log.regitra_acao(item,Log.COMPARTILHADA)

    return jsonResponse(contexto)
