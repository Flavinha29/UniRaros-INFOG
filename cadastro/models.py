from django.db import models
from django.conf import settings
# ✅ REMOVIDO: imports de signals (agora estão apenas no signals.py)

class Paciente(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE, 
        related_name='paciente_profile'
    )
    doenca = models.CharField(max_length=255, blank=True, verbose_name="Doença")
    laudo = models.FileField(upload_to='laudos/', blank=True, verbose_name="Laudo médico")
    
    # ✅ TELEFONE ESPECÍFICO DO PACIENTE (OPCIONAL)
    telefone = models.CharField(max_length=20, blank=True, verbose_name="Telefone do Paciente")

    def __str__(self):
        return f"{self.user.first_name} {self.user.last_name}"

    class Meta:
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

class Profile(models.Model):
    TIPOS_USUARIO = (
        (0, "Administrador"),
        (1, "Paciente"),
        (2, "Usuário"),
    )

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    tipo_usuario = models.PositiveSmallIntegerField(choices=TIPOS_USUARIO, default=2)
    image = models.ImageField(upload_to='profiles/', default='profiles/default.png', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.get_tipo_usuario_display()}"

# ✅ REMOVIDO: Todos os signals (estão duplicados no signals.py)