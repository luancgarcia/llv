# -*- encoding: utf-8 -*-

from django.contrib import admin

from lojas.models import Loja

class LojaAdmin(admin.ModelAdmin):
	list_display = ['nome','telefone','publicada']
	list_filter = ['publicada']
	list_editable = ['publicada']

admin.site.register(Loja, LojaAdmin)