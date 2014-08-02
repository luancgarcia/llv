# -*- encoding: utf-8 -*-

from optparse import make_option
from suds.client import Client
import string

from django.core.files import File
from django.core.management.base import BaseCommand
from django.conf import settings

from lojas.models import Shopping, Loja


class Command(BaseCommand):
    '''
    Importa as lojas consultando o servido do wiseit
    '''
    args = ''
    help = 'Importa as lojas consultando o servido do wiseit'

    def handle(self, *args, **options):
        print 45 * '-'
        print '\tIniciando consulta ao WiseIt'
        print 45 * '-'
        try:
            cliente = Client(settings.WSDL_URL)
            if cliente:
                print ' Contectou'
                shoppings = Shopping.get_publicadas()
                for shopping in shoppings:
                    print ' Buscando lojas do %s' % shopping
                    dados = cliente.service.findLoja(codEmpreendimento=shopping.id_multiplan)
                    nomes = [string.capwords(d.fantasia.nome) for d in dados if d.fantasia.nome]
                    print ' %s lojas' % len(nomes)
                    for nome in nomes:
                        loja, criada = Loja.objects.get_or_create(shopping=shopping,
                                                                  nome=nome)
                        if loja:
                            loja.publicada = True
                            loja.save()
            else:
                print ' Houve algum problema.'
                print ' Encerrando...'

        except Exception, e:
            raise e

        print 45 * '-'
        print '\tFIM'
        print 45 * '-'