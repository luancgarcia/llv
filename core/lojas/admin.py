# -*- encoding: utf-8 -*-

from django.contrib import admin

from lojas.models import Loja, Shopping

class LojaAdmin(admin.ModelAdmin):
	list_display = ['nome','shopping','telefone','publicada']
	list_filter = ['shopping','publicada']
	list_editable = ['publicada']
	search_fields= ['nome']
	prepopulated_fields = {'slug': ('nome',), }

class ShoppingAdmin(admin.ModelAdmin):
    list_display = ['nome','publicada','id_multiplan']
    prepopulated_fields = {'slug': ('nome',), }
    list_editable = ['publicada']
    list_filter = ['publicada']

admin.site.register(Loja, LojaAdmin)
admin.site.register(Shopping, ShoppingAdmin)
