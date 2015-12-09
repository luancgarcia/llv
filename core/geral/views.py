# -*- encoding: utf-8 -*-

import os
from PIL import Image, ImageDraw, ImageFont
from datetime import date, timedelta, datetime
from collections import OrderedDict

from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.http import Http404
from django.core.cache import cache
from django.conf import settings
from django.db.models import Q
from aggregate_if import Count
from django.contrib.admin.views.decorators import staff_member_required

from utils.functions import jsonResponse, dict_mais_vistas, listas_e_totais
from utils.custom_email import TemplatedEmail

from geral.models import (Categoria, ImagemOferta, Oferta, Log, Mascara,
                          Sazonal, Perfil)
from .decorators import indica_shopping
from lojas.models import Loja, Shopping
from notificacoes.models import Solicitacao


def index(request):
    return render(request, "index.html", {})

def modal_fb_login(request):
    return render(request, "modais/modal_fb_login.html", {})

def modal_fb_login_chrome_ios(request):
    return render(request, "modais/modal_fb_login_crhome_ios.html", {})

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

def contexto_home(destaques, eventos, ofertas, mais_paginas, shopping, com_filtro=False):
    trinta = tem_trinta = tem_cinq = cinquenta = tem_setenta = setenta \
    = preco1 = tem_preco1 = preco2 = tem_preco2 = preco3 = tem_preco3 = preco4 \
        = tem_preco4 = preco5 = tem_preco5 = False
    generos = []

    if com_filtro:
        destaques_x = Oferta.prontos(tipo=Oferta.DESTAQUE, shopping=shopping.id)
        eventos_x = Oferta.prontos(tipo=Oferta.EVENTO, shopping=shopping.id)
        ofertas_x = Oferta.prontos(shopping=shopping.id)
        ofertas_x = ofertas_x[:slice_oferta(len(destaques_x), len(eventos_x))]
    else:
        destaques_x = destaques
        eventos_x = eventos
        ofertas_x = ofertas

    lojas_dict = {}
    for i in Oferta.itens_por_shopping(shopping=shopping.id):
        if i.genero and Oferta.GENEROS[i.genero][1].lower() not in generos:
            generos.append(Oferta.GENEROS[i.genero][1])
        desconto = int(i.desconto) if i.desconto else None
        if desconto:
            if not tem_trinta and desconto <= 30:
                trinta = tem_trinta = True
            if not tem_cinq and desconto > 30 and desconto <= 50:
                cinquenta = tem_cinq = True
            if not tem_setenta and desconto > 50:
                setenta = tem_setenta = True

        preco = int(i.preco_final) if i.preco_final else None
        if preco:
            if not tem_preco1 and preco <= 30:
                preco1 = tem_preco1 = True
            if not tem_preco2 and preco > 30 and preco <= 50:
                preco2 = tem_preco2 = True
            if not tem_preco3 and preco > 50 and preco <= 100:
                preco3 = tem_preco3 = True
            if not tem_preco4 and preco > 100 and preco <= 300:
                preco4 = tem_preco4 = True
            if not tem_preco5 and preco > 300:
                preco5 = tem_preco5 = True
        if i.loja:
            lojas_dict[i.loja.slug] = i.loja.nome
    #for i in destaques_x+eventos_x+ofertas_x:
    #    if i.get('genero', None) and i['genero'].lower() not in generos:
    #        generos.append(i['genero'])
    #    desconto = int(i['desconto']) if i.get('desconto', None) else None
    #    if desconto:
    #        if not tem_trinta and desconto <= 30:
    #            trinta = tem_trinta = True
    #        if not tem_cinq and desconto > 30 and desconto <= 50:
    #            cinquenta = tem_cinq = True
    #        if not tem_setenta and desconto > 50:
    #            setenta = tem_setenta = True
    #    if i.get('loja', None):
    #        lojas_dict[i['loja']['slug']] = i['loja']['nome'] 
    #    preco = int(i['preco_final']) if i.get('preco_final', None) else None
    #    if preco:
    #        if not tem_preco1 and preco <= 30:
    #            preco1 = tem_preco1 = True
    #        if not tem_preco2 and preco > 30 and preco <= 50:
    #            preco2 = tem_preco2 = True
    #        if not tem_preco3 and preco > 50 and preco <= 100:
    #            preco3 = tem_preco3 = True
    #        if not tem_preco4 and preco > 100 and preco <= 300:
    #            preco4 = tem_preco4 = True
    #        if not tem_preco5 and preco > 300:
    #            preco5 = tem_preco5 = True

    return {'destaques': destaques,
            'ultimo_destaque_id': [int(d['id']) for d in destaques],
            'eventos': eventos,
            'ultimo_evento_id': [int(e['id']) for e in eventos],
            'ofertas': ofertas,
            'ultima_oferta_id': [int(o['id']) for o in ofertas],
            'categorias': Categoria.publicadas_com_oferta(shopping.id),
            'mais_paginas': mais_paginas,
            #'lojas': Loja.publicadas_com_oferta(shopping=shopping.id),
            'lojas_dict': OrderedDict(sorted(lojas_dict.items(), key=lambda n: n[1])),
            'lojas_splash': Loja.publicadas_sem_oferta(shopping=shopping.id),
            'sazonal': Sazonal.atual(shopping=shopping.id),
            'shopping_id': shopping.id,
            'shopping_slug': shopping.slug,
            'shopping_nome': shopping.nome,
            'generos': set(generos),
            'trinta': trinta,
            'cinquenta': cinquenta,
            'setenta': setenta,
            'preco1': preco1,
            'preco2': preco2,
            'preco3': preco3,
            'preco4': preco4,
            'preco5': preco5}

@indica_shopping
def home(request, **kwargs):
    shopping = Shopping.objects.get(slug=kwargs['slug'])
    destaques = Oferta.prontos(tipo=Oferta.DESTAQUE, shopping=shopping.id)

    eventos = Oferta.prontos(tipo=Oferta.EVENTO, shopping=shopping.id)

    ofertas = Oferta.prontos(shopping=shopping.id)
    mais_paginas = True if len(ofertas) > 14 else False
    ofertas = ofertas[:slice_oferta(len(destaques),len(eventos))]

    contexto = contexto_home(destaques,eventos,ofertas,mais_paginas,shopping)

    response = render(request, "home.html", contexto)
    response.set_cookie(key='shp_id', value=shopping.id)

    return response

def split_ids(valores):
    if valores:
        return [int(''.join(i.split('.'))) for i in valores.split(', ')]
    return []

@indica_shopping
def home_com_filtro(request, **kwargs):
    shopping = Shopping.objects.get(slug=kwargs['slug'])
    template = "home.html"
    ids_filtrar = []
    destaque_ids = evento_ids = oferta_ids = []
    if request.GET.get('mais_ofertas'):
        destaque_ids = split_ids(request.POST.get('ultimo_destaque', None))
        evento_ids = split_ids(request.POST.get('ultimo_evento', None))
        oferta_ids = split_ids(request.POST.get('ultima_oferta', None))
        ids_filtrar = destaque_ids+evento_ids+oferta_ids
        template = "home-part.html"


    if kwargs.get('categoria'):
        slug = kwargs.get('categoria')
        destaques, ofertas, eventos, mais_paginas = home_por_categoria(slug,
                                                                       shopping.id,
                                                                       ids_filtrar)
    elif kwargs.get('genero'):
        slug = kwargs.get('genero')
        destaques, ofertas, eventos, mais_paginas = home_por_genero(slug,
                                                                    shopping.id,
                                                                    ids_filtrar)
    elif kwargs.get('loja'):
        slug = kwargs.get('loja')
        destaques, ofertas, eventos, mais_paginas = home_por_loja(slug,
                                                                  shopping.id,
                                                                  ids_filtrar)
    elif kwargs.get('preco'):
        slug = kwargs.get('preco')
        destaques, ofertas, eventos, mais_paginas = home_por_preco(slug,
                                                                   shopping.id,
                                                                   ids_filtrar)
    else:
        slug = kwargs.get('desconto')
        destaques, ofertas, eventos, mais_paginas = home_por_desconto(slug,
                                                                      shopping.id,
                                                                      ids_filtrar)

    if request.GET.get('mais_ofertas'):
        ids_destaques = destaque_ids+[d['id'] for d in destaques]
        ids_eventos = evento_ids+[e['id'] for e in eventos]
        ids_ofertas = oferta_ids+[o['id'] for o in ofertas]
        contexto = {'destaques': destaques,
                    'ultimo_destaque_id': ids_destaques,
                    'eventos': eventos,
                    'ultimo_evento_id': ids_eventos,
                    'ofertas': ofertas,
                    'ultima_oferta_id': ids_ofertas,
                    'mais_paginas': mais_paginas,
                    'eh_paginacao': True}
    else:
        contexto = contexto_home(destaques,eventos,ofertas,mais_paginas,shopping,com_filtro=True)
    contexto.update({'data_filtro': 1})

    response = render(request, template, contexto)
    response.set_cookie(key='shp_id', value=shopping.id)

    return response

def destaques_ofertas_eventos(items):
    destaques = items.filter(tipo=Oferta.DESTAQUE)
    destaques = [d.to_dict() for d in destaques]

    eventos = items.filter(tipo=Oferta.EVENTO)
    eventos = [e.to_dict() for e in eventos]

    ofertas = items.filter(tipo=Oferta.OFERTA)
    ofertas = [o.to_dict() for o in ofertas]
    mais_paginas = True if len(ofertas) > 14 else False
    ofertas = ofertas[:slice_oferta(len(destaques),len(eventos))]

    return destaques, ofertas, eventos, mais_paginas

def home_por_categoria(slug, shopping, ids_filtrar):
    categoria = Categoria.objects.filter(slug=slug,shopping_id=shopping).get()
    hoje = date.today()
    items = Oferta.objects.filter(status=Oferta.PUBLICADO,
                                  categoria=categoria,
                                  loja__shopping_id=shopping) \
                          .filter(inicio__lte=hoje,fim__gte=hoje) \
                          .exclude(id__in=ids_filtrar) \
                          .order_by('-data_aprovacao')
    return destaques_ofertas_eventos(items)

def categoria(request, categoria):
    categoria = Categoria.objects.filter(slug=categoria).get()
    hoje = date.today()
    items = Oferta.objects.filter(status=Oferta.PUBLICADO, categoria=categoria)\
                          .filter(inicio__lte=hoje,fim__gte=hoje)
    destaques, ofertas, eventos, mais_paginas = destaques_ofertas_eventos(items)

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

def home_por_genero(slug, shopping, ids_filtrar):
    if slug == 'masculino':
        genero = 0
    elif slug == 'feminino':
        genero = 1
    elif slug == 'infantil':
        genero = 2
    else:
        genero = 3
    hoje = date.today()
    items = Oferta.objects.filter(status=Oferta.PUBLICADO,
                                  genero=genero,
                                  loja__shopping_id=shopping) \
                          .filter(inicio__lte=hoje,fim__gte=hoje) \
                          .exclude(id__in=ids_filtrar) \
                          .order_by('-data_aprovacao')
    return destaques_ofertas_eventos(items)

def home_por_loja(slug, shopping, ids_filtrar):
    hoje = date.today()
    loja = Loja.objects.filter(slug=slug,shopping_id=shopping).get()
    items = Oferta.objects.filter(status=Oferta.PUBLICADO,
                                  loja=loja).exclude(id__in=ids_filtrar) \
                          .filter(inicio__lte=hoje,fim__gte=hoje) \
                          .order_by('-data_aprovacao')

    return destaques_ofertas_eventos(items)

def home_por_preco(preco, shopping, ids_filtrar):
    hoje = date.today()
    items = Oferta.objects.filter(status=Oferta.PUBLICADO,
                                  loja__shopping_id=shopping) \
                          .filter(inicio__lte=hoje,fim__gte=hoje) \
                          .order_by('-data_aprovacao')
    if preco == '301':
        items = items.filter(preco_final__gte='301')
    elif preco == '300':
        items = items.filter(preco_final__lte='300',preco_final__gte='101')
    elif preco == '100':
        items = items.filter(preco_final__lte='100',preco_final__gte='51')
    elif preco == '50':
        items = items.filter(preco_final__lte='50',preco_final__gte='31')
    else:
        items = items.filter(preco_final__lte='30')

    if ids_filtrar:
        items = items.exclude(id__in=ids_filtrar)

    return destaques_ofertas_eventos(items)

def home_por_desconto(porcentagem, shopping, ids_filtrar):
    hoje = date.today()
    items = Oferta.objects.filter(status=Oferta.PUBLICADO,
                                  loja__shopping_id=shopping) \
                          .filter(inicio__lte=hoje,fim__gte=hoje) \
                          .order_by('-data_aprovacao')

    porcentagem = int(porcentagem)
    if porcentagem == 30:
        items = items.filter(desconto__lte=30)
    elif porcentagem == 50:
        items = items.filter(desconto__gte=31,desconto__lte=50)
    else:
        items = items.filter(desconto__gte=51,desconto__lte=70)

    if ids_filtrar:
        items = items.exclude(id__in=ids_filtrar)

    return destaques_ofertas_eventos(items)

def mais_items(ids_para_filtrar, tipo, id_shopping):
    hoje = date.today()
    if tipo == Oferta.OFERTA:
        corte = 32
    else:
        corte = 3

    # cache_key = 'MAIS_%s_%s_%s' % (id_shopping, tipo, ''.join(map(str, ids_para_filtrar)))
    # cache_mais = cache.get(cache_key)

    # if cache_mais:
    #     return cache_mais
    # else:
    items = Oferta.objects.filter(loja__shopping_id=id_shopping,
                                  tipo=tipo,
                                  status=Oferta.PUBLICADO,
                                  inicio__lte=hoje, fim__gte=hoje) \
                           .exclude(id__in=ids_para_filtrar) \
                           .order_by('-data_aprovacao')[:corte]
        # items = Oferta.objects.filter(tipo=tipo,status=Oferta.PUBLICADO)\
        #                       .filter(Q(loja__shopping_id=id_shopping) |
        #                               Q(shopping_id=id_shopping)) \
        #                       .filter(inicio__lte=hoje,fim__gte=hoje) \
        #                       .exclude(id__in=ids_para_filtrar) \
        #                       .order_by('-data_aprovacao')[:corte]
        # items_final = []
        # for i in items:
        #     items_final.append(i.to_dict())
        # cache.set(cache_key, items_final)
    items_final = [i.to_dict() for i in items]
    return items_final

def limpa_ids(valores):
    ids = []
    for i in valores.split(', '):
        limpa = i.replace('.','')
        if limpa:
	    try:
		id_inteiro = int(limpa)
		ids.append(id_inteiro)
	    except:
		pass
    #return [int(''.join(i.split('.'))) for i in valores.split(', ')]
    #return ids
    return [ int(float(i.replace('.',''))) for i in valores.split(', ')]
@csrf_exempt
def mais_ofertas(request):
    ultimo_destaque = request.POST.get('ultimo_destaque', None)
    ultimo_evento = request.POST.get('ultimo_evento', None)
    ultima_oferta = request.POST.get('ultima_oferta', None)
    id_shopping_cookie = request.COOKIES.get('shp_id', None)
    id_shopping = request.POST.get('shopping_id', id_shopping_cookie)

    destaques = eventos = ofertas = ultimo_destaque_id = ultimo_evento_id = ultima_oferta_id = []
    total_destaques = total_eventos = 0
    mais_paginas = False
    if ultimo_destaque:
        ultimo_destaque = limpa_ids(ultimo_destaque)
        destaques = mais_items(ultimo_destaque, Oferta.DESTAQUE, id_shopping)
        ultimo_destaque_id = ultimo_destaque + [int(d['id']) for d in destaques]
        total_destaques = len(destaques)
    if ultimo_evento:
        ultimo_evento = limpa_ids(ultimo_evento)
        eventos = mais_items(ultimo_evento, Oferta.EVENTO, id_shopping)
        ultimo_evento_id = ultimo_evento + [int(e['id']) for e in eventos]
        total_eventos = len(eventos)
    if ultima_oferta:
        ultima_oferta = limpa_ids(ultima_oferta)
        ofertas = mais_items(ultima_oferta, Oferta.OFERTA, id_shopping)
        if len(ofertas) > 14:
            mais_paginas = True
        if total_destaques or total_eventos:
            ofertas = ofertas[:slice_oferta(len(destaques),len(eventos))]
        ultima_oferta_id = ultima_oferta + [int(o['id']) for o in ofertas]

    contexto = {'destaques': destaques,
                'ultimo_destaque_id': ultimo_destaque_id,
                'eventos': eventos,
                'ultimo_evento_id': ultimo_evento_id,
                'ofertas': ofertas,
                'ultima_oferta_id': ultima_oferta_id,
                'mais_paginas': mais_paginas,
                'eh_paginacao': True,
                'shopping_id': id_shopping}

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

def modal_slug(request, tipo, slug_item):
    contexto = {}
    print tipo, slug_item
    if not tipo in ['oferta','destaque','evento']:
        raise Http404

    nome_template = "modais/%s.html" % tipo

    item = Oferta.objects.get_or_none(slug=slug_item)
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

    id_item = ''.join(id_item.split('.'))
    item = Oferta.objects.get(id=id_item)
    Log.objects.create(acao=Log.CURTIDA,oferta=item)

    arquivo = '%s_curtir.png' % id_item
    destino = os.path.join(settings.COMPARTILHADAS_PASTA, arquivo)
    destino_url = '%s%s' % (settings.COMPARTILHADAS_URL, arquivo)

    if not os.path.isfile(destino):
        img_oferta = ImagemOferta.objects.filter(oferta=item)[0]
        imagem = Image.open('%s' % img_oferta.img_120x120.path)
        base = Image.new('RGBA', (450, 120), (247, 247, 247))
        base.paste(imagem, (0,0), imagem)
        fonte = ImageFont.truetype(settings.FONTE_SHARE, 15)
        fonte_chamada = ImageFont.truetype(settings.FONTE_SHARE, 12)
        draw = ImageDraw.Draw(base)
        draw = draw.text((130,10), item.nome[:40], font=fonte,
                         fill=(45, 78, 157))
        draw = ImageDraw.Draw(base)
        if item.texto_promocional:
            descricao = item.texto_promocional[:40]
        else:
            descricao = item.descricao[:40]
        draw = draw.text((130,35), descricao, font=fonte_chamada,
                         fill=(128, 128, 128))
        draw = ImageDraw.Draw(base)

        try:
            base.save(destino)
        except Exception, e:
            raise e

    mensagem = u'Acabei de curtir uma oferta do Lápis Vermelho'
    mensagem += '\r\n\r\n\r\n\r\n %s' % item.url
    mensagem += '\r\n\r\n\r\n\r\n #LapisVermelho'

    return jsonResponse({'total': item.total_curtido,
                         'imagem': destino_url,
                         'mensagem': mensagem})

@csrf_exempt
def descurtir(request):
    id_item = request.POST.get('id_item')
    total = int(request.POST.get('total_atual'))
    if not id_item and not request.is_ajax():
        raise Http404

    ultimo = Log.objects.filter(acao=Log.CURTIDA,oferta_id=id_item).latest('id')
    if ultimo:
        ultimo.delete()
        total = total - 1

    return jsonResponse({'total': total})

@csrf_exempt
def modal_share(request, id_item):
    if not request.is_ajax():
        raise Http404

    item = Oferta.objects.get(id=id_item)
    imagem = item.imagens.all()[:1].get()
    sazonal = Sazonal.atual(serializado=False)
    imagens_sazonal = []
    if sazonal:
        imagens_sazonal = [m.to_dict() for m in sazonal.mascaras.all()]
    contexto = {'item': item.to_dict(modal=True),
                'imagem_url': imagem.img_376x376.url,
                'imagem_id': imagem.id,
                'mascaras': Mascara.normais_serializadas(),
                'sazonal': sazonal.to_dict() if sazonal else None,
                'imagens_sazonal': imagens_sazonal}

    return render(request, "modais/share.html", contexto)

@csrf_exempt
def mesclar(request):
    imagem_id = request.POST.get('imagem_id', None)
    mascara_id = request.POST.get('mascara_id', None)
    id_item = request.POST.get('id_item', None)
    if not imagem_id and not mascara_id:
        raise Http404
    id_item = ''.join(id_item.split('.'))
    imagem_id = ''.join(imagem_id.split('.'))
    mascara_id = ''.join(mascara_id.split('.'))

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
        background_arquivo = '%s' % imagem.img_250x250.path
        background = Image.open(background_arquivo)
        foreground_arquivo = '%s' % mascara.img_250x250.path
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
        destino_url = '%s' % imagem.img_376x376.url

    item_dict = item.to_dict(modal=True)
    nome_shopping = item.loja.shopping.nome if item.loja else item.shopping.nome
    nome_loja = item.loja.nome if item.loja else ""
    nome_loja = nome_loja.replace(" ","")
    nome_shopping = nome_shopping.replace(" ","")

    quebra_linha = '\r\n\r\n\r\n\r\n'
    if nome_shopping and nome_loja:
        hashtags = '#LapisVermelho #%s #%s' % (nome_shopping, nome_loja)
    elif nome_shopping and not nome_loja:
        hashtags = '#LapisVermelho #%s' % nome_shopping
    elif not nome_shopping and nome_loja:
        hashtags = '#LapisVermelho #%s' % nome_loja
    else:
        hashtags = '#LapisVermelho'
    mensagem = '%s%s%s%s%s%s%s' % (item_dict['titulo'],
                                   quebra_linha,
                                   item_dict['descricao'],
                                   quebra_linha,
                                   hashtags,
                                   quebra_linha,
                                   item.url)

    contexto = {'titulo': item_dict['titulo'],
                'descricao': item_dict['chamada_promocional'],
                'imagem': destino_url,
                'mensagem': mensagem}

    Log.regitra_acao(item,Log.COMPARTILHADA)

    return jsonResponse(contexto)

@csrf_exempt
def solicitar_loja(request):
    shopping = request.COOKIES.get('shp_id', None)
    if not shopping:
        raise Http404
    nome = request.POST.get('nome', None)
    email = request.POST.get('email', None)
    loja = request.POST.get('loja', None)

    loja_solicitada = Loja.objects.filter(shopping_id=shopping,nome=loja)[:1]
    if loja_solicitada:
        loja_solicitada = loja_solicitada[0]
        loja_dict = loja_solicitada.to_dict()
        mkt_lojistas = Perfil.objects.filter(shopping_id=shopping)
        mkts = mkt_lojistas.filter(tipo=Perfil.MARKETING)
        mkt_mails = [m.user.email for m in mkts]
        lojistas = mkt_lojistas.filter(tipo=Perfil.LOJISTA)
        lojistas_mails = [l.user.email for l in lojistas]
    else:
        raise Http404

    contexto = {'nome': nome,
                'email': email,
                'loja': loja_dict,
                'assunto': u'LLV - Solicitação de loja %s' % loja_dict['nome'],
                'sucesso': False}

    solicitacao = Solicitacao.objects.create(nome=nome, email=email,
                                             loja=loja_solicitada)
    envia = solicitacao.dispara_solicitacao(contexto, mkt_mails, lojistas_mails)
    if envia:
        contexto['sucesso'] = True

    return jsonResponse(contexto)

@csrf_exempt
def notifica(request, acao):
    nome = request.POST.get('nome', None)
    email = request.POST.get('email', None)
    loja = request.POST.get('loja', None)

    loja_solicitada = Loja.objects.filter(shopping_id=1,nome=loja)[:1]
    if loja_solicitada:
        loja_solicitada = loja_solicitada[0].to_dict()
    else:
        raise Http404
    contexto = {'nome': nome,
                'email': email,
                'loja': loja_solicitada,
                'assunto': u'LLV - Solicitação de loja: %s' % loja_solicitada['nome'] ,
                'sucesso': False}

    try:
        TemplatedEmail(settings.FALE_CONOSCO, contexto['assunto'],
                       'email/solicitacao.html', contexto, send_now=True)
        contexto['sucesso'] = True
    except:
        raise

    return jsonResponse(contexto)

@staff_member_required
def relatorios_index(request):
    contexto = {'shoppings': [s.to_dict() for s in Shopping.objects.all()]}
    return render(request, "relatorios/index.html", contexto)

def relatorios(request, shopping_id):
    lojas_mais_vistas_query = Loja.objects.annotate(vistas=Count('pk',
                                                                 only=Q(ofertas__logs__acao=1,shopping=shopping_id)))\
                                          .order_by('-vistas')[:10]
    lojas_mais_vistas = [{'nome': l.nome, 'numero': l.vistas} for l in lojas_mais_vistas_query if l.vistas]

    lojas_mais_pedidas_query = Loja.objects.annotate(pedidos=Count('pk', only=Q(shopping=shopping_id)))\
                                           .order_by('-pedidos','-data_criacao')[:10]
    lojas_mais_pedidas = [{'nome': l.nome, 'numero': l.pedidos} for l in lojas_mais_pedidas_query if l.pedidos]

    contexto = {'nome_shopping': Shopping.objects.get(id=shopping_id).nome,
                'shopping_id': shopping_id,
                'lojas_mais_vistas': lojas_mais_vistas,
                'lojas_mais_pedidas': lojas_mais_pedidas}
    return render(request, "relatorios/shopping.html", contexto)

@csrf_exempt
def lojas_mais_vistas(request, shopping_id):
    inicio_str = inicio = fim_str = fim = None
    if request.method == "POST":
        inicio_str = request.POST.get('inicio', None)
        inicio = datetime.strptime(inicio_str, '%d/%m/%Y')
        fim_str = request.POST.get('fim', None)
        fim = datetime.strptime(fim_str, '%d/%m/%Y')

    contexto = {'tipo': 'loja',
                'nome_shopping': Shopping.objects.get(id=shopping_id).nome}

    if inicio and fim:
        query_filtro = Loja.objects.annotate(vistas=Count('pk', only=Q(ofertas__logs__acao=1,
                                                                       shopping=shopping_id,
                                                                       ofertas__logs__data_criacao__gte=inicio,
                                                                       ofertas__logs__data_criacao__lte=fim)))\
                                   .order_by('-vistas')
        filtradas, total_filtradas = listas_e_totais(query_filtro, 'vistas')
        contexto.update({'filtradas': filtradas, 'total_filtradas': total_filtradas,
                         'inicio': inicio_str, 'fim': fim_str})
    else:
        hoje = date.today()
        mais_vistas_query = Loja.relatorio_visitas(shopping_id)
        mes_query = Loja.relatorio_visitas(shopping_id, date=hoje + timedelta(days=-30))
        semana_query = Loja.relatorio_visitas(shopping_id, date=hoje + timedelta(days=-7))

        mais_vistas, total_vistas = listas_e_totais(mais_vistas_query, 'vistas')
        mais_do_mes, total_mes = listas_e_totais(mes_query, 'vistas')
        mais_da_semana, total_semana = listas_e_totais(semana_query, 'vistas')
        contexto.update({'mais_vistas': mais_vistas, 'total_vistas': total_vistas,
                         'mais_do_mes': mais_do_mes, 'total_mes': total_mes,
                         'mais_da_semana': mais_da_semana, 'total_semana': total_semana})

    return render(request, "relatorios/mais_vistas.html", contexto)

@csrf_exempt
def lojas_mais_solicitadas(request, shopping_id):
    inicio_str = inicio = fim_str = fim = None
    if request.method == "POST":
        inicio_str = request.POST.get('inicio', None)
        inicio = datetime.strptime(inicio_str, '%d/%m/%Y')
        fim_str = request.POST.get('fim', None)
        fim = datetime.strptime(fim_str, '%d/%m/%Y')

    contexto = {'nome_shopping': Shopping.objects.get(id=shopping_id).nome}

    if inicio and fim:
        query_filtro = Loja.objects.annotate(pedidos=Count('pk', only=Q(shopping=shopping_id,
                                                                        solicitacoes__data_criacao__gte=inicio,
                                                                        solicitacoes__data_criacao__lte=fim))) \
                                   .order_by('-pedidos')
        filtradas, total_filtradas = listas_e_totais(query_filtro, 'pedidos')
        contexto.update({'filtradas': filtradas, 'total_filtradas': total_filtradas,
                         'inicio': inicio_str, 'fim': fim_str})
    else:
        hoje = date.today()
        mes = hoje + timedelta(days=-30)
        semana = hoje + timedelta(days=-7)
        solicitadas_query = Loja.relatorio_solicitacoes(shopping_id)
        mais_solicitadas, total_solicitadas = listas_e_totais(solicitadas_query, 'pedidos')
        mes_query = Loja.relatorio_solicitacoes(shopping_id, date=mes)
        mais_do_mes, total_mes = listas_e_totais(mes_query, 'pedidos')
        semana_query = Loja.relatorio_solicitacoes(shopping_id, date=semana)
        mais_da_semana, total_semana = listas_e_totais(semana_query, 'pedidos')
        contexto.update({'mais_solicitadas': mais_solicitadas, 'total_solicitadas': total_solicitadas,
                         'mais_do_mes': mais_do_mes, 'total_mes': total_mes,
                         'mais_da_semana': mais_da_semana, 'total_semana': total_semana})
    return render(request, "relatorios/lojas_mais_solicitadas.html", contexto)

@csrf_exempt
def itens_com_mais(request, shopping_id, acao, tipo):
    inicio_str = inicio = fim_str = fim = None
    if request.method == "POST":
        inicio_str = request.POST.get('inicio', None)
        inicio = datetime.strptime(inicio_str, '%d/%m/%Y')
        fim_str = request.POST.get('fim', None)
        fim = datetime.strptime(fim_str, '%d/%m/%Y')

    if inicio and fim:
        query_filtro = Oferta.relatorio_filtrado(shopping_id, acao, tipo, inicio, fim)

        filtradas, total_filtradas = listas_e_totais(query_filtro, 'vistas')
        contexto = {'tipo': Oferta.TIPOS[tipo][1], 'nome_shopping': Shopping.objects.get(id=shopping_id).nome,
                    'filtradas': filtradas, 'total_filtradas': total_filtradas,
                    'inicio': inicio_str, 'fim': fim_str}
    else:
        contexto = Oferta.itens_mais(shopping_id, acao, tipo)

    return contexto

@csrf_exempt
def ofertas_mais_vistas(request, shopping_id):
    contexto = itens_com_mais(request, shopping_id, Log.CLIQUE, Oferta.OFERTA)
    return render(request, "relatorios/mais_vistas.html", contexto)

@csrf_exempt
def ofertas_mais_curtidas(request, shopping_id):
    contexto = itens_com_mais(request, shopping_id, Log.CURTIDA, Oferta.OFERTA)
    return render(request, "relatorios/mais_vistas.html", contexto)

@csrf_exempt
def ofertas_mais_compartilhadas(request, shopping_id):
    contexto = itens_com_mais(request, shopping_id, Log.COMPARTILHADA, Oferta.OFERTA)
    return render(request, "relatorios/mais_vistas.html", contexto)

@csrf_exempt
def destaques_mais_vistos(request, shopping_id):
    contexto = itens_com_mais(request, shopping_id, Log.CLIQUE, Oferta.DESTAQUE)
    return render(request, "relatorios/mais_vistas.html", contexto)

@csrf_exempt
def destaques_mais_curtidos(request, shopping_id):
    contexto = itens_com_mais(request, shopping_id, Log.CURTIDA, Oferta.DESTAQUE)
    return render(request, "relatorios/mais_vistas.html", contexto)

@csrf_exempt
def destaques_mais_compartilhados(request, shopping_id):
    contexto = itens_com_mais(request, shopping_id, Log.COMPARTILHADA, Oferta.DESTAQUE)
    return render(request, "relatorios/mais_vistas.html", contexto)

@csrf_exempt
def eventos_mais_vistos(request, shopping_id):
    contexto = itens_com_mais(request, shopping_id, Log.CLIQUE, Oferta.EVENTO)
    return render(request, "relatorios/mais_vistas.html", contexto)

@csrf_exempt
def eventos_mais_curtidos(request, shopping_id):
    contexto = itens_com_mais(request, shopping_id, Log.CURTIDA, Oferta.EVENTO)
    return render(request, "relatorios/mais_vistas.html", contexto)

@csrf_exempt
def eventos_mais_compartilhados(request, shopping_id):
    contexto = itens_com_mais(request, shopping_id, Log.COMPARTILHADA, Oferta.EVENTO)
    return render(request, "relatorios/mais_vistas.html", contexto)

@csrf_exempt
def categorias_mais_vistas(request, shopping_id):
    inicio_str = inicio = fim_str = fim = None
    if request.method == "POST":
        inicio_str = request.POST.get('inicio', None)
        inicio = datetime.strptime(inicio_str, '%d/%m/%Y')
        fim_str = request.POST.get('fim', None)
        fim = datetime.strptime(fim_str, '%d/%m/%Y')

    contexto = {'tipo': 'categoria', 'modalidade': None,
                'nome_shopping': Shopping.objects.get(id=shopping_id).nome}

    if inicio and fim:
        query_filtro = Categoria.objects.annotate(vistas=Count('pk', only=Q(ofertas__loja__shopping=shopping_id,
                                                                            ofertas__logs__acao=1,
                                                                            ofertas__logs__data_criacao__gte=inicio,
                                                                            ofertas__logs__data_criacao__lte=fim+timedelta(days=1)))) \
                                        .order_by('-vistas')
        filtradas, total_filtradas = listas_e_totais(query_filtro, 'vistas')
        contexto.update({'filtradas': filtradas, 'total_filtradas': total_filtradas,
                         'inicio': inicio_str, 'fim': fim_str})
    else:
        hoje = date.today()
        mes = hoje + timedelta(days=-30)
        semana = hoje + timedelta(days=-7)

        mais_query = Categoria.objects.annotate(vistas=Count('pk', only=Q(ofertas__loja__shopping=shopping_id,
                                                                          ofertas__logs__acao=1))).order_by('-vistas')

        mes_query = Categoria.objects.annotate(vistas=Count('pk', only=Q(ofertas__loja__shopping=shopping_id,
                                                                         ofertas__logs__acao=1,
                                                                         ofertas__logs__data_criacao__gte=mes)))\
                                     .order_by('-vistas')

        semana_query = Categoria.objects.annotate(vistas=Count('pk', only=Q(ofertas__loja__shopping=shopping_id,
                                                                            ofertas__logs__acao=1,
                                                                            ofertas__logs__data_criacao__gte=semana)))\
                                        .order_by('-vistas')

        mais_vistas, total_vistas = listas_e_totais(mais_query, 'vistas')
        mais_do_mes, total_mes = listas_e_totais(mes_query, 'vistas')
        mais_da_semana, total_semana = listas_e_totais(semana_query, 'vistas')
        contexto.update({'mais_vistas': mais_vistas, 'total_vistas': total_vistas,
                         'mais_do_mes': mais_do_mes, 'total_mes': total_mes,
                         'mais_da_semana': mais_da_semana, 'total_semana': total_semana})

    return render(request, "relatorios/mais_vistas.html", contexto)

def ribeirao(request):
    return redirect('/ribeirao-shopping/')

def diamond(request):
    return redirect('/diamondmall/')
