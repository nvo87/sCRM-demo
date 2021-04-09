from django.contrib import admin

from clients.models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'phone')
    search_fields = ('last_name', 'phone')
