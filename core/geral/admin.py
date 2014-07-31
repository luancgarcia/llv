# -*- encoding: utf-8 -*-

from django.contrib import admin

from geral.models import Categoria, Oferta, ImagemOferta, Log, Destaque, Evento


OCULTA_NO_ADMIN = ('tipo','evento','data_aprovacao','publicada')

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome','publicada']
    prepopulated_fields = {'slug': ('nome',), }
    exclude = ['default']
    list_editable = ['publicada']
    list_filter = ['publicada']


class ImagemInline(admin.StackedInline):
    classes = ('grp-collapse grp-open',)
    inline_classes = ('grp-collapse grp-open',)
    model = ImagemOferta
    exclude = ('principal','vertical')
    extra = 1
    fieldsets = (
        ('', {
            'fields': (('imagem','ordem'),)
        }),
    )

class OfertaAdmin(admin.ModelAdmin):
    inlines = [ImagemInline,]
    exclude = OCULTA_NO_ADMIN
    prepopulated_fields = {'slug': ('nome',), }
    list_filter = ['loja', 'status']
    list_display = ['__unicode__','status']
    readonly_fields = ['desconto']

    fieldsets = (
        ('Informações', {
            'fields': ('loja','nome','slug', 'descricao',
                       'texto_promocional', 'texto_link',)
        }),
        ('Digite os valores do produto', {
            'fields': (('preco_inicial','preco_final'),'desconto')
        }),
    )

    # class Media:
        # js = []

    def queryset(self, request):
        qs = super(OfertaAdmin, self).queryset(request)
        return qs.filter(tipo=Oferta.OFERTA)

    def save_model(self, request, obj, form, change):
        obj.tipo = Oferta.OFERTA
        # apagar quando implementar o js
        if obj.preco_final and obj.preco_inicial:
            antes = float(obj.preco_inicial.replace(',','.'))
            depois = float(obj.preco_final.replace(',','.'))
            obj.desconto = int(100-(100*int(depois)/int(antes)))
        obj.save()


class DestaqueAdmin(admin.ModelAdmin):
    inlines = [ImagemInline,]
    exclude = OCULTA_NO_ADMIN
    prepopulated_fields = {'slug': ('nome',), }

    def queryset(self, request):
        qs = super(DestaqueAdmin, self).queryset(request)
        return qs.filter(tipo=Oferta.DESTAQUE)

    def save_model(self, request, obj, form, change):
        obj.tipo = Oferta.DESTAQUE
        if obj.preco_final and obj.preco_inicial:
            antes = float(obj.preco_inicial.replace(',','.'))
            depois = float(obj.preco_final.replace(',','.'))
            obj.desconto = int(100-(100*int(depois)/int(antes)))
        obj.save()


class EventoAdmin(admin.ModelAdmin):
    inlines = [ImagemInline,]
    exclude = OCULTA_NO_ADMIN
    prepopulated_fields = {'slug': ('nome',), }

    def queryset(self, request):
        qs = super(EventoAdmin, self).queryset(request)
        return qs.filter(tipo=Oferta.EVENTO)

    def save_model(self, request, obj, form, change):
        obj.tipo = Oferta.EVENTO
        if obj.preco_final and obj.preco_inicial:
            antes = float(obj.preco_inicial.replace(',','.'))
            depois = float(obj.preco_final.replace(',','.'))
            obj.desconto = int(100-(100*int(depois)/int(antes)))
        obj.save()


class ImagemOfertaAdmin(admin.ModelAdmin):
    list_display = ['oferta','ordem','order_link',]
    exclude = ['principal','vertical']


admin.site.register(Categoria, CategoriaAdmin)
admin.site.register(Oferta, OfertaAdmin)
admin.site.register(Destaque, DestaqueAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(ImagemOferta, ImagemOfertaAdmin)
admin.site.register(Log)