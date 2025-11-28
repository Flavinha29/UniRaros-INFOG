# ajuda/signals.py
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.conf import settings
from .models import PedidoAjuda

@receiver(post_save, sender=PedidoAjuda)
def send_help_request_notification(sender, instance, created, **kwargs):
    """✅ ENVIA EMAIL QUANDO UM PEDIDO DE AJUDA É CRIADO"""
    if created:
        admin_emails = settings.ADMIN_EMAILS
        
        context = {
            'user_name': instance.usuario.get_full_name_or_username(),
            'user_email': instance.usuario.email,
            'user_type': instance.usuario.get_user_type_display(),
            'titulo': instance.titulo,
            'descricao': instance.descricao,  # ✅ CORRIGIDO: descricao em vez de mensagem
            'request_date': instance.criado_em.strftime('%d/%m/%Y às %H:%M'),
            'admin_url': f"{settings.SITE_URL}/admin/ajuda/pedidoajuda/{instance.id}/change/",
            'user_admin_url': f"{settings.SITE_URL}/admin/accounts/customuser/{instance.usuario.id}/change/",
        }
        
        # Renderizar conteúdo HTML e texto
        html_content = render_to_string('emails/help_request_notification.html', context)
        text_content = render_to_string('emails/help_request_notification.txt', context)
        
        # Enviar email
        subject = f"Novo Pedido de Ajuda - {instance.titulo}"
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=admin_emails,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()