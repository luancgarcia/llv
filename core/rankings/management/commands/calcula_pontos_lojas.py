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
        dez_dias_atras = hoje - timedelta(days=-10)

        # cria novo intervalo
        intervalo, criar = Intervalo.objects.get_or_create(inicio=dez_dias_atras, fim=hoje)

        for shopping in malls:
            print 'Vendo lojas do %s' % shopping.nome
            # lojas = Loja.objects.filter(ofertas__status=1,ofertas__inicio__lte=date.today(),ofertas__fim__gt=datetime.now(),shopping_id=shopping.id).distinct()
            lojas = Loja.objects.filter(shopping_id=shopping.id).distinct()

            for loja in lojas:
                print '    calculando pontos de %s' % loja.nome

                # cria nova entrada em Ponto pra loja nesse intervalo
                ponto, c = Ponto.objects.get_or_create(intervalo=intervalo,loja=loja)

                if ponto:
                    # import ipdb;ipdb.set_trace()
                    ofertas = loja.ofertas.exclude(status__in=[0,3]) \
                                          .filter(data_aprovacao__gte=dez_dias_atras)

                    ponto.produtos = ofertas.count()
                    ponto.fotos = sum([o.imagens.count() for o in ofertas])
                    ponto.likes = sum([o.logs.filter(acao=Log.CURTIDA).count() for o in ofertas])
                    ponto.shares = sum([o.logs.filter(acao=Log.COMPARTILHADA).count()*2 for o in ofertas])
                    ponto.desconto_30 = ofertas.filter(desconto__lte=30).count()
                    ponto.desconto_50 = ofertas.filter(desconto__gte=31,desconto__lte=50).count()*2
                    ponto.desconto_70 = ofertas.filter(desconto__gte=51,desconto__lte=70).count()*3
                    ponto.desconto_100 = ofertas.filter(desconto__gte=71,
                                                        desconto__lte=100).count()*4
                    ponto.save()

        # close_old_connections()
