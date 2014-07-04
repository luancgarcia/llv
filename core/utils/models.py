# -*- encoding: utf-8 -*-

from django.db import models

__all__ = ['BaseModel', 'EditorialModel', 'BaseManager']


class BaseManager(models.Manager):
    """
    extends the default django manager to include a method that returns
    none if the given model doesn't exists.
    """
    def get_or_none(self, **kwargs):
        try:
            if 'related_models' not in kwargs:
                return self.get(**kwargs)
            else:
                if 'related_models' in kwargs:
                    related = kwargs['related_models']
                    del kwargs['related_models']
                else:
                    related = tuple()
                self.select_related(*related).get(kwargs)
        except self.model.DoesNotExist:
            return None


class BaseModel(models.Model):
    u'''
    BaseModel é uma classe abstrata de modelo de campos de
    básicos como controle de data e hora de atualização e criação que
    todos as entidades do sistema devem possuir.'''

    data_criacao = models.DateTimeField(
        u"data da criação", auto_now_add=True, editable=False
    )
    data_atualizacao = models.DateTimeField(
        u"data da atualização", auto_now=True, auto_now_add=True,
        editable=False
    )

    objects = BaseManager()

    class Meta:
        abstract = True


class EditorialModel(BaseModel):
    '''
    Extende BaseModel para ter campos de controle comuns a situacao editorial
    '''
    publicada = models.BooleanField(u'Publicada', default=False)

