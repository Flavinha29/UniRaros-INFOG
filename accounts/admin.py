# accounts/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, Paciente  # ✅ SÓ CustomUser (Paciente não existe)

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
    list_display = ['username', 'email', 'user_type', 'status', 'is_staff']
    list_filter = ['user_type', 'status', 'is_staff']
    fieldsets = UserAdmin.fieldsets + (
        ('Informações Adicionais', {
            'fields': ('user_type', 'status', 'phone', 'birth_date')
        }),
    )
