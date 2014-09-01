# -*- encoding: utf-8 -*-

from imagekit.admin import AdminThumbnail

from django.contrib import admin
from django.forms import ModelForm

from geral.models import (Categoria, Oferta, ImagemOferta, Log, Destaque, Evento,
                          Mascara, PerfilMarketing, PerfilLojista, PerfilAdministrador,
                          Sazonal)
from lojas.models import Loja


OCULTA_NO_ADMIN = ('tipo','evento','data_aprovacao','publicada','autor','texto_link')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome','shopping','publicada']
    prepopulated_fields = {'slug': ('nome',), }
    exclude = ['sazonal','imagem']
    list_editable = ['publicada']
    list_filter = ['publicada','shopping']

    def queryset(self, request):
        qs = super(CategoriaAdmin, self).queryset(request)
        return qs.filter(sazonal=False)


class SazonalAdmin(admin.ModelAdmin):
    list_display = ['nome','shopping','publicada']
    prepopulated_fields = {'slug': ('nome',), }
    exclude = ['sazonal','imagem']
    list_editable = ['publicada']
    list_filter = ['publicada','shopping']
    def queryset(self, request):
        qs = super(SazonalAdmin, self).queryset(request)
        return qs.filter(sazonal=True)


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


class OfertaModelForm(ModelForm):
    class Meta:
        model = Oferta
        localized_fields = ('__all__')

class OfertaAdmin(admin.ModelAdmin):
    inlines = [ImagemInline,]
    exclude = OCULTA_NO_ADMIN
    prepopulated_fields = {'slug': ('nome',), }
    list_filter = ['loja', 'status','genero']
    readonly_fields = ('total_compartilhado', 'total_visto', 'total_curtido',
                       'desconto_value', 'autor')

    class Media:
        js = [
            'js/preco_desconto_admin.js',
            'js/jquery.maskMoney.min.js',
        ]

    def queryset(self, request):
        qs = super(OfertaAdmin, self).queryset(request)
        perfil = request.user.perfil.get()
        if perfil.is_lojista:
            qs = qs.filter(loja=perfil.loja)
        return qs.filter(tipo=Oferta.OFERTA)

    def changelist_view(self, request, extra_context=None):
        self.list_display = ('__unicode__',)
        perfil = request.user.perfil.get()
        if perfil.is_lojista:
            self.list_display = self.list_display + ('status_string',)
            self.list_editable = None
        else:
            self.list_display = self.list_display + ('status','autor')
            self.list_editable = ('status',)
        return super(OfertaAdmin, self).changelist_view(request, extra_context)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        if db_field.name == "loja":
            if perfil.is_lojista:
                kwargs["queryset"] = Loja.objects.filter(id=perfil.loja.id)
            elif perfil.is_marketing:
                kwargs["queryset"] = Loja.objects.filter(shopping=perfil.shopping)
            else:
                kwargs["queryset"] = Loja.objects.all()
        return super(OfertaAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        perfil = request.user.perfil.get()
        if db_field.name == "categoria" and perfil.shopping:
            kwargs["queryset"] = Categoria.objects.filter(shopping=perfil.shopping)
        return super(OfertaAdmin, self).formfield_for_manytomany(db_field, request, **kwargs)

    def get_fieldsets(self, request, obj=None):
        fieldsets = super(OfertaAdmin, self).get_fieldsets(request, obj)
        perfil = request.user.perfil.get()

        if not perfil.is_lojista and not perfil.is_marketing:
            fieldsets = (
                ('Dados', {
                    'fields': ('total_visto','total_curtido', 'total_compartilhado','autor')
                }),
                ('Informações', {
                    'fields': ('status','loja','nome','slug','categoria','genero',
                               'descricao', 'texto_promocional',)
                }),
                ('Digite os valores do produto', {
                    'fields': (('preco_inicial','preco_final'),'desconto')
                }),
            )
        elif not perfil.is_lojista:
            fieldsets = (
                ('Informações', {
                    'fields': ('status','loja','nome','slug','categoria','genero',
                               'descricao', 'texto_promocional',)
                }),
                ('Digite os valores do produto', {
                    'fields': (('preco_inicial','preco_final'),'desconto')
                }),
            )
        else:
            fieldsets = (
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


class DestaqueAdmin(admin.ModelAdmin):
    inlines = [ImagemNaoOfertaInline,]
    exclude = OCULTA_NO_ADMIN
    prepopulated_fields = {'slug': ('nome',), }
    list_display = ['__unicode__','status']
    list_editable = ['status']

    class Media:
        js = [
            'js/preco_desconto_admin.js',
            'js/jquery.maskMoney.min.js',
        ]

    fieldsets = (
        ('Informações', {
            'fields': (
                'status', 'loja', 'nome', 'slug', 'categoria', 'genero',
                'descricao', 'texto_promocional',)
        }),
        ('Digite os valores do produto', {
            'fields': (('preco_inicial', 'preco_final'), 'desconto')
        }),
    )

    def queryset(self, request):
        qs = super(DestaqueAdmin, self).queryset(request)
        return qs.filter(tipo=Oferta.DESTAQUE)

    def save_model(self, request, obj, form, change):
        obj.tipo = Oferta.DESTAQUE
        obj.save()


class EventoAdmin(admin.ModelAdmin):
    inlines = [ImagemNaoOfertaInline,]
    exclude = OCULTA_NO_ADMIN + ('preco_inicial','preco_final','desconto')
    prepopulated_fields = {'slug': ('nome',), }
    list_display = ['nome','genero','status']
    list_editable = ['status']
    list_display_links = ['nome','genero']

    class Media:
        js = [
            'js/preco_desconto_admin.js',
            'js/jquery.maskMoney.min.js',
        ]

    def queryset(self, request):
        qs = super(EventoAdmin, self).queryset(request)
        return qs.filter(tipo=Oferta.EVENTO)

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
    list_filter = ['acao','oferta__tipo']
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
admin.site.register(Oferta, OfertaAdmin, form=OfertaModelForm)
admin.site.register(Destaque, DestaqueAdmin, form=OfertaModelForm)
admin.site.register(Evento, EventoAdmin, form=OfertaModelForm)
admin.site.register(ImagemOferta, ImagemOfertaAdmin)
admin.site.register(Log, LogAdmin)
admin.site.register(PerfilMarketing, PerfilMktAdmin)
admin.site.register(PerfilLojista, PerfilLojistaAdmin)
admin.site.register(Mascara, MascaraAdmin)
admin.site.register(PerfilAdministrador, PerfilAdministradorAdmin)
admin.site.register(Sazonal, SazonalAdmin)
