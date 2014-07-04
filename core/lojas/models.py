# -*- encoding: utf-8 -*-

from django.db import models

from utils.models import EditorialModel, BaseManager


class Loja(EditorialModel):
    nome = models.CharField(u'Nome', max_length=100, null=True, blank=False)

    class Meta:
        verbose_name=u'Loja'
        verbose_name_plural=u'Lojas'
        ordering = ['nome']

    def __unicode__(self):
        return u'%s' % self.nome
