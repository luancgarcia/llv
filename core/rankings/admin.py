from django.contrib import admin

from models import Intervalo, Ponto

class PontoAdmin(admin.ModelAdmin):
    list_filter = ['loja__shopping']
    list_display = ['loja', 'total', 'intervalo']
    ordering = ['-total']

admin.site.register(Intervalo)
admin.site.register(Ponto, PontoAdmin)
