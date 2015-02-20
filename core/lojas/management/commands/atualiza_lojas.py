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
                shoppings = Shopping.get_publicadas()
                print ' Iterando sobre %s shoppings' % shoppings.count()
                for shopping in shoppings:
                    print ' Buscando lojas do %s' % shopping
                    dados = cliente.service.findLoja(codEmpreendimento=shopping.id_multiplan)
                    total = 0
                    for d in dados:
                        if d.fantasia.nome:
                            nome = string.capwords(d.fantasia.nome)
                            try:
                                loja, criada = Loja.objects.get_or_create(shopping=shopping,
                                                                          id_multiplan=d.codPessoa)
                                if loja:
                                    loja.publicada = True
                                    loja.nome = nome
                                    loja.save()
                                total += 1
                            except:
                                print '    problema com a loja %s' % nome
                                pass
                    print '    Total de %s lojas' % total
            else:
                print ' Houve algum problema.'
                print ' Encerrando...'

        except Exception, e:
            raise e
        print 45 * '-'
        print '\tFIM'
        print 45 * '-'