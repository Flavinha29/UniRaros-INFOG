from django.contrib import admin
from .models import Evento

@admin.register(Evento)
class EventoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'tipo', 'data_inicio', 'data_fim', 'local')
    list_filter = ('tipo', 'data_inicio')
    search_fields = ('nome', 'descricao', 'local')
    ordering = ('data_inicio',)
