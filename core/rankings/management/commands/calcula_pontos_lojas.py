# -*- encoding: utf-8 -*-

from datetime import datetime, date, timedelta

from django.core.management.base import BaseCommand
from django.db import close_old_connections

from lojas.models import Shopping, Loja
from rankings.models import Intervalo, Ponto
from geral.models import Log


class Command(BaseCommand):
    '''
    Calcula ponto das lojas nos últimos 10 dias
    '''
    args = ''
    help = u'Calcula ponto das lojas nos últimos 10 dias'

    def handle(self, *args, **options):
        malls = Shopping.objects.all()
        hoje = date.today()
        dez_dias_atras = hoje - timedelta(days=10)

        # cria novo intervalo
        intervalo, criar = Intervalo.objects.get_or_create(inicio=dez_dias_atras, fim=hoje)

        for shopping in malls:
            print 'Vendo lojas do %s' % shopping.nome
            lojas = Loja.objects.filter(ofertas__status=1,
                                        ofertas__data_aprovacao__gte=dez_dias_atras,
                                        shopping_id=shopping.id).distinct()
            # lojas = Loja.objects.filter(ofertas__status=1, ofertas__inicio__lte=date.today(),
            #                             ofertas__fim__gt=datetime.now(),
            #                             shopping_id=shopping.id).distinct()
            # lojas = Loja.objects.filter(shopping_id=shopping.id).distinct()

            for loja in lojas:
                print '    calculando pontos de %s' % loja.nome

                # cria nova entrada em Ponto pra loja nesse intervalo
                ponto, c = Ponto.objects.get_or_create(intervalo=intervalo,loja=loja)

                if ponto:
                    # ofertas = loja.ofertas.exclude(status__in=[0,3]).filter(data_aprovacao__gte=dez_dias_atras)
                    ofertas = loja.ofertas.filter(status=1,data_aprovacao__gte=dez_dias_atras)

                    produtos = ofertas.count()
                    fotos = sum([o.imagens.count() for o in ofertas])
                    likes = sum([o.logs.filter(acao=Log.CURTIDA).count() for o in ofertas])
                    shares = sum([o.logs.filter(acao=Log.COMPARTILHADA).count()*2 for o in ofertas])
                    desconto_30 = ofertas.filter(desconto__lte=30).count()
                    desconto_50 = ofertas.filter(desconto__gte=31,desconto__lte=50).count()*2
                    desconto_70 = ofertas.filter(desconto__gte=51,desconto__lte=70).count()*3
                    desconto_100 = ofertas.filter(desconto__gte=71,desconto__lte=100).count()*4

                    ponto.produtos = produtos
                    ponto.fotos = fotos
                    ponto.likes = likes
                    ponto.shares = shares
                    ponto.desconto_30 = desconto_30
                    ponto.desconto_50 = desconto_50
                    ponto.desconto_70 = desconto_70
                    ponto.desconto_100 = desconto_100

                    ponto.total = produtos+fotos+likes+shares+desconto_30+desconto_50+desconto_70\
                                  +desconto_100
                    ponto.save()

        close_old_connections()
