from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
from django.conf import settings
from .models import Relato

@receiver(post_save, sender=Relato)
def send_relato_notification(sender, instance, created, **kwargs):
    if created:
        # Lista de administradores
        admin_emails = [
            'admin1@exemplo.com',
            'admin2@exemplo.com', 
            'admin3@exemplo.com'
        ]
        
        # Contexto para o template de email
        context = {
            'patient_name': instance.autor.get_full_name_or_username(),
            'report_title': instance.titulo,
            'report_content': instance.conteudo,
            'report_date': instance.criado_em.strftime('%d/%m/%Y às %H:%M'),
            'approve_url': f"{settings.SITE_URL}{reverse('relatos:approve_relato', args=[instance.id])}",
            'reject_url': f"{settings.SITE_URL}{reverse('relatos:reject_relato', args=[instance.id])}",
            'admin_url': f"{settings.SITE_URL}/admin/relatos/relato/{instance.id}/change/",
        }
        
        # Renderizar conteúdo HTML e texto
        html_content = render_to_string('emails/relato_notification.html', context)
        text_content = render_to_string('emails/relato_notification.txt', context)
        
        # Enviar email
        subject = f"Novo Relato Pendente - {instance.titulo}"
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=admin_emails,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()