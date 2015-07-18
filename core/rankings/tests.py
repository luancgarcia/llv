# -*- encoding: utf-8 -*-
import datetime
from django.test import TestCase

from models import Intervalo, Ponto
from lojas.tests import LojaModelTest

inicio = datetime.datetime.strptime('01072015', '%d%m%Y').date()
fim = datetime.datetime.strptime('15072015', '%d%m%Y').date()

class IntervaloModelTest(TestCase):
    @classmethod
    def _create_intervalo(cls, inicio, fim):
        intervalo = Intervalo()
        intervalo.inicio = inicio
        intervalo.fim = fim
        intervalo.save()
        return intervalo

    def test_creating_intervalo_and_save_it_in_the_database(self):
        intervalo = self._create_intervalo(inicio, fim)

        all_intervalos_saved = Intervalo.objects.all()
        self.assertEquals(len(all_intervalos_saved), 1)
        only_intervalo_saved = all_intervalos_saved[0]

        self.assertEquals(only_intervalo_saved, intervalo)
        self.assertEquals(only_intervalo_saved.inicio, inicio)
        self.assertEquals(only_intervalo_saved.fim, fim)


class PontoModelTest(TestCase):
    @classmethod
    def _create_ponto(cls, intervalo, loja):
        ponto = Ponto()
        ponto.intervalo = intervalo
        ponto.loja = loja
        ponto.produtos = 1
        ponto.fotos = 1
        ponto.likes = 1
        ponto.shares = 2
        ponto.desconto_30 = 1
        ponto.desconto_50 = 2
        ponto.desconto_70 = 3
        ponto.desconto_100 = 4
        ponto.save()
        return ponto

    def test_creating_ponto_and_save_it_in_the_database(self):
        intervalo = IntervaloModelTest._create_intervalo(inicio, fim)
        loja = LojaModelTest._create_loja()
        ponto = self._create_ponto(intervalo, loja)

        all_pontos_saved = Ponto.objects.all()
        self.assertEquals(all_pontos_saved.count(), 1)
        only_ponto_saved = all_pontos_saved[0]

        self.assertEquals(only_ponto_saved, ponto)

        self.assertEquals(only_ponto_saved.intervalo, intervalo)
        self.assertEquals(only_ponto_saved.loja, loja)
        self.assertEquals(only_ponto_saved.shares, 2)
        self.assertEquals(only_ponto_saved.desconto_100, 4)