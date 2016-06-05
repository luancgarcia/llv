# -*- encoding: utf-8 -*-
from imagekit.admin import AdminThumbnail

from django.contrib import admin
from django.forms import ModelForm
from django.forms.models import BaseInlineFormSet
from django.core.exceptions import ValidationError
from django.db.models import Q

from geral.models import (Categoria, Oferta, ImagemOferta, Log, Destaque, Evento,
                          Mascara, PerfilMarketing, PerfilLojista, PerfilAdministrador,
                          Sazonal, Cupom)
from lojas.models import Loja, Shopping


OCULTA_NO_ADMIN = ('tipo', 'evento', 'data_aprovacao', 'publicada', 'autor', 'texto_link', 'subtipo')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome','shopping','publicada']
    prepopulated_fields = {'slug': ('nome',), }
    exclude = ['sazonal','imagem']
    list_editable = ['publicada']
    list_filter = ['publicada','shopping']

    def queryset(self, request):
        qs = super(CategoriaAdmin, self).queryset(request)
        perfil = request.user.perfil.get()
        if not perfil.is_adm:
            loja_shopping = None
            if perfil.loja:
                loja_shopping = perfil.loja.shopping
            qs = qs.filter(
                Q(shopping=perfil.shopping) | Q(shopping=loja_shopping)
            )
        return qs.filter(sazonal=False)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        if db_field.name == "shopping":
            kwargs["queryset"] = Shopping.objects.filter(id=perfil.shopping_id)

        return super(CategoriaAdmin, self).formfield_for_foreignkey(db_field,
                                                                    request,
                                                                    **kwargs)


class SazonalAdmin(admin.ModelAdmin):
    list_display = ['nome','shopping','publicada']
    prepopulated_fields = {'slug': ('nome',), }
    exclude = ['sazonal','imagem']
    list_editable = ['publicada']
    list_filter = ['publicada','shopping']
    def queryset(self, request):
        qs = super(SazonalAdmin, self).queryset(request)
        perfil = request.user.perfil.get()
        if not perfil.is_adm:
            loja_shopping = None
            if perfil.loja:
                loja_shopping = perfil.loja.shopping
            qs = qs.filter(
                Q(shopping=perfil.shopping) | Q(shopping=loja_shopping)
            )
        return qs.filter(sazonal=True)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        if db_field.name == "shopping":
            kwargs["queryset"] = Shopping.objects.filter(id=perfil.shopping_id)
        return super(SazonalAdmin, self).formfield_for_foreignkey(db_field,
                                                                  request,
                                                                  **kwargs)


class ImagemInlineFormSet(BaseInlineFormSet):
    def clean(self):
        total_forms = self.total_form_count()
        imgs_instancia = self.instance.imagens.all().count()
        mensagem = u'Deve haver, no mínimo, 1 imagem para validar'
        if not self.instance.status == 3:
            if not total_forms:
                raise ValidationError({'status': [mensagem]})
            elif not self.files and not imgs_instancia >= 1:
                raise ValidationError({'status': [mensagem]})
            elif total_forms == 1:
                if self.data.get('imagens-0-imagem-clear') == 'on' or\
                   self.cleaned_data[0]['DELETE']:
                    raise ValidationError({'status': [mensagem]})

        super(ImagemInlineFormSet, self).clean()


class ImagemInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    model = ImagemOferta
    exclude = ('principal','vertical')
    extra = 0
    max_num = 3
    fieldsets = (
        ('', {
            'fields': (('imagem','ordem'),)
        }),
    )
    formset = ImagemInlineFormSet


class ImagemNaoOfertaInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    model = ImagemOferta
    exclude = ('principal','vertical')
    extra = 1
    max_num = 1
    fieldsets = (
        ('', {
            'fields': (('imagem','ordem'),)
        }),
    )
    formset = ImagemInlineFormSet


class ItemModelForm(ModelForm):
    class Meta:
        model = Oferta
        localized_fields = ('__all__')


class OfertaModelForm(ItemModelForm):
    def clean_loja(self):
        loja = self.cleaned_data['loja']
        if not loja:
            raise ValidationError({'loja': ["Selecione uma loja", ]})
        return loja

    def clean_genero(self):
        genero = self.cleaned_data['genero']
        if genero == None:
            raise ValidationError({'genero': [u'Informe o gênero']})
        return genero

    def clean_categoria(self):
        categoria = self.cleaned_data['categoria']
        if not categoria:
            raise ValidationError({'categoria': [u'Informe ao menos uma categoria']})
        return categoria

    def clean_descricao(self):
        descricao = self.cleaned_data['descricao']
        if not descricao:
            raise ValidationError({'descricao': [u'Informe a descrição']})
        return descricao


class OfertaAdmin(admin.ModelAdmin):
    inlines = [ImagemInline,]
    exclude = OCULTA_NO_ADMIN + ('shopping',)
    prepopulated_fields = {'slug': ('nome',), }
    list_filter = ['loja__shopping', 'loja', 'status','genero']
    readonly_fields = ('total_compartilhado', 'total_visto', 'total_curtido',
                       'desconto_value', 'autor','url',)
    search_fields = ['nome']
    form = OfertaModelForm

    class Media:
        js = [
            'js/preco_desconto_admin.js',
            'js/comum_admin.js',
            'js/jquery.maskMoney.min.js',
        ]

    def queryset(self, request):
        qs = super(OfertaAdmin, self).queryset(request)
        perfil = request.user.perfil.get()
        if perfil.is_lojista:
            qs = qs.filter(loja=perfil.loja)
        if perfil.is_marketing and perfil.shopping:
            qs = qs.filter(Q(loja__shopping=perfil.shopping)|
                           Q(autor__shopping=perfil.shopping))
        return qs.filter(tipo=Oferta.OFERTA)

    def changelist_view(self, request, extra_context=None):
        self.list_display = ('__unicode__',)
        perfil = request.user.perfil.get()
        if perfil.is_lojista:
            self.list_display = self.list_display + ('status_string',)
            self.list_editable = None
        else:
            self.list_display = self.list_display + ('status', 'autor',)
            self.list_editable = ('status',)

        self.list_display = self.list_display + ('url',)
        return super(OfertaAdmin, self).changelist_view(request, extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        if db_field.name == "loja":
            if perfil.is_lojista:
                kwargs["queryset"] = Loja.objects.filter(id=perfil.loja.id)
            elif perfil.is_marketing and perfil.shopping:
                kwargs["queryset"] = Loja.objects.filter(shopping=perfil.shopping)
            else:
                kwargs["queryset"] = Loja.objects.all()
        return super(OfertaAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        loja_shopping = None
        if perfil.loja:
            loja_shopping = perfil.loja.shopping
        if db_field.name == "categoria" and (perfil.shopping or loja_shopping):
            kwargs["queryset"] = Categoria.objects.filter(
                                                   Q(shopping=perfil.shopping) |
                                                   Q(shopping=loja_shopping)
                                                   )
        return super(OfertaAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(OfertaAdmin, self).get_fieldsets(request, obj)
        perfil = request.user.perfil.get()

        if not perfil.is_lojista and not perfil.is_marketing:
            fieldsets = (
                ('Dados', {
                    'fields': ('total_visto','total_curtido', 'total_compartilhado','autor', 'url',)
                }),
                ('Datas', {
                    'fields': ('inicio','fim')
                }),
                ('Informações', {
                    'fields': ('status', 'razao', 'loja', 'nome', 'slug', 'categoria', 'genero',
                               'descricao', 'texto_promocional',)
                }),
                ('Digite os valores do produto', {
                    'fields': (('preco_inicial','preco_final'),'desconto')
                }),
            )
        elif not perfil.is_lojista:
            fieldsets = (
                ('Datas', {
                    'fields': ('inicio', 'fim')
                }),
                ('Informações', {
                    'fields': ('status', 'razao', 'loja', 'nome', 'slug', 'categoria', 'genero',
                               'descricao', 'texto_promocional',)
                }),
                ('Digite os valores do produto', {
                    'fields': (('preco_inicial','preco_final'),'desconto')
                }),
            )
        else:
            fieldsets = (
                ('Datas', {
                    'fields': ('inicio', 'fim')
                }),
                ('Informações', {
                        'fields': ('loja', 'nome', 'slug', 'categoria', 'genero',
                                   'descricao', 'texto_promocional',)
                }),
                ('Digite os valores do produto', {
                    'fields': (('preco_inicial','preco_final'),'desconto')
                }),
            )
        return fieldsets

    def save_model(self, request, obj, form, change):
        perfil = request.user.perfil.get()
        if not obj.autor:
            obj.autor = perfil
        if perfil.is_lojista:
            obj.status = Oferta.PENDENTE
        obj.tipo = Oferta.OFERTA
        obj.save()


class DestaqueModelForm(ModelForm):
    class Meta:
        model = Destaque
        localized_fields = ('__all__')


class DestaqueAdmin(admin.ModelAdmin):
    inlines = [ImagemNaoOfertaInline, ]
    exclude = OCULTA_NO_ADMIN
    # prepopulated_fields = {'slug': ('nome',), }
    list_display = ['__unicode__', 'shopping', 'status']
    list_editable = ['status']
    search_fields = ['nome']
    form = DestaqueModelForm
    list_filter = ['shopping', 'status']

    class Media:
        js = [
            'js/preco_desconto_admin.js',
            'js/jquery.maskMoney.min.js',
            'js/comum_admin.js',
        ]

    fieldsets = (
        ('Datas', {
            'fields': ('inicio', 'fim')
        }),
        ('Informações', {
            'fields': (
                'status', 'loja', 'shopping', 'nome', 'slug', 'categoria',
                'genero', 'descricao', 'texto_promocional',)
        }),
        ('Digite os valores do produto', {
            'fields': (('preco_inicial', 'preco_final'), 'desconto')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        if db_field.name == "loja":
            if perfil.is_marketing and perfil.shopping:
                kwargs["queryset"] = Loja.objects.filter(
                    shopping=perfil.shopping)
            else:
                kwargs["queryset"] = Loja.objects.all()
        if db_field.name == "shopping":
            if perfil.is_marketing and perfil.shopping:
                kwargs["queryset"] = Shopping.objects.filter(id=perfil.shopping.id)
            else:
                kwargs["queryset"] = Shopping.objects.all()
        return super(DestaqueAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        loja_shopping = perfil.loja.shopping if perfil.loja else None
        if db_field.name == "categoria" and (perfil.shopping or loja_shopping):
            kwargs["queryset"] = Categoria.objects.filter(
                Q(shopping=perfil.shopping) |
                Q(shopping=loja_shopping)
            )
        return super(DestaqueAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def queryset(self, request):
        qs = super(DestaqueAdmin, self).queryset(request)
        qs = qs.filter(tipo=Oferta.DESTAQUE)
        perfil = request.user.perfil.get()
        if perfil.is_lojista:
            qs = qs.filter(loja=perfil.loja)
        if perfil.is_marketing and perfil.shopping:
            qs = qs.filter(Q(shopping=perfil.shopping) |
                           Q(loja__shopping=perfil.shopping) |
                           Q(autor__shopping=perfil.shopping))
        return qs

    def save_model(self, request, obj, form, change):
        obj.tipo = Oferta.DESTAQUE
        obj.save()


class CupomModelForm(ModelForm):
    class Meta:
        model = Cupom
        localized_fields = ('__all__')

    def __init__(self, *args, **kwargs):
        super(CupomModelForm, self).__init__(*args, **kwargs)

        self.fields['loja'].required = True


class CupomAdmin(admin.ModelAdmin):
    inlines = [ImagemNaoOfertaInline, ]
    exclude = OCULTA_NO_ADMIN
    # prepopulated_fields = {'slug': ('nome',), }
    list_display = ['__unicode__', 'shopping', 'status']
    list_editable = ['status']
    search_fields = ['nome']
    form = CupomModelForm
    list_filter = ['shopping', 'status']

    class Media:
        js = [
            'js/preco_desconto_admin.js',
            'js/jquery.maskMoney.min.js',
            'js/comum_admin.js',
        ]

    fieldsets = (
        ('Datas', {
            'fields': ('inicio', 'fim')
        }),
        ('Informações', {
            'fields': (
                'status', 'loja', 'shopping', 'nome', 'slug', 'categoria',
                'genero', 'descricao', 'texto_promocional',)
        }),
        ('Digite os valores do produto', {
            'fields': (('preco_inicial', 'preco_final'), 'desconto')
        }),
    )

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        if db_field.name == "loja":
            if perfil.is_marketing and perfil.shopping:
                kwargs["queryset"] = Loja.objects.filter(
                    shopping=perfil.shopping)
            else:
                kwargs["queryset"] = Loja.objects.all()
        if db_field.name == "shopping":
            if perfil.is_marketing and perfil.shopping:
                kwargs["queryset"] = Shopping.objects.filter(id=perfil.shopping.id)
            else:
                kwargs["queryset"] = Shopping.objects.all()
        return super(CupomAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        loja_shopping = perfil.loja.shopping if perfil.loja else None
        if db_field.name == "categoria" and (perfil.shopping or loja_shopping):
            kwargs["queryset"] = Categoria.objects.filter(
                Q(shopping=perfil.shopping) |
                Q(shopping=loja_shopping)
            )
        return super(CupomAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def queryset(self, request):
        qs = super(CupomAdmin, self).queryset(request)
        qs = qs.filter(tipo=Oferta.DESTAQUE, subtipo=Oferta.CUPOM)
        perfil = request.user.perfil.get()
        if perfil.is_lojista:
            qs = qs.filter(loja=perfil.loja)
        if perfil.is_marketing and perfil.shopping:
            qs = qs.filter(Q(shopping=perfil.shopping) |
                           Q(loja__shopping=perfil.shopping) |
                           Q(autor__shopping=perfil.shopping))
        return qs

    def save_model(self, request, obj, form, change):
        obj.tipo = Oferta.DESTAQUE
        obj.subtipo = Oferta.CUPOM
        obj.save()


class EventoModelForm(ModelForm):
    class Meta:
        model = Destaque
        localized_fields = ('__all__')


class EventoAdmin(admin.ModelAdmin):
    inlines = [ImagemNaoOfertaInline,]
    exclude = OCULTA_NO_ADMIN + ('preco_inicial','preco_final','desconto')
    # prepopulated_fields = {'slug': ('nome',), }
    list_display = ['nome','genero','status']
    list_editable = ['status']
    list_display_links = ['nome','genero']
    search_fields = ['nome']
    list_filter = ['shopping', 'status']
    form = EventoModelForm

    fieldsets = (
        ('Datas', {
            'fields': ('inicio', 'fim')
        }),
        ('Informações', {
            'fields': (
                'status', 'loja', 'shopping', 'nome', 'slug', 'categoria',
                'genero', 'descricao', 'texto_promocional',)
        }),
    )

    class Media:
        js = [
            'js/preco_desconto_admin.js',
            'js/jquery.maskMoney.min.js',
            'js/comum_admin.js',
        ]

    def queryset(self, request):
        qs = super(EventoAdmin, self).queryset(request)
        perfil = request.user.perfil.get()
        if perfil.is_lojista:
            qs = qs.filter(loja=perfil.loja)
        if perfil.is_marketing and perfil.shopping:
            qs = qs.filter(Q(shopping=perfil.shopping) |
                           Q(loja__shopping=perfil.shopping) |
                           Q(autor__shopping=perfil.shopping))
        return qs.filter(tipo=Oferta.EVENTO)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        if db_field.name == "loja":
            if perfil.is_marketing and perfil.shopping:
                kwargs["queryset"] = Loja.objects.filter(
                    shopping=perfil.shopping)
            else:
                kwargs["queryset"] = Loja.objects.all()
        if db_field.name == "shopping":
            if perfil.is_marketing and perfil.shopping:
                kwargs["queryset"] = Shopping.objects.filter(
                    id=perfil.shopping.id)
            else:
                kwargs["queryset"] = Shopping.objects.all()
        return super(EventoAdmin, self).formfield_for_foreignkey(db_field,
                                                                 request,
                                                                 **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        loja_shopping = None
        if perfil.loja:
            loja_shopping = perfil.loja.shopping
        if db_field.name == "categoria" and (perfil.shopping or loja_shopping):
            kwargs["queryset"] = Categoria.objects.filter(
                Q(shopping=perfil.shopping) |
                Q(shopping=loja_shopping)
            )
        return super(EventoAdmin, self).formfield_for_manytomany(db_field,
                                                                   request,
                                                                   **kwargs)

    def save_model(self, request, obj, form, change):
        obj.tipo = Oferta.EVENTO
        obj.save()


class ImagemOfertaAdmin(admin.ModelAdmin):
    list_display = ['oferta','ordem','order_link',]
    exclude = ['principal','vertical']


class PerfilMktAdmin(admin.ModelAdmin):
    list_display = ['__unicode__','shopping']
    exclude = ['loja','tipo']
    list_filter = ['shopping__nome']

    def queryset(self, request):
        qs = super(PerfilMktAdmin, self).queryset(request)
        return qs.filter(tipo=PerfilMarketing.MARKETING)

    def save_model(self, request, obj, form, change):
        obj.tipo = PerfilMarketing.MARKETING
        obj.save()


class PerfilLojistaAdmin(admin.ModelAdmin):
    list_display = ['__unicode__','loja']
    exclude = ['shopping','tipo']
    list_filter = ['loja__shopping']

    def queryset(self, request):
        qs = super(PerfilLojistaAdmin, self).queryset(request)
        return qs.filter(tipo=PerfilMarketing.LOJISTA)

    def save_model(self, request, obj, form, change):
        obj.tipo = PerfilMarketing.LOJISTA
        obj.save()


class PerfilAdministradorAdmin(admin.ModelAdmin):
    list_display = ['__unicode__',]

    def queryset(self, request):
        qs = super(PerfilAdministradorAdmin, self).queryset(request)
        return qs.filter(tipo=PerfilAdministrador.ADMINISTRADOR)

    def save_model(self, request, obj, form, change):
        obj.tipo = PerfilAdministrador.ADMINISTRADOR
        obj.save()


class LogAdmin(admin.ModelAdmin):
    list_display = ['__unicode__','data_criacao']
    list_filter = ['acao','oferta__tipo', 'oferta__loja__shopping']
    exclude = ['tipo','shopping','loja']


class MascaraAdmin(admin.ModelAdmin):
    miniatura = AdminThumbnail(image_field='thumb_98x98')
    list_display = ['__unicode__','miniatura','tipo','categoria']
    list_filter = ['categoria','tipo']
    fieldsets = (
        ('', {
            'fields': ('tipo', 'publicada',)
        }),
        ('', {
            'fields': ('categoria',)
        }),
        ('Imagem', {
            'fields': ('imagem',)
        }),
        ('Thumbnail', {
            'fields': ('thumb',)
        }),
    )


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Oferta, OfertaAdmin)
admin.site.register(Destaque, DestaqueAdmin)
admin.site.register(Cupom, CupomAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(ImagemOferta, ImagemOfertaAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(PerfilMarketing, PerfilMktAdmin)
admin.site.register(PerfilLojista, PerfilLojistaAdmin)
admin.site.register(Mascara, MascaraAdmin)
admin.site.register(PerfilAdministrador, PerfilAdministradorAdmin)
admin.site.register(Sazonal, SazonalAdmin)
