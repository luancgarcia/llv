# -*- encoding: utf-8 -*-

from django.contrib import admin

from geral.models import Categoria, Oferta, ImagemOferta, Log, Destaque, Evento

class CategoriaAdmin(admin.ModelAdmin):
    list_display = ['nome']


class OfertaAdmin(admin.ModelAdmin):
    exclude = ('tipo',)

    def queryset(self, request):
        qs = super(OfertaAdmin, self).queryset(request)
        return qs.filter(tipo=Oferta.OFERTA)

    def save_model(self, request, obj, form, change):
        obj.tipo = Oferta.OFERTA
        obj.save()


class DestaqueAdmin(admin.ModelAdmin):
    exclude = ('tipo',)

    def queryset(self, request):
        qs = super(DestaqueAdmin, self).queryset(request)
        return qs.filter(tipo=Oferta.DESTAQUE)

    def save_model(self, request, obj, form, change):
        obj.tipo = Oferta.DESTAQUE
        obj.save()


class EventoAdmin(admin.ModelAdmin):
    exclude = ('tipo',)

    def queryset(self, request):
        qs = super(EventoAdmin, self).queryset(request)
        return qs.filter(tipo=Oferta.EVENTO)

    def save_model(self, request, obj, form, change):
        obj.tipo = Oferta.EVENTO
        obj.save()


admin.site.register(Categoria)
admin.site.register(Oferta, OfertaAdmin)
admin.site.register(Destaque, DestaqueAdmin)
admin.site.register(Evento, EventoAdmin)
admin.site.register(ImagemOferta)
admin.site.register(Log)