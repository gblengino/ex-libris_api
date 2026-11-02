from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Country

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    fieldsets = UserAdmin.fieldsets + (
        ('Información Adicional', {'fields': ('bio', 'country')}),
    )
    list_display = ('username', 'email', 'is_active', 'created_at', 'is_deleted')
    list_filter = ('is_deleted', 'country')
    search_fields = ('username', 'email')

    def get_queryset(self, request):
        return self.model.all_objects.get_queryset()

@admin.register(Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)