# -*- encoding: utf-8 -*-

from django.contrib import admin

from lojas.models import Loja, Shopping

class LojaAdmin(admin.ModelAdmin):
	list_display = ['nome','telefone','publicada']
	list_filter = ['publicada']
	list_editable = ['publicada']

class ShoppingAdmin(admin.ModelAdmin):
    list_display = ['nome','publicada','id_multiplan']
    prepopulated_fields = {'slug': ('nome',), }
    list_editable = ['publicada']
    list_filter = ['publicada']

admin.site.register(Loja, LojaAdmin)
admin.site.register(Shopping, ShoppingAdmin)
