# -*- encoding: utf-8 -*-
from django.contrib import admin

from models import ApiUser, ApiSession, ApiLog

class ApiUserAdmin(admin.ModelAdmin):
    readonly_fields = ['token']
    list_display = ['nome', 'email', 'shopping']
    list_filter = ['shopping']


admin.site.register(ApiUser, ApiUserAdmin)
admin.site.register(ApiSession)
admin.site.register(ApiLog)
