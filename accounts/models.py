from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError

class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = [
        ('patient', 'Paciente'),
        ('admin', 'Administrador'),
        ('staff', 'Equipe'),
    ]
    STATUS_CHOICES = [
        ('pending', 'Pendente'),
        ('approved', 'Aprovado'),
        ('rejected', 'Rejeitado'),
    ]
    
    user_type = models.CharField(
        max_length=10, 
        choices=USER_TYPE_CHOICES, 
        default='patient'
    )
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='pending'
    )
    phone = models.CharField(max_length=20, blank=True, verbose_name="Telefone")
    birth_date = models.DateField(null=True, blank=True, verbose_name="Data de Nascimento")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if self.user_type == 'admin' and self.status == 'pending':
            raise ValidationError('Administradores não podem ter status pendente.')

    def is_approved(self):
        return self.status == 'approved'

    def get_full_name_or_username(self):
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username

    class Meta:
        verbose_name = 'Usuário'
        verbose_name_plural = 'Usuários'
        db_table = 'custom_user'

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"
class Paciente(models.Model):
    user = models.OneToOneField(
        CustomUser, 
        on_delete=models.CASCADE, 
        related_name='paciente_profile'
    )
    nome_completo = models.CharField(max_length=255)
    email = models.EmailField()
    
    def __str__(self):
        return self.nome_completo

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'