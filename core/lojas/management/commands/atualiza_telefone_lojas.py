# -*- encoding: utf-8 -*-

from optparse import make_option
from suds.client import Client
import string

from django.core.management.base import BaseCommand
from django.conf import settings

from lojas.models import Shopping, Loja


class Command(BaseCommand):
    '''
    Atualiza as lojas consultando o servido do wiseit
    '''
    help = 'Atualiza as lojas consultando o servido do wiseit'

    def handle(self, *args, **options):
        print 45 * '-'
        print '\tIniciando consulta ao WiseIt'
        print 45 * '-'
        try:
            cliente = Client(settings.WSDL_URL)
            if cliente:
                print ' Contectou'
                lojas = Loja.objects.all()
                print ' Iterando sobre %s lojas' % lojas.count()
                total = 0
                for loja in lojas:
                    dado = cliente.service.findLojaById(codigo=loja.id_multiplan, mostrar='todos')
                    if dado.telefone and dado.telefone[0]:
                        info = dado.telefone[0]
                        loja.telefone = '(%s) %s' % (info.numDDD, info.numTelefone)
                        loja.save()
                        total += 1
                print '    Total de %s lojas atualizadas' % total
            else:
                print ' Houve algum problema.'
                print ' Encerrando...'

        except Exception, e:
            raise e
        print 45 * '-'
        print '\tFIM'
        print 45 * '-'