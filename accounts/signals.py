from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.urls import reverse
import time

User = get_user_model()

@receiver(post_save, sender=User)
def send_registration_notification(sender, instance, created, **kwargs):
    """✅ ENVIA EMAIL QUANDO UM PACIENTE SE CADASTRA - CORRIGIDO"""
    if created and instance.user_type == 'patient':
        # ✅ AGUARDA 2 SEGUNDOS PARA O PACIENTE SER CRIADO
        time.sleep(2)
        
        admin_emails = settings.ADMIN_EMAILS
        
        # ✅ TENTA OBTER DADOS DO PACIENTE SE EXISTIR
        paciente_data = {}
        try:
            if hasattr(instance, 'paciente_profile'):
                paciente = instance.paciente_profile
                paciente_data = {
                    'Doença': paciente.doenca or 'Não informada',
                    'Laudo': 'Sim' if paciente.laudo else 'Não',
                }
        except:
            paciente_data = {
                'Doença': 'Ainda não disponível',
                'Laudo': 'Ainda não disponível',
            }
        
        # Coletar todos os dados do usuário
        user_data = {
            'Nome de usuário': instance.username,
            'E-mail': instance.email,
            'Nome completo': f"{instance.first_name} {instance.last_name}".strip() or 'Não informado',
            'Telefone': instance.phone or 'Não informado',
            'Data de nascimento': instance.birth_date.strftime('%d/%m/%Y') if instance.birth_date else 'Não informada',
            'Tipo de usuário': instance.get_user_type_display(),
            'Status': instance.get_status_display(),
            'Data de registro': instance.date_joined.strftime('%d/%m/%Y às %H:%M'),
            **paciente_data  # ✅ INCLUI DADOS DO PACIENTE
        }
        
        context = {
            'user': instance,
            'user_data': user_data,
            'approve_url': f"{settings.SITE_URL}{reverse('accounts:approve_user', args=[instance.id])}",
            'reject_url': f"{settings.SITE_URL}{reverse('accounts:reject_user', args=[instance.id])}",
            'admin_url': f"{settings.SITE_URL}/admin/accounts/customuser/{instance.id}/change/",
        }
        
        # Renderizar conteúdo HTML e texto
        html_content = render_to_string('emails/registration_notification.html', context)
        text_content = render_to_string('emails/registration_notification.txt', context)
        
        # Enviar email
        subject = f"Novo Cadastro de Paciente - {instance.username}"
        
        email = EmailMultiAlternatives(
            subject=subject,
            body=text_content,
            from_email=settings.DEFAULT_FROM_EMAIL,
            to=admin_emails,
        )
        email.attach_alternative(html_content, "text/html")
        email.send()