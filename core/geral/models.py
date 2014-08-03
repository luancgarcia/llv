# -*- encoding: utf-8 -*-
from datetime import datetime
from imagekit.models import ImageSpecField
from pilkit.processors import Adjust, resize

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User

from utils.models import BaseModel, EditorialModel, BaseManager, OrderedModel
from lojas.models import Loja


class Perfil(BaseModel):
    user = models.ForeignKey(User, related_name='perfil', verbose_name='Usuário')
    loja = models.ForeignKey(Loja, verbose_name=u'Loja', related_name='usuarios',
                             null=True, blank=True)

    def __unicode__(self):
        return u'%s' % self.user.first_name


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

    PENDENTE = 0
    PUBLICADO = 1
    EXPIRADO = 2
    STATUSES = (
        (PENDENTE, u'Pendete'),
        (PUBLICADO, u'Publicado'),
        (EXPIRADO, u'Expirado'),
    )

    loja = models.ForeignKey(Loja, verbose_name=u'Loja', related_name='ofertas',
                             null=True, blank=True)
    nome = models.CharField(u'Título', max_length=200, null=True, blank=True)
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
    status = models.IntegerField(u'Status', choices=STATUSES, default=PENDENTE)
    data_aprovacao = models.DateTimeField(u"Data de aprovação", null=True)

    class Meta:
        verbose_name=u'Oferta'
        verbose_name_plural=u'Ofertas'
        ordering = ['-data_aprovacao','nome']
        unique_together = (('loja','slug'))

    def __unicode__(self):
        return u'%s - %s [ %s off %s - %s ]' % (self.nome,
                                               self.texto_link,
                                               self.desconto_value,
                                               self.preco_inicial,
                                               self.preco_final)

    def save(self, *args, **kwargs):
        if self.status == Oferta.PUBLICADO:
            self.data_aprovacao = datetime.now()
        super(Oferta, self).save(*args, **kwargs)

    @property
    def desconto_value(self):
        return u'%s%%' % self.desconto if self.desconto else ''

    def status_string(self):
        return u'%s' % Oferta.STATUSES[self.status][1]
    status_string.short_description = u'Status'

    def porcentagem_desconto(self):
        antes = float(self.preco_inicial.replace(',','.'))
        depois = float(self.preco_final.replace(',','.'))
        return int(100-(100*int(depois)/int(antes)))

    @classmethod
    def get_ofertas(cls):
        return cls.objects.filter(publicada=True,tipo=cls.OFERTA)

    def to_dict(self):
        imagem = None
        if self.tipo == Oferta.OFERTA:
            imagens = self.imagens.filter(oferta__tipo=Oferta.OFERTA)
            if imagens:
                imagem = imagens[0].img_172x172.url
        elif self.tipo == Oferta.EVENTO:
            imagens = self.imagens.filter(oferta__tipo=Oferta.EVENTO)
            if imagens:
                imagem = imagens[0].evento_180x445.url
        else:
            imagens = self.imagens.filter(oferta__tipo=Oferta.DESTAQUE)
            if imagens:
                imagem = imagens[0].img_376x376.url

        return {'id': self.id,
                'loja': self.loja,
                'descricao': self.descricao,
                'porcentagem': self.porcentagem_desconto(),
                'desconto': self.desconto,
                'preco_final': self.preco_final,
                'preco_inicial': self.preco_inicial,
                'texto_do_link': self.texto_link,
                'chamada_promocional': self.texto_promocional,
                'loja': self.loja.to_dict(),
                'imagem': imagem}

    @classmethod
    def destaques_prontos(cls):
        destaques = cls.objects.filter(tipo=cls.DESTAQUE,
                                       status=cls.PUBLICADO)\
                               .order_by('-data_aprovacao')
        return [d.to_dict() for d in destaques[:3]]

    @classmethod
    def eventos_prontos(cls):
        eventos = cls.objects.filter(tipo=cls.EVENTO,
                                     status=cls.PUBLICADO)\
                             .order_by('-data_aprovacao')
        return [e.to_dict() for e in eventos[:3]]

    @classmethod
    def ofertas_prontas(cls):
        ofertas = cls.objects.filter(tipo=cls.OFERTA,
                                     status=cls.PUBLICADO)\
                             .order_by('-data_aprovacao')
        return [o.to_dict() for o in ofertas[:32]]


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


class ImagemOferta(OrderedModel):
    oferta = models.ForeignKey(Oferta, verbose_name=u'Oferta',
                               related_name='imagens')
    imagem = models.ImageField(u'Imagem', upload_to='ofertas',
                               null=True, blank=True)
    img_376x376 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(376, 376)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})
    img_172x172 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(172, 172)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})
    evento_180x445 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(180, 445)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})
    principal = models.BooleanField(u'Imagem principal', default=False)
    vertical = models.BooleanField(u'Imagem vertical', default=False)

    class Meta:
        verbose_name=u'Imagem'
        verbose_name_plural=u'Imagens das ofertas'
        ordering = ['oferta','ordem']

    def __unicode__(self):
        return u'%s - %s' % (self.oferta.nome, self.ordem)


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

