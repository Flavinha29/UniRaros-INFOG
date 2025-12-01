from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from .models import Profile

# ✅ APENAS UM SIGNAL - inteligente e seguro
@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def criar_ou_atualizar_profile(sender, instance, created, **kwargs):
    """
    Cria ou atualiza Profile automaticamente.
    USA get_or_create para EVITAR DUPLICAÇÃO.
    """
    if created:
        # ✅ MÉTODO SEGURO - não duplica
        Profile.objects.get_or_create(
            user=instance,
            defaults={'tipo_usuario': 2}  # Default: usuário comum
        )
    else:
        # Atualiza se já existe
        if hasattr(instance, 'profile'):
            instance.profile.save()

# ✅ REMOVIDO: Segundo signal duplicado