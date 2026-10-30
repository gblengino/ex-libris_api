from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('bio', 'country')}),
    )
    list_display = ('username', 'email', 'is_active', 'created_at')
    list_filter = ('is_active', 'country')
    search_fields = ('username', 'email')