# -*- encoding: utf-8 -*-
import os

from datetime import datetime, timedelta
from imagekit.models import ImageSpecField
from pilkit.processors import Adjust, resize

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.template.defaultfilters import date as _date

from utils.models import BaseModel, EditorialModel, BaseManager, OrderedModel
from lojas.models import Loja, Shopping
from notificacoes.models import Notificacao


class Perfil(BaseModel):
    LOJISTA = 0
    MARKETING = 1
    ADMINISTRADOR = 2

    TIPOS = (
        (LOJISTA, u'Lojista'),
        (MARKETING, u'Marketing'),
        (ADMINISTRADOR, u'Administrador'),
    )

    user = models.ForeignKey(User, related_name='perfil', verbose_name='Usuário')
    loja = models.ForeignKey(Loja, verbose_name=u'Loja', related_name='usuarios',
                             null=True, blank=True)
    shopping = models.ForeignKey(Shopping, verbose_name=u'Shopping',
                                 related_name='usuarios', null=True, blank=True)
    tipo = models.IntegerField(u'Tipo', choices=TIPOS, default=LOJISTA,
                               blank=True, null=True)

    def __unicode__(self):
        return u'%s' % self.user

    @property
    def is_marketing(self):
        return True if self.tipo == Perfil.MARKETING else None

    @property
    def is_lojista(self):
        return True if self.tipo == Perfil.LOJISTA else None

    @property
    def is_adm(self):
        return True if self.tipo == Perfil.ADMINISTRADOR else None


class PerfilMarketing(Perfil):
    class Meta:
        proxy = True
        verbose_name = u'Perfil Marketing'
        verbose_name_plural = u'Perfis Marketing'


class PerfilLojista(Perfil):
    class Meta:
        proxy = True
        verbose_name = u'Perfil Lojista'
        verbose_name_plural = u'Perfis Lojistas'


class PerfilAdministrador(Perfil):
    class Meta:
        proxy = True
        verbose_name = u'Perfil Administrador'
        verbose_name_plural = u'Perfis Administradores'


class Categoria(EditorialModel):
    shopping = models.ForeignKey(Shopping, verbose_name=u'Shopping',
                                 related_name='categorias', null=True, blank=True)
    nome = models.CharField(u'Nome', max_length=100, blank=False, null=True)
    slug = models.SlugField(max_length=150, blank=False, null=False, unique=True)
    sazonal = models.BooleanField(u'Categoria sazonal?', default=False)
    imagem = models.ImageField(u'Imagem', upload_to='categorias',
                               null=True, blank=True)
    img_162x27 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(162, 27)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})

    class Meta:
        verbose_name=u'Categoria'
        verbose_name_plural=u'Categorias'
        ordering = ['nome']

    def __unicode__(self):
        shopping = ' (%s)' % self.shopping.nome if self.shopping else ''
        return u'%s%s' % (self.nome, shopping)

    def to_dict(self):
        contexto =  {'id': self.id,
                     'nome': self.nome,
                     'slug': self.slug}
        if self.sazonal:
            contexto.update({'imagem': self.img_162x27.url if self.imagem else None})

        return contexto

    @classmethod
    def publicadas_com_oferta(cls):
        shopping = Shopping.objects.get(id=1)
        categorias = cls.objects.filter(shopping=shopping,publicada=True,sazonal=False).order_by('nome')
        return [c.to_dict() for c in categorias if c.ofertas.filter(status=Oferta.PUBLICADO)]


class Sazonal(Categoria):
    class Meta:
        proxy = True
        verbose_name = u'Categoria Sazonal'
        verbose_name_plural = u'Categorias Sazonais'

    def save(self, *args, **kwargs):
        self.sazonal = True
        if self.publicada:
            Categoria.objects.filter(publicada=True,sazonal=True).update(publicada=False)
        super(Categoria, self).save(*args, **kwargs)

    @classmethod
    def atual(cls):
        atual = cls.objects.filter(sazonal=True,publicada=True)[:1]
        return atual[0].to_dict() if atual else {}


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
        (PENDENTE, u'Pendente'),
        (PUBLICADO, u'Publicado'),
        (EXPIRADO, u'Expirado'),
    )

    MASCULINO =0
    FEMININO = 1
    INFANTIL = 2
    UNISSEX = 3
    GENEROS = (
        (MASCULINO, u'Masculino'),
        (FEMININO, u'Feminino'),
        (INFANTIL,u'Infantil'),
        (UNISSEX,u'Unissex'),
    )

    loja = models.ForeignKey(Loja, verbose_name=u'Loja', related_name='ofertas',
                             null=True, blank=True)
    categoria = models.ManyToManyField(Categoria, verbose_name=u'Categoria',null=True,
                                       blank=True, related_name='ofertas')
    nome = models.CharField(u'Título', max_length=200, null=True, blank=False)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    descricao = models.TextField(u'Descrição do produto', blank=True, null=True)
    evento = models.TextField(u'Descrição do Evento', blank=True, null=True)
    texto_promocional = models.TextField(u'Chamada Promocional',
                                         blank=True, null=True)
    preco_inicial = models.DecimalField(u'De R$', max_digits=8, decimal_places=2,
                                     null=True, blank=True)
    preco_final = models.DecimalField(u'Por R$', max_digits=8, decimal_places=2,
                                      null=True, blank=True)
    desconto = models.IntegerField(u'Desconto (em %)', null=True, blank=True)
    tipo = models.IntegerField(u'Tipo', choices=TIPOS, default=OFERTA)
    texto_link = models.CharField(u'Texto do link', max_length="140", null=True, blank=True)
    status = models.IntegerField(u'Status', choices=STATUSES, default=PENDENTE)
    data_aprovacao = models.DateTimeField(u"Data de aprovação", null=True)
    genero = models.IntegerField(u'Gênero', choices=GENEROS, default=UNISSEX,
                                 null=True, blank=False)
    autor = models.ForeignKey(Perfil, verbose_name=u'Autor', null=True, blank=False)

    class Meta:
        verbose_name=u'Oferta'
        verbose_name_plural=u'Ofertas'
        ordering = ['-data_aprovacao','nome']
        unique_together = (('loja','slug'))

    def __unicode__(self):
        desconto_str = u'%s off' % self.desconto_value if self.desconto_value else ''
        preco_final = u'%s' % self.preco_final if self.preco_final else ''
        preco_inicial = u'%s' % self.preco_inicial if self.preco_inicial else ''
        separador = ' - ' if preco_final and preco_inicial else ''
        return u'%s [ %s %s%s%s ]' % (self.nome,
                                    desconto_str,
                                    preco_inicial,
                                    separador,
                                    preco_final)

    def save(self, *args, **kwargs):
        if self.status == Oferta.PUBLICADO:
            self.data_aprovacao = datetime.now()
            # if self.notificacoes.all():
            #     pass
        elif self.status == Oferta.PENDENTE:
            mkt = self.marketing_responsavel
            n, created = Notificacao.objects.get_or_create(oferta=self,
                                                           solicitante=self.autor,
                                                           responsavel=mkt)
            if n:
                n.save()
            # notifica criacao
        super(Oferta, self).save(*args, **kwargs)

    def desconto_value(self):
        return u'%s%%' % self.desconto if self.desconto else ''
    desconto_value.short_description = u'Desconto'
    desconto_value = property(desconto_value)

    @property
    def expira(self):
        return self.data_aprovacao + timedelta(days=7) if self.data_aprovacao else None

    @property
    def expira_str(self):
        return _date(self.expira, 'd/m/Y') if self.expira else None

    def status_string(self):
        return u'%s' % Oferta.STATUSES[self.status][1]
    status_string.short_description = u'Status'

    def porcentagem_desconto(self):
        if self.preco_inicial and self.preco_final:
            return int(100-(100*int(self.preco_final)/int(self.preco_inicial)))
        else:
            return None

    @classmethod
    def get_ofertas(cls):
        return cls.objects.filter(publicada=True,tipo=cls.OFERTA)

    def marketing_responsavel(self):
        marketing = Perfil.objects.filter(tipo=Perfil.MARKETING,
                                          shopping=self.loja.shopping)[:1]
        return marketing[0] if marketing else None
    marketing_responsavel.short_description = u'Marketing responsável'
    marketing_responsavel.property = True


    def to_dict(self, modal=False):
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

        contexto =  {'id': self.id,
                     'loja': self.loja.to_dict() if self.loja else None,
                     'descricao': self.descricao,
                     'texto_do_link': self.texto_link,
                     'chamada_promocional': self.texto_promocional,
                     'imagem': imagem,
                     'compartilhamentos': self.total_visto,
                     'curtidas': self.total_curtido,
                     'categoria': [c.to_dict() for c in self.categoria.all()],
                     'expira': self.expira,
                     'expira_str': self.expira_str,
                     'titulo': self.nome}

        if not self.tipo == Oferta.EVENTO:
            contexto.update({'porcentagem': self.porcentagem_desconto(),
                             'desconto': self.desconto,
                             'preco_final': self.preco_final,
                             'preco_inicial': self.preco_inicial,})

        if modal:
            imagens = [{'maior':img.img_376x376.url,
                        'menor':img.img_94x94.url} for img in self.imagens.all()]
            contexto.update({'descricao': self.descricao,
                             'imagens': imagens})
        return contexto

    @classmethod
    def prontos(cls, tipo=OFERTA, from_id=None):
        items = cls.objects.filter(tipo=tipo,
                                   status=cls.PUBLICADO)\
                           .order_by('-data_aprovacao')
        if from_id:
            items = items.filter(id__gt=from_id)
        if tipo == cls.OFERTA:
            return [i.to_dict() for i in items[:32]]
        return [i.to_dict() for i in items[:3]]

    @property
    def total_compartilhado(self):
        return u'%s' % self.logs.filter(acao=Log.COMPARTILHADA).count()

    @property
    def total_visto(self):
        return u'%s' % self.logs.filter(acao=Log.CLIQUE).count()

    @property
    def total_curtido(self):
        return u'%s' % self.logs.filter(acao=Log.CURTIDA).count()


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

    def __unicode__(self):
        return u'%s' % self.nome


class ImagemOferta(OrderedModel):
    def new_filename(instance, filename):
        fname, dot, extension = filename.rpartition('.')
        fname = slugify(fname)
        return os.path.join('ofertas','%s.%s' % (fname, extension))

    oferta = models.ForeignKey(Oferta, verbose_name=u'Oferta',
                               related_name='imagens')
    imagem = models.ImageField(u'Imagem', upload_to=new_filename,
                               null=True, blank=True)
    img_376x376 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(376, 376)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})
    img_172x172 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(172, 172)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})
    img_94x94 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(94, 94)],
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
        ordering = ['-data_criacao',]

    def __unicode__(self):
        return u'%s - %s' % (self.oferta, self.ACOES[self.acao-1][1])

    @classmethod
    def regitra_acao(cls, oferta, acao):
        cls.objects.create(oferta=oferta,acao=acao)


class Mascara(EditorialModel):
    NORMAL = 0
    SAZONAL = 1
    CATEGORIAS = (
        (NORMAL, u'Normal'),
        (SAZONAL, u'Sazonal')
    )

    def new_filename(instance, filename):
        fname, dot, extension = filename.rpartition('.')
        fname = slugify(fname)
        return os.path.join('mascaras','%s.%s' % (fname, extension))

    imagem = models.ImageField(u'Imagem', upload_to=new_filename,
                               null=True, blank=True)
    img_376x376 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(376, 376)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})
    thumb = models.ImageField(u'Thumbnail', upload_to=new_filename,
                               null=True, blank=True)
    thumb_98x98 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(98, 98)],
                                 source='thumb', format='PNG',
                                 options={'quality': 90})
    categoria = models.IntegerField(u'Tipo de categoria', choices=CATEGORIAS,
                                    null=True, blank=True, default=NORMAL)

    class Meta:
        verbose_name = u'Imagem para compartilhar'
        verbose_name_plural = u'Imagens para compartilhar'

    def __unicode__(self):
        return u'%s' % self.imagem

    def custom_miniatura(self):
        return u'<a href='

    @classmethod
    def serializado(cls):
        return [{'id': i.id,
                 'imagem': i.img_376x376.url,
                 'thumb': i.thumb_98x98.url} for i in cls.get_publicadas()]
