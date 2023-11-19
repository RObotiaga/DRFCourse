from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import CustomUser


class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ('id', 'user_id',)
    ordering = ('user_id',)
    fieldsets = (
        (None, {'fields': ('user_id', 'password', 'is_active')}),
    )


admin.site.register(CustomUser, CustomUserAdmin)
