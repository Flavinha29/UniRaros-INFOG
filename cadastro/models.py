from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.conf import settings

class Paciente(models.Model):
    nome_completo = models.CharField(max_length=150)
    cpf = models.CharField(max_length=14, unique=True)  # formato XXX.XXX.XXX-XX
    telefone = models.CharField(max_length=20)
    email = models.EmailField(unique=True)
    laudo = models.FileField(upload_to='laudos/')
    senha = models.CharField(max_length=128)  # podemos usar User ou hash depois

    def __str__(self):
        return self.nome_completo

# cadastro/models.py

class Profile(models.Model):
    TIPOS_USUARIO = (
        (0, "Administrador"),
        (1, "Paciente"),
        (2, "Usuário"),
    )
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_usuario = models.PositiveSmallIntegerField(choices=TIPOS_USUARIO, default=2)

    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_usuario_display()}"