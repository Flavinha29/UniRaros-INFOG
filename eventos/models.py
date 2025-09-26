from django.db import models
from django.utils import timezone

class Evento(models.Model):
    """RF - Gerenciar eventos do UniRaros"""
    
    TIPO_EVENTO_CHOICES = [
        ('Palestra', 'Palestra'),
        ('Oficina', 'Oficina'),
        ('Webinar', 'Webinar'),
        ('Outros', 'Outros'),
    ]
    
    nome = models.CharField(max_length=200, verbose_name="Nome do evento")
    descricao = models.TextField(verbose_name="Descrição do evento", blank=True)
    tipo = models.CharField(max_length=50, choices=TIPO_EVENTO_CHOICES, default='Outros')
    data_inicio = models.DateTimeField(verbose_name="Data e hora de início", default=timezone.now)
    data_fim = models.DateTimeField(verbose_name="Data e hora de término", default=timezone.now)
    local = models.CharField(max_length=200, verbose_name="Local do evento", blank=True)
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.nome} ({self.tipo})"

    class Meta:
        verbose_name = "Evento"
        verbose_name_plural = "Eventos"
        ordering = ['data_inicio']
