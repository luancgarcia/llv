# -*- encoding: utf-8 -*-
from django.db import models

from utils.models import BaseModel
from lojas.models import Loja

class Intervalo(BaseModel):
    inicio = models.DateField(u'Início', null=False, blank=False)
    fim = models.DateField(u'Fim', null=False, blank=False)

    class Meta:
        verbose_name = u'Intervalo'
        verbose_name_plural = u'Intervalos'

    def __unicode__(self):
        return u'%s a %s' % (self.inicio.strftime("%d/%m/%Y"), self.fim.strftime("%d/%m/%Y"))


class Ponto(BaseModel):
    intervalo = models.ForeignKey(Intervalo, verbose_name='Intervalo', related_name='pontos')
    loja = models.ForeignKey(Loja, verbose_name='Loja', related_name='pontos')
    produtos = models.IntegerField(u'Produtos', null=True)  # 1 ponto cada
    fotos = models.IntegerField(u'Fotos', null=True)  # 1 ponto cada
    likes = models.IntegerField(u'Curtidas', null=True)  # 1 ponto cada
    shares = models.IntegerField(u'Compartilhadas', null=True)  # 2 pontos cada
    desconto_30 = models.IntegerField(u'Descontos até 30%', null=True) # 1 ponto cada
    desconto_50 = models.IntegerField(u'Descontos de 31% a 50%', null=True) # 2 pontos cada
    desconto_70 = models.IntegerField(u'Descontos de 51% a 70%', null=True) # 3 pontos cada
    desconto_100 = models.IntegerField(u'Descontos acima de 70%', null=True) # 4 pontos cada
    total = models.IntegerField(u'Total', null=True)

    class Meta:
        verbose_name = u'Ponto'
        verbose_name_plural = u'Pontos'

    def __unicode__(self):
        return u'%s pontos do intervalo %s da loja %s' % (self.total, self.intervalo, self.loja)

    def to_dict(self):
        return {'loja': self.loja.nome,
                'total': self.total}

    @classmethod
    def dez_mais(cls, shopping, intervalo):
        return cls.objects.filter(loja__shopping_id=shopping,intervalo_id=intervalo).order_by('-total', 'loja__nome')[:10]
