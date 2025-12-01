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
    # ✅ TELEFONE AGORA OBRIGATÓRIO
    phone = models.CharField(
        max_length=20, 
        verbose_name="Telefone",
        blank=False
    )
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