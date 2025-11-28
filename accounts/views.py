# accounts/views.py
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth import logout
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth import get_user_model  # ✅ ADICIONAR ESTA LINHA

from .forms import UserCreationFormCustom

User = get_user_model()  # ✅ USA get_user_model() EM VEZ DE IMPORTAR DIRETO

class SignupView(CreateView):
    form_class = UserCreationFormCustom
    template_name = 'accounts/register.html'
    success_url = reverse_lazy('login')

@login_required
def dashboard(request):
    user = request.user
    if user.is_staff:
        template = 'dashboards/dashboard_admin.html'
    elif user.user_type == 'patient':  # ✅ CORRIGIDO: user_type em vez de paciente_profile
        template = 'dashboards/dashboard_paciente.html'
    else:
        template = 'dashboards/dashboard_user.html'
    return render(request, template)

def custom_logout(request):
    logout(request)
    return redirect('home')

# ✅ NOVAS VIEWS PARA APROVAÇÃO DE USUÁRIOS

def is_admin(user):
    """✅ VERIFICA SE O USUÁRIO É ADMINISTRADOR"""
    return user.is_authenticated and (user.user_type == 'admin' or user.is_staff)

@login_required
@user_passes_test(is_admin)
def approve_user(request, user_id):
    """✅ APROVA UM USUÁRIO PACIENTE"""
    user = get_object_or_404(User, id=user_id)
    
    if user.user_type == 'patient' and user.status == 'pending':
        user.status = 'approved'
        user.save()
        
        # ✅ ENVIA EMAIL DE APROVAÇÃO PARA O PACIENTE
        send_mail(
            subject='Cadastro Aprovado - Sistema Doenças Raras',
            message=f'''Olá {user.first_name or user.username},

Seu cadastro foi aprovado com sucesso! Agora você pode acessar sua conta e utilizar todos os recursos do sistema.

Acesse: {settings.SITE_URL}/accounts/login/

Atenciosamente,
Equipe Doenças Raras
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        messages.success(request, f'Usuário {user.username} aprovado com sucesso!')
    else:
        messages.warning(request, f'Não foi possível aprovar o usuário {user.username}.')
    
    return redirect('admin:accounts_customuser_changelist')

@login_required
@user_passes_test(is_admin)
def reject_user(request, user_id):
    """✅ REJEITA UM USUÁRIO PACIENTE"""
    user = get_object_or_404(User, id=user_id)
    
    if user.user_type == 'patient' and user.status == 'pending':
        user.status = 'rejected'
        user.save()
        
        # ✅ ENVIA EMAIL DE REJEIÇÃO PARA O PACIENTE
        send_mail(
            subject='Cadastro Não Aprovado - Sistema Doenças Raras',
            message=f'''Olá {user.first_name or user.username},

Após análise, infelizmente não podemos aprovar seu cadastro no momento.

Para mais informações, entre em contato conosco.

Atenciosamente,
Equipe Doenças Raras
''',
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[user.email],
            fail_silently=False,
        )
        
        messages.success(request, f'Usuário {user.username} rejeitado.')
    else:
        messages.warning(request, f'Não foi possível rejeitar o usuário {user.username}.')
    
    return redirect('admin:accounts_customuser_changelist')