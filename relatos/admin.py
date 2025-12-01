# relatos/admin.py
from django.contrib import admin
from django.utils.html import format_html
from .models import Relato, Comentario, Curtida

class RelatoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'paciente', 'status', 'status_badge', 'data_postagem', 'aprovado_por')
    list_filter = ('status', 'data_postagem', 'aprovado_por')
    search_fields = ('titulo', 'texto', 'paciente__user__first_name', 'paciente__user__email')
    readonly_fields = ('data_postagem', 'data_aprovacao')
    actions = ['aprovar_relatos', 'rejeitar_relatos']
    list_editable = ('status',)  # ✅ CORRETO: status está em list_display
    
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'texto', 'paciente', 'data_postagem')
        }),
        ('Status e Aprovação', {
            'fields': ('status', 'aprovado_por', 'data_aprovacao')
        }),
        ('Campos de Compatibilidade', {
            'fields': ('aprovado', 'publicado'),
            'classes': ('collapse',),
        }),
    )
    
    def status_badge(self, obj):
        """Exibe status com cores"""
        colors = {
            'pending': 'orange',
            'approved': 'green',
            'rejected': 'red',
        }
        return format_html(
            '<span style="background-color: {}; color: white; padding: 2px 8px; border-radius: 10px; font-size: 12px;">{}</span>',
            colors.get(obj.status, 'gray'),
            obj.get_status_display()
        )
    status_badge.short_description = 'Status Badge'
    status_badge.admin_order_field = 'status'
    
    def aprovar_relatos(self, request, queryset):
        from django.utils import timezone
        from django.contrib import messages
        
        for relato in queryset.filter(status='pending'):
            relato.status = 'approved'
            relato.aprovado_por = request.user
            relato.data_aprovacao = timezone.now()
            relato.save()
        
        self.message_user(request, f"{queryset.filter(status='pending').count()} relato(s) aprovado(s) com sucesso!")
    aprovar_relatos.short_description = "✅ Aprovar relatos selecionados"
    
    def rejeitar_relatos(self, request, queryset):
        for relato in queryset.filter(status='pending'):
            relato.status = 'rejected'
            relato.aprovado_por = request.user
            relato.save()
        
        self.message_user(request, f"{queryset.filter(status='pending').count()} relato(s) rejeitado(s).")
    rejeitar_relatos.short_description = "❌ Rejeitar relatos selecionados"

class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('autor', 'relato', 'data', 'texto_resumido')
    list_filter = ('data', 'relato')
    search_fields = ('texto', 'autor__username', 'relato__titulo')
    
    def texto_resumido(self, obj):
        return obj.texto[:50] + '...' if len(obj.texto) > 50 else obj.texto
    texto_resumido.short_description = 'Comentário'

class CurtidaAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'relato', 'created_at')
    list_filter = ('created_at',)

admin.site.register(Relato, RelatoAdmin)
admin.site.register(Comentario, ComentarioAdmin)
admin.site.register(Curtida, CurtidaAdmin)