from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from .models import Paciente

User = get_user_model()

@receiver(post_save, sender=User)
def criar_paciente(sender, instance, created, **kwargs):
    if created and instance.tipo_usuario == 'paciente':
        Paciente.objects.create(
            user=instance,
            nome_completo=instance.get_full_name() or instance.username,
            email=instance.email
        )
