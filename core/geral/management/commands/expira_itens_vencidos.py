# -*- encoding: utf-8 -*-

from datetime import date

from django.core.management.base import BaseCommand

from geral.models import Oferta


class Command(BaseCommand):
    '''
    Marca como expirado os itens já vencidos
    '''
    args = ''
    help = u'Marca como expirado os itens já vencidos'

    def handle(self, *args, **options):
        print '='*50
        print u'Início'
        hoje = date.today()
        print u'Hoje é %s' % hoje
        print u'Buscando itens vencidos e marcando como "Expirado"'
        vencidos = Oferta.objects.filter(fim__lt=hoje)
        print u'Itens vencidos: %s' % vencidos.count()
        vencidos.update(status=Oferta.EXPIRADO)
        print '='*50