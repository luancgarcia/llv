# -*- encoding: utf-8 -*-
from django.contrib import admin

from models import ApiUser, ApiSession, ApiLog

class ApiUserAdmin(admin.ModelAdmin):
    readonly_fields = ['token']
    list_display = ['nome', 'email']
    list_filter = ['shopping']


class ApiSessionAdmin(admin.ModelAdmin):
    list_display = ['user', 'inicio', 'fim']


class ApiLogAdmin(admin.ModelAdmin):
    list_display = ['sessao', 'tipo_de_log']
    list_filter = ['tipo',]

admin.site.register(ApiUser, ApiUserAdmin)
admin.site.register(ApiSession, ApiSessionAdmin)
admin.site.register(ApiLog, ApiLogAdmin)
