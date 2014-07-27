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

    class Meta:
        abstract = True


class OrderedModel(BaseModel):

    def save(self, *args, **kwargs):
        if not self.id:
            try:
                self.ordem = self.__class__.objects.all().order_by("-ordem")[0].ordem + 1
            except IndexError:
                self.ordem = 0
        super(OrderedModel, self).save()

    def order_link(self):
        model_type_id = ContentType.objects.get_for_model(self.__class__).id
        model_id = self.id
        kwargs = {"direction": "up", "model_type_id": model_type_id, "model_id": model_id}
        url_up = reverse("admin-move", kwargs=kwargs)
        kwargs["direction"] = "down"
        url_down = reverse("admin-move", kwargs=kwargs)
        return '<a href="%s">Sobe</a> - <a href="%s">Desce</a>' % (url_up, url_down)
    order_link.allow_tags = True
    order_link.short_description = 'Mover'
    order_link.admin_order_field = 'order'

    @staticmethod
    def move_down(model_type_id, model_id):
        try:
            ModelClass = ContentType.objects.get(id=model_type_id).model_class()

            lower_model = ModelClass.objects.get(id=model_id)
            higher_model = ModelClass.objects.filter(ordem__gt=lower_model.ordem)[0]

            lower_model.ordem, higher_model.ordem = higher_model.ordem, lower_model.ordem

            higher_model.save()
            lower_model.save()
        except IndexError:
            pass
        except ModelClass.DoesNotExist:
            pass

    @staticmethod
    def move_up(model_type_id, model_id):
        try:
            ModelClass = ContentType.objects.get(id=model_type_id).model_class()

            higher_model = ModelClass.objects.get(id=model_id)
            lower_model = ModelClass.objects.filter(ordem__lt=higher_model.ordem).order_by('-ordem')[0]

            lower_model.ordem, higher_model.ordem = higher_model.ordem, lower_model.ordem

            higher_model.save()
            lower_model.save()
        except IndexError:
            pass
        except ModelClass.DoesNotExist:
            pass

    ordem = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ["ordem"]
        abstract = True

