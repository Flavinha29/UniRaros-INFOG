from django.contrib import admin
from .models import Conteudo

class ConteudoAdmin(admin.ModelAdmin):
    list_display = ('nome', 'categoria', 'criado_em')
    list_filter = ('categoria',)
    search_fields = ('nome', 'resumo')

admin.site.register(Conteudo, ConteudoAdmin)
