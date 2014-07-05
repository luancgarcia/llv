# -*- encoding: utf-8 -*-

from django.contrib import admin

from geral.models import Categoria, Oferta, ImagemOferta, Log

class CategoriaAdmin(admin.ModelAdmin):
	list_display = ['nome']

admin.site.register(Categoria)
admin.site.register(Oferta)
admin.site.register(ImagemOferta)
admin.site.register(Log)