from django.db import models
from django.conf import settings
from django.utils import timezone
from django.urls import reverse
from django.core.exceptions import ValidationError

class Relato(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]
    
    # ✅ CORRIGIDO: Agora referencia cadastro.Paciente
    paciente = models.ForeignKey('cadastro.Paciente', on_delete=models.CASCADE, related_name='relatos')
    titulo = models.CharField(max_length=255)
    texto = models.TextField()
    data_postagem = models.DateTimeField(default=timezone.now)
    
    # ✅ SISTEMA DE STATUS PARA APROVAÇÃO
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending',
        verbose_name="Status"
    )
    
    # ✅ CAMPOS DE CONTROLE DE APROVAÇÃO
    aprovado_por = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='relatos_aprovados',
        verbose_name="Aprovado por"
    )
    data_aprovacao = models.DateTimeField(null=True, blank=True, verbose_name="Data de aprovação")
    
    # ✅ MANTENDO PARA COMPATIBILIDADE (OPCIONAL)
    aprovado = models.BooleanField(default=False)
    publicado = models.BooleanField(default=False)

    class Meta:
        verbose_name = 'Relato'
        verbose_name_plural = 'Relatos'
        ordering = ['-data_postagem']

    def __str__(self):
        return self.titulo

    def get_absolute_url(self):
        return reverse("relatos_detail", kwargs={"pk": self.pk})

    def clean(self):
        """✅ VALIDAÇÃO: Só pacientes aprovados podem criar relatos"""
        if self.paciente and self.paciente.user.status != 'approved':
            raise ValidationError('Apenas pacientes aprovados podem criar relatos.')

    def save(self, *args, **kwargs):
        """✅ ATUALIZA CAMPOS LEGADOS QUANDO STATUS MUDA"""
        if self.status == 'approved':
            self.aprovado = True
            self.publicado = True
            if not self.data_aprovacao:
                self.data_aprovacao = timezone.now()
        elif self.status == 'rejected':
            self.aprovado = False
            self.publicado = False
        elif self.status == 'pending':
            self.aprovado = False
            self.publicado = False
            
        super().save(*args, **kwargs)

    def pode_ser_visualizado(self):
        """✅ VERIFICA SE O RELATO PODE SER VISTO PUBLICAMENTE"""
        return self.status == 'approved'

class Comentario(models.Model):
    relato = models.ForeignKey(Relato, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    texto = models.TextField()
    data = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"Comentário de {self.autor} em {self.relato}"

    class Meta:
        verbose_name = 'Comentário'
        verbose_name_plural = 'Comentários'
        ordering = ['-data']

class Curtida(models.Model):
    relato = models.ForeignKey(Relato, on_delete=models.CASCADE, related_name='curtidas')
    usuario = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('relato', 'usuario')
        verbose_name = 'Curtida'
        verbose_name_plural = 'Curtidas'

    def __str__(self):
        return f"{self.usuario} curtiu {self.relato}"