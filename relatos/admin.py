from django.contrib import admin
from .models import Relato, Comentario

class RelatoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'paciente', 'aprovado', 'data_postagem')
    list_filter = ('aprovado',)
    actions = ['aprovar_relatos']

    def aprovar_relatos(self, request, queryset):
        queryset.update(aprovado=True, publicado=True)

admin.site.register(Relato, RelatoAdmin)
admin.site.register(Comentario)
