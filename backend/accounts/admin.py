from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


class UserAdmin(admin.ModelAdmin):
    list_display = ('login', 'email', 'phone', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('login', 'email', 'phone')
    ordering = ('login',)
    filter_horizontal = ('groups', 'user_permissions',)


admin.site.register(User, UserAdmin)
