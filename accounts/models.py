from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    TIPO_CHOICES = (
        ('usuario', 'Usuário'),
        ('paciente', 'Paciente'),
    )
    tipo_usuario = models.CharField(max_length=20, choices=TIPO_CHOICES, default='usuario')

    def is_paciente(self):
        return self.tipo_usuario == 'paciente'


class Paciente(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='paciente_profile')
    nome_completo = models.CharField(max_length=200)
    email = models.EmailField(unique=True)
    doenca = models.CharField(max_length=200, blank=True, null=True)
    aprovado = models.BooleanField(default=False)  # aprovado pelo admin

    def __str__(self):
        return self.nome_completo
