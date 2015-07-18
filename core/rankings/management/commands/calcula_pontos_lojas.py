# -*- encoding: utf-8 -*-

from datetime import datetime, date

from django.core.management.base import BaseCommand

from lojas.models import Shopping, Loja
from rankings.models import Intervalo, Ponto


class Command(BaseCommand):
    '''
    Calcula ponto das lojas nos últimos 10 dias
    '''
    args = ''
    help = u'Calcula ponto das lojas nos últimos 10 dias'

    def handle(self, *args, **options):
        malls = Shopping.objects.all()
        for shopping in malls:
            print 'Vendo lojas do %s' % shopping.nome
            lojas = Loja.objects.filter(ofertas__status=1,
                                       ofertas__inicio__lte=date.today(),
                                       ofertas__fim__gt=datetime.now(),
                                       shopping_id=shopping.id) \
                                 .distinct()
            for loja in lojas:
                print '    calculando pontos de %s' % loja.nome
