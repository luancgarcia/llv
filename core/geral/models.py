# -*- encoding: utf-8 -*-
import os

from datetime import datetime, timedelta, date
from imagekit.models import ImageSpecField
from pilkit.processors import Adjust, resize

from django.db import models
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.template.defaultfilters import date as _date
from django.db.models import Q
from aggregate_if import Count
from django.db.models.signals import post_save
from django.conf import settings

from utils.models import BaseModel, EditorialModel, OrderedModel
from utils.functions import separa_tres_colunas, dict_mais_vistas, listas_e_totais
from lojas.models import Loja, Shopping
from geral.signals import cria_envia_notificacao, completa_slug
from notificacoes.models import Solicitacao


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

    @property
    def possui_notificacoes(self):
        return True if self.responsavel.all() else False

    @property
    def numero_notificacoes(self):
        return u'%s' % self.responsavel.all().count()

    @property
    def numero_notificacoes_naolidas(self):
        return u'%s' % self.responsavel.filter(lida=False).count()


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
    slug = models.SlugField(max_length=150, blank=False, null=False,
                            unique=False)
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
        unique_together = ('shopping','slug')

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
    def publicadas_com_oferta(cls, shopping=1):
        categorias = cls.objects.filter(shopping_id=shopping, sazonal=False,
                                        publicada=True).select_related()
        categorias = categorias.filter(ofertas__status=1, ofertas__fim__gte=date.today()) \
                                .order_by('nome') \
                                .distinct()
#        categorias = cls.objects.filter(ofertas__fim__gt=date.today(), ofertas__status=1, shopping_id=shopping, sazonal=False, publicada=True) \
#                                .order_by('nome') \
#                                .distinct()
        return categorias
        '''return separa_tres_colunas([c.to_dict() for c in categorias])'''


class Sazonal(Categoria):
    class Meta:
        proxy = True
        verbose_name = u'Categoria Sazonal'
        verbose_name_plural = u'Categorias Sazonais'

    def save(self, *args, **kwargs):
        self.sazonal = True
        if self.publicada:
            Categoria.objects.filter(publicada=True,sazonal=True,shopping=self.shopping)\
                             .update(publicada=False)
        super(Categoria, self).save(*args, **kwargs)

    @classmethod
    def atual(cls, serializado=False, shopping=1):
        atual = cls.objects.filter(sazonal=True,
                                   publicada=True,
                                   shopping_id=shopping)[:1]
        if serializado:
            return atual[0].to_dict() if atual else {}
        return atual[0] if atual else None


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
    RASCUNHO = 3
    REPROVADO = 4
    STATUSES = (
        (PENDENTE, u'Pendente'),
        (PUBLICADO, u'Publicado'),
        (EXPIRADO, u'Expirado'),
        (RASCUNHO, u'Rascunho'),
        (REPROVADO, u'Reprovado'),
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
    shopping = models.ForeignKey(Shopping, verbose_name=u'Shopping', null=True,
                                 blank=True, related_name='ofertas')
    categoria = models.ManyToManyField(Categoria, verbose_name=u'Categoria',null=True,
                                       blank=True, related_name='ofertas')
    nome = models.CharField(u'Título', max_length=200, null=True, blank=False)
    slug = models.SlugField(max_length=250, null=True, blank=True, unique=True)
    descricao = models.TextField(u'Descrição do produto', blank=True, null=True)
    evento = models.TextField(u'Descrição do Evento', blank=True, null=True)
    texto_promocional = models.CharField(u'Chamada Promocional', blank=True,
                                         null=True, max_length=25,
                                         help_text=u'Limite 25 caracteres')
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
                                 null=True, blank=True)
    autor = models.ForeignKey(Perfil, verbose_name=u'Autor', null=True, blank=False)
    inicio = models.DateField(u'Data de publicação', null=True, blank=False,
                              help_text=u'Informe a data para ficar online')
    fim = models.DateField(u'Data de expiração', null=True, blank=False,
                           help_text=u'Informe a data para ficar offline ')
    razao = models.TextField(u'Razão da reprovação', null=True, blank=True)

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
            notificacoes = self.notificacoes.all()
            if notificacoes:
                for n in notificacoes:
                    try:
                        n.notifica_aprovacao()
                    except:
                        pass

            for s in Solicitacao.objects.filter(loja=self.loja):
                try:
                    s.responde_solicitacao()
                except:
                    pass
        elif self.status == Oferta.REPROVADO:
            notificacoes = self.notificacoes.all()
            if notificacoes:
                for n in notificacoes:
                    try:
                        n.notifica_reprovacao(self.razao)
                    except:
                        pass
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
            return 0

    @classmethod
    def get_ofertas(cls):
        return cls.objects.filter(publicada=True,tipo=cls.OFERTA)

    @property
    def marketing_responsavel(self):
        if not self.loja or self.status == Oferta.PUBLICADO:
            return None
        marketing = Perfil.objects.filter(tipo=Perfil.MARKETING,
                                          shopping=self.loja.shopping)[:1]
        return marketing[0] if marketing else None

    def get_image(self):
        imagem = None
        images = self.imagens.all()
        if self.tipo == Oferta.OFERTA:
            if images and images[0].imagem:
                imagem = images[0].img_172x172.url
        elif self.tipo == Oferta.EVENTO:
            if images:
                imagem = images[0].evento_180x445.url
        else:
            if images:
                imagem = images[0].img_376x376.url

        return imagem

    @classmethod
    def prontos_api(cls, from_id=None, id_multiplan=1):
        hoje = date.today()
        items = cls.objects.filter(status=cls.PUBLICADO,loja__shopping__id_multiplan=id_multiplan,
                                   inicio__lte=hoje, fim__gte=hoje).order_by('-data_aprovacao')
        if from_id:
            filtro = cls.objects.get(id=from_id)
            items = items.filter(data_aprovacao__lt=filtro.data_aprovacao)
        items = items[:32]
        return [i.to_api() for i in items], items[::-1][0].id if items else None

    def to_api(self):
        contexto = {'id': str(self.id),
                    'loja': self.loja.to_dict() if self.loja else None,
                    'descricao': self.descricao,
                    'texto_do_link': self.texto_link,
                    'chamada_promocional': self.texto_promocional,
                    'imagem': self.get_image(),
                    'compartilhamentos': self.total_visto,
                    'curtidas': self.total_curtido,
                    'categoria': [c.to_dict() for c in self.categoria.all()],
                    'expira': self.expira_str,
                    'titulo': self.nome,
                    'tipo': Oferta.TIPOS[self.tipo][1],
                    'inicio': _date(self.inicio, 'd/m/Y'),
                    'fim': _date(self.fim, 'd/m/Y'),
                    'fim_curto': _date(self.fim, 'd/m'),
                    'genero': self.GENEROS[self.genero][1],
                    'desconto': self.desconto,
                    'preco_final': self.preco_final,
                    'preco_inicial': self.preco_inicial}

        imagens = [{'maior': img.img_600x600.url,
                    'menor': img.img_94x94.url} for img in self.imagens.all()]

        contexto.update({'imagens': imagens})

        return contexto

    def to_dict(self, modal=False):
        imagem = None
        images = self.imagens.all()
        if self.tipo == Oferta.OFERTA:
            if images and images[0].imagem:
                imagem = images[0].img_172x172.url
        elif self.tipo == Oferta.EVENTO:
            if images:
                imagem = images[0].evento_180x445.url
        else:
            if images:
                imagem = images[0].img_376x376.url

        contexto =  {'id': str(self.id),
                     'unicode': self,
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
                     'titulo': self.nome,
                     'tipo': Oferta.TIPOS[self.tipo][1] if self.tipo else None,
                     'inicio': _date(self.inicio, 'd/m/Y'),
                     'fim': _date(self.fim, 'd/m/Y'),
                     'fim_curto': _date(self.fim, 'd/m'),
                     'genero': self.GENEROS[self.genero][1] if self.genero in [0,1,2,3] else None,
                     'porcentagem': self.porcentagem_desconto(),
                     'desconto': self.desconto}

        if not self.tipo == Oferta.EVENTO:
            contexto.update({'preco_final': self.preco_final,
                             'preco_inicial': self.preco_inicial,})

        if modal:
            imagens = [{'maior':img.img_600x600.url,
                        'menor':img.img_94x94.url} for img in images]
            contexto.update({'descricao': self.descricao,
                             'imagens': imagens})
        return contexto

    @classmethod
    def itens_por_shopping(cls, shopping=1):
        hoje = date.today()
        items = cls.objects.filter(status=cls.PUBLICADO) \
                           .filter(Q(loja__shopping_id=shopping) |
                                    Q(shopping_id=shopping)) \
                           .filter(inicio__lte=hoje, fim__gte=hoje) \
                           .order_by('-data_aprovacao')
        return items

    @classmethod
    def prontos(cls, tipo=0, from_id=None, shopping=1):
        hoje = date.today()
        if tipo == cls.DESTAQUE or tipo == cls.EVENTO:
            items = cls.objects.filter(shopping_id=shopping,tipo=tipo,status=cls.PUBLICADO,
                                       inicio__lte=hoje,fim__gte=hoje).order_by('-data_aprovacao')
        else:
            items = cls.objects.filter(loja__shopping_id=shopping,
                                       tipo=tipo,
                                       status=cls.PUBLICADO,
                                       inicio__lte=hoje,fim__gte=hoje) \
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

    @property
    def url(self):
        tipo = Oferta.TIPOS[self.tipo][1].lower()
        if self.shopping:
            shopping = self.shopping.slug
        elif self.loja:
            shopping = self.loja.shopping.slug
        else:
            return 'Sem url ainda'

        return '%s/%s#%s?%s' % (settings.SHARE_URL, shopping, tipo, self.slug)

    @classmethod
    def query_relatorio(cls, shopping_id, acao, tipo, date=None):
        if tipo == cls.EVENTO and not date:
            return Oferta.objects.annotate(vistas=Count('pk', only=Q(shopping=shopping_id,
                                                                     logs__acao=acao,
                                                                     tipo=tipo))).order_by('-vistas')
        elif tipo == cls.EVENTO and date:
            return Oferta.objects.annotate(vistas=Count('pk', only=Q(shopping=shopping_id,
                                                                     logs__acao=acao,
                                                                     logs__data_criacao__gte=date,
                                                                     tipo=tipo))).order_by('-vistas')
        elif not date:
            return Oferta.objects.annotate(vistas=Count('pk', only=Q(loja__shopping=shopping_id,
                                                                 logs__acao=acao,
                                                                 tipo=tipo))).order_by('-vistas')
        else:
            return Oferta.objects.annotate(vistas=Count('pk', only=Q(loja__shopping=shopping_id,
                                                                     logs__acao=acao,
                                                                     logs__data_criacao__gte=date,
                                                                     tipo=tipo))).order_by('-vistas')

    @classmethod
    def itens_mais(cls, shopping_id, acao, tipo):
        hoje = date.today()

        mais_vistas_query = cls.query_relatorio(shopping_id, acao, tipo)
        mes_query = cls.query_relatorio(shopping_id, acao, tipo, date=hoje + timedelta(days=-30))
        semana_query = cls.query_relatorio(shopping_id, acao, tipo, date=hoje + timedelta(days=-7))

        mais_vistas, total_vistas = listas_e_totais(mais_vistas_query, 'vistas')
        mais_do_mes, total_mes = listas_e_totais(mes_query, 'vistas')
        mais_da_semana, total_semana = listas_e_totais(semana_query, 'vistas')

        return {'tipo': cls.TIPOS[tipo][1],
                'nome_shopping': Shopping.objects.get(id=shopping_id).nome,
                'mais_vistas': mais_vistas, 'total_vistas': total_vistas,
                'mais_do_mes': mais_do_mes, 'total_mes': total_mes,
                'mais_da_semana': mais_da_semana, 'total_semana': total_semana}

    @classmethod
    def relatorio_filtrado(cls, shopping_id, acao, tipo, inicio, fim):
        if tipo == cls.EVENTO:
            return cls.objects.annotate(vistas=Count('pk', only=Q(shopping=shopping_id,
                                                                  logs__acao=acao,
                                                                  logs__data_criacao__gte=inicio,
                                                                  logs__data_criacao__lte=fim + timedelta(days=1),
                                                                  tipo=tipo))).order_by('-vistas')
        else:
            return cls.objects.annotate(vistas=Count('pk', only=Q(loja__shopping=shopping_id,
                                                              logs__acao=acao,
                                                              logs__data_criacao__gte=inicio,
                                                              logs__data_criacao__lte=fim + timedelta(days=1),
                                                              tipo=tipo))).order_by('-vistas')


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
        fname = '%s_%s' % (slugify(unicode(fname)), datetime.now().strftime("%Y%m%d%H%M%S"))
        return os.path.join('ofertas','%s.%s' % (fname, extension))

    oferta = models.ForeignKey(Oferta, verbose_name=u'Oferta',
                               related_name='imagens')
    imagem = models.ImageField(u'Imagem', upload_to=new_filename,
                               null=True, blank=True)
    img_600x600 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                  resize.ResizeToFill(600, 600)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})
    img_376x376 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(376, 376)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})
    img_250x250 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                  resize.ResizeToFill(250, 250)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})
    img_172x172 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(172, 172)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})
    img_120x120 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                  resize.ResizeToFill(120, 120)],
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
    img_250x250 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                  resize.ResizeToFill(250, 250)],
                                 source='imagem', format='PNG',
                                 options={'quality': 90})
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
    tipo = models.IntegerField(u'Tipo de categoria', choices=CATEGORIAS,
                               null=True, blank=False, default=NORMAL)
    categoria = models.ForeignKey(Categoria, null=True, blank=True,
                                  verbose_name=u'Categoria',
                                  related_name='mascaras')

    class Meta:
        verbose_name = u'Imagem para compartilhar'
        verbose_name_plural = u'Imagens para compartilhar'

    def __unicode__(self):
        return u'%s' % self.imagem

    @classmethod
    def normais_serializadas(cls):
        return [i.to_dict() for i in cls.objects.filter(tipo=cls.NORMAL,
                                                        publicada=True)]

    def to_dict(self):
        return {'id': self.id,
                'imagem': self.img_376x376.url,
                'thumb': self.thumb_98x98.url}

post_save.connect(cria_envia_notificacao, sender=Oferta)
post_save.connect(completa_slug, sender=Oferta)
post_save.connect(completa_slug, sender=Destaque)
post_save.connect(completa_slug, sender=Evento)
