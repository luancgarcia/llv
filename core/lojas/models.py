# -*- encoding: utf-8 -*-

from imagekit.models import ImageSpecField
from pilkit.processors import Adjust, resize

from django.db import models
from django.utils.text import slugify

from utils.models import EditorialModel, BaseManager


class Shopping(EditorialModel):
    nome = models.CharField(u'Nome', max_length=100, blank=False, null=True)
    slug = models.SlugField(max_length=150, blank=False, null=False, unique=True)
    id_multiplan = models.IntegerField(u'id do shopping na multiplan', null=True, blank=True)

    class Meta:
        verbose_name=u'Shopping'
        verbose_name_plural=u'Shoppings'
        ordering = ['nome']

    def __unicode__(self):
        return u'%s' % self.nome

    def to_dict(self):
        return {'nome': self.nome,
                'slug': self.slug,
                'id_multiplan': self.id_multiplan}


class Loja(EditorialModel):
    def new_filename(instance, filename):
        fname, dot, extension = filename.rpartition('.')
        fname = slugify(fname)
        return os.path.join('lojas','%s.%s' % (fname, extension))

    shopping = models.ForeignKey(Shopping, verbose_name=u'Shopping', related_name='lojas')
    nome = models.CharField(u'Nome', max_length=100, null=True, blank=False)
    slug = models.CharField(u'Slug', max_length=150, null=True, blank=True)
    logo = models.ImageField(u'Imagem', upload_to=new_filename,
                               null=True, blank=True)
    logo_120x50 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(120, 50)],
                                 source='logo', format='PNG',
                                 options={'quality': 90})
    telefone = models.CharField(u'telefone', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name=u'Loja'
        verbose_name_plural=u'Lojas'
        ordering = ['nome']

    def __unicode__(self):
        return u'%s - %s' % (self.nome, self.shopping)

    def to_dict(self):
        return {'id': self.id,
                'nome': self.nome,
                'slug': self.slug,
                'logo': self.logo_120x50.url if self.logo else None,
                'telefone': self.telefone,
                'shopping': self.shopping.to_dict()}

    @classmethod
    def publicadas_com_oferta(cls):
        lojas = cls.objects.filter(shopping=1,publicada=True).order_by('nome')
        return [l.to_dict() for l in lojas if l.ofertas.filter(status=1)]

    @classmethod
    def publicadas_sem_oferta(cls):
        lojas = cls.objects.filter(shopping=1,publicada=True).order_by('nome')
        return [l.to_dict() for l in lojas if not l.ofertas.filter(status=1)]
