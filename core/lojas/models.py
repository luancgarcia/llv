# -*- encoding: utf-8 -*-

from imagekit.models import ImageSpecField
from pilkit.processors import Adjust, resize

from django.db import models

from utils.models import EditorialModel, BaseManager


class Loja(EditorialModel):
    nome = models.CharField(u'Nome', max_length=100, null=True, blank=False)
    logo = models.CharField(u'Logo', max_length=100, null=True, blank=True)
    logo = models.ImageField(u'Imagem', upload_to='lojas',
                               null=True, blank=True)
    logo_120x50 = ImageSpecField([Adjust(contrast=1.1, sharpness=1.1),
                                 resize.ResizeToFill(120, 50)],
                                 source='logo', format='JPG',
                                 options={'quality': 90})
    telefone = models.CharField(u'telefone', max_length=100, null=True, blank=True)

    class Meta:
        verbose_name=u'Loja'
        verbose_name_plural=u'Lojas'
        ordering = ['nome']

    def __unicode__(self):
        return u'%s' % self.nome
