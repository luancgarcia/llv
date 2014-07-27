# -*- encoding: utf-8 -*-

from django.db import models
from django.utils.text import slugify
from imagekit.models import ImageSpecField
from pilkit.processors import Adjust, resize

from utils.models import BaseModel, EditorialModel, BaseManager
from lojas.models import Loja


class Categoria(EditorialModel):
    nome = models.CharField(u'Nome', max_length=100, blank=False, null=True)
    slug = models.SlugField(max_length=150, blank=False, null=False, unique=True)
    default = models.BooleanField(u'Categoria default?', default=False)

    class Meta:
        verbose_name=u'Categoria'
        verbose_name_plural=u'Categorias'
        ordering = ['nome']

    def __unicode__(self):
        return u'%s' % self.nome


class Oferta(EditorialModel):
    OFERTA = 0
    DESTAQUE = 1
    EVENTO = 2

    TIPOS = (
        (OFERTA, u'Oferta'),
        (DESTAQUE, u'Destaque'),
        (EVENTO, u'Evento')
    )

    loja = models.ForeignKey(Loja, verbose_name=u'Loja', related_name='ofertas',
                             null=True, blank=True)
    nome = models.CharField(u'Nome', max_length=200, null=True, blank=True)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    descricao = models.TextField(u'Descrição do produto', blank=True, null=True)
    evento = models.TextField(u'Descrição do Evento', blank=True, null=True)
    texto_promocional = models.TextField(u'Chamada Promocional',
                                         blank=True, null=True)
    preco_inicial = models.CharField(u'De: R$', max_length=70, null=True,
                                     blank=False)
    preco_final = models.CharField(u'Por: R$', max_length=70, null=True,
                                   blank=False)
    desconto = models.IntegerField(u'Desconto', null=True, blank=True)
    tipo = models.IntegerField(u'Tipo', choices=TIPOS, default=OFERTA)
    texto_link = models.CharField(u'Texto do link', max_length="140", null=True, blank=False)

    class Meta:
        verbose_name=u'Oferta'
        verbose_name_plural=u'Ofertas'
        ordering = ['nome']
        unique_together = (('loja','slug'))

    def __unicode__(self):
        return u'%s - %s[ %s off %s - %s ]' % (self.nome,
                                               self.texto_link,
                                               self.desconto_value,
                                               self.preco_inicial,
                                               self.preco_final)

    @property
    def desconto_value(self):
        return u'%s%%' % self.desconto if self.desconto else ''

    def porcentagem_desconto(self):
        antes = float(self.preco_inicial.replace(',','.'))
        depois = float(self.preco_final.replace(',','.'))
        return int(100-(100*int(depois)/int(antes)))

    @classmethod
    def get_ofertas(cls):
        return cls.objects.filter(publicada=True,tipo=cls.OFERTA)

    def to_dict(self):
        return {'loja': self.loja,
                'descricao': self.descricao,
                'porcentagem': self.porcentagem_desconto(),
                'desconto': self.desconto,
                'preco_final': self.preco_final,
                'preco_inicial': self.preco_inicial}


class Destaque(Oferta):
    class Meta:
        proxy = True
        verbose_name=u'Destaque'
        verbose_name_plural=u'Destaques'


class Evento(Oferta):
    class Meta:
        proxy = True
        verbose_name=u'Evento'
        verbose_name_plural=u'Eventos'


class ImagemOferta(EditorialModel):
    oferta = models.ForeignKey(Oferta, verbose_name=u'Oferta',
                               related_name='imagens')
    imagem = models.ImageField(u'Imagem', upload_to='ofertas',
                               null=True, blank=True)
    img_376x376 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(376, 376)],
                                 source='imagem', format='JPG',
                                 options={'quality': 90})
    principal = models.BooleanField(u'Imagem principal', default=False)
    vertical = models.BooleanField(u'Imagem vertical', default=False)

    class Meta:
        verbose_name=u'Imagem da oferta'
        verbose_name_plural=u'Imagens das ofertas'


class Log(BaseModel):
    CLIQUE = 1
    CURTIDA = 2
    COMPARTILHADA = 3

    ACOES = (
        (CLIQUE, u'Clique'),
        (CURTIDA, u'Curtida'),
        (COMPARTILHADA, u'Compartilhada'),
    )

    oferta = models.ForeignKey(Oferta, verbose_name=u'Oferta',
                               related_name='logs', null=True, blank=True)
    acao = models.IntegerField(u'Ação', blank=True, null=True, choices=ACOES)

    class Meta:
        verbose_name=u'Log de Ação'
        verbose_name_plural=u'Logs das Ações'
        ordering = ['data_criacao',]

    def __unicode__(self):
        return u'%s - %s' % (self.oferta, ACOES[self.acao][1])

