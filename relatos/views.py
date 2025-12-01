# relatos/views.py
from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404, render
from django.core.mail import send_mail
from django.contrib import messages
from django.conf import settings 
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
import threading

from .models import Relato, Comentario, Curtida
from .forms import RelatoForm, ComentarioForm

def is_patient_approved(user):
    """✅ VERIFICA SE É UM PACIENTE APROVADO"""
    if not user.is_authenticated:
        return False
    
    # Verifica se é paciente e está aprovado
    if user.user_type == 'patient' and user.status == 'approved':
        try:
            # ✅ CORREÇÃO: Verifica se existe objeto Paciente relacionado
            from cadastro.models import Paciente
            return Paciente.objects.filter(user=user).exists()
        except:
            return False
    
    return False

def is_admin(user):
    """✅ VERIFICA SE É ADMINISTRADOR"""
    return user.is_authenticated and (user.user_type == 'admin' or user.is_staff or user.is_superuser)

def can_create_relato(user):
    """✅ VERIFICA SE O USUÁRIO PODE CRIAR RELATOS"""
    return is_patient_approved(user)

# ✅ FUNÇÕES PARA ENVIO DE EMAILS
def enviar_email_notificacao_relato(relato, request):
    """Envia email para administradores sobre novo relato"""
    try:
        current_site = get_current_site(request)
        dominio = current_site.domain
        
        context = {
            'relato': relato,
            'paciente': relato.paciente,
            'dominio': dominio,
            'admin_url': f'http://{dominio}/admin/relatos/relato/{relato.id}/change/',
            'data': relato.data_postagem.strftime('%d/%m/%Y %H:%M'),
        }
        
        subject = f'[UniRaros] Novo relato para aprovação: {relato.titulo}'
        text_message = render_to_string('emails/relato_notification.txt', context)
        
        admin_emails = settings.ADMIN_EMAILS
        
        if admin_emails:
            send_mail(
                subject=subject,
                message=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=admin_emails,
                fail_silently=True,
            )
            return True
            
    except Exception as e:
        print(f"Erro ao enviar email de notificação: {e}")
        return False

# ✅ THREAD PARA ENVIO ASSÍNCRONO DE EMAILS
class EmailThread(threading.Thread):
    def __init__(self, relato, request):
        self.relato = relato
        self.request = request
        threading.Thread.__init__(self)
    
    def run(self):
        enviar_email_notificacao_relato(self.relato, self.request)

# ✅ VIEWS PRINCIPAIS
class RelatoListView(ListView):
    model = Relato
    template_name = 'relatos/list.html'
    context_object_name = 'relatos'
    paginate_by = 10

    def get_queryset(self):
        # ✅ MOSTRA APENAS RELATOS APROVADOS PARA TODOS
        # Admins também veem apenas aprovados no site público
        return Relato.objects.filter(status='approved').order_by('-data_postagem')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['can_create_relato'] = can_create_relato(self.request.user)
        return context

class RelatoDetailView(DetailView):
    model = Relato
    template_name = 'relatos/detail.html'

    def get_queryset(self):
        # ✅ SÓ MOSTRA RELATOS APROVADOS
        return Relato.objects.filter(status='approved')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        relato = self.get_object()
        context['comentarios'] = relato.comentarios.all().order_by('-data')
        context['form'] = ComentarioForm()
        
        # Verifica se usuário curtiu
        if self.request.user.is_authenticated:
            context['usuario_curtiu'] = relato.curtidas.filter(usuario=self.request.user).exists()
        else:
            context['usuario_curtiu'] = False
        
        context['can_comment'] = self.request.user.is_authenticated
        
        return context

# relatos/views.py - Atualize a RelatoCreateView

class RelatoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Relato
    form_class = RelatoForm
    template_name = 'relatos/form.html'
    success_url = '/relatos/'

    def test_func(self):
        """✅ SÓ PACIENTES APROVADOS PODEM CRIAR RELATOS"""
        return can_create_relato(self.request.user)

    def form_valid(self, form):
        """✅ CONFIGURA OS DADOS DO RELATO ANTES DE SALVAR"""
        user = self.request.user
        
        # Verifica se o usuário é paciente
        if user.user_type != 'patient':
            messages.error(self.request, "Apenas pacientes podem criar relatos.")
            return self.form_invalid(form)
        
        try:
            # ✅ BUSCA O PACIENTE CORRETAMENTE
            # Primeiro importa o modelo Paciente
            from cadastro.models import Paciente
            
            # Tenta obter o objeto Paciente relacionado ao usuário
            paciente = Paciente.objects.get(user=user)
            
            # Associa o paciente ao relato
            form.instance.paciente = paciente
            
        except Paciente.DoesNotExist:
            messages.error(self.request, 
                "Perfil de paciente não encontrado. "
                "Por favor, complete seu cadastro como paciente primeiro."
            )
            return self.form_invalid(form)
        except Exception as e:
            messages.error(self.request, f"Erro ao associar paciente: {str(e)}")
            return self.form_invalid(form)
        
        # Define os outros campos
        form.instance.status = 'pending'
        form.instance.data_postagem = timezone.now()

        # Salva o relato
        response = super().form_valid(form)
        
        # ✅ ENVIA EMAIL DE NOTIFICAÇÃO PARA ADMINISTRADORES
        try:
            EmailThread(self.object, self.request).start()
        except:
            # Se falhar, tenta enviar sincrono
            try:
                enviar_email_notificacao_relato(self.object, self.request)
            except:
                pass  # Não quebra o fluxo
        
        messages.success(self.request, "Seu relato foi enviado e está aguardando aprovação.")
        return response

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_patient'] = self.request.user.user_type == 'patient'
        return context

# ✅ VIEWS PARA COMENTÁRIOS E CURTIDAS
@login_required
def adicionar_comentario(request, pk):
    """✅ ADICIONA UM COMENTÁRIO A UM RELATO"""
    relato = get_object_or_404(Relato, pk=pk, status='approved')
    
    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.relato = relato
            comentario.autor = request.user
            comentario.data = timezone.now()
            comentario.save()
            messages.success(request, "Comentário publicado com sucesso.")
        else:
            messages.error(request, "Erro ao publicar comentário.")
    
    return redirect('relatos:relato-detail', pk=relato.pk)

@login_required
def toggle_curtida(request, pk):
    """✅ ADICIONA/REMOVE CURTIDA DE UM RELATO"""
    relato = get_object_or_404(Relato, pk=pk, status='approved')
    
    curtida, created = Curtida.objects.get_or_create(relato=relato, usuario=request.user)
    if not created:
        curtida.delete()
        messages.info(request, "Curtida removida.")
    else:
        messages.success(request, "Você curtiu este relato.")
    
    return redirect('relatos:relato-detail', pk=relato.pk)

# ✅ VIEW PARA PACIENTE VER SEUS PRÓPRIOS RELATOS
# relatos/views.py - Atualize a função meus_relatos

@login_required
def meus_relatos(request):
    """✅ MOSTRA RELATOS DO USUÁRIO LOGADO (PACIENTE)"""
    user = request.user
    
    if user.user_type == 'patient':
        try:
            # ✅ CORREÇÃO: Busca paciente primeiro
            from cadastro.models import Paciente
            paciente = Paciente.objects.get(user=user)
            relatos = Relato.objects.filter(paciente=paciente).order_by('-data_postagem')
        except Paciente.DoesNotExist:
            relatos = []
            messages.info(request, "Você ainda não tem um perfil de paciente completo.")
        except Exception:
            relatos = []
    else:
        relatos = []
        messages.warning(request, "Apenas pacientes podem visualizar seus relatos.")
    
    return render(request, 'relatos/meus_relatos.html', {
        'relatos': relatos,
        'total': len(relatos),
        'aprovados': relatos.filter(status='approved').count() if relatos else 0,
        'pendentes': relatos.filter(status='pending').count() if relatos else 0,
        'rejeitados': relatos.filter(status='rejected').count() if relatos else 0,
    })

# ✅ VIEWS PARA APROVAÇÃO/REJEIÇÃO (USADAS VIA ADMIN)
@login_required
@user_passes_test(is_admin)
def approve_relato(request, relato_id):
    """✅ APROVA UM RELATO (via admin)"""
    relato = get_object_or_404(Relato, id=relato_id)
    
    if relato.status == 'pending':
        relato.status = 'approved'
        relato.aprovado_por = request.user
        relato.data_aprovacao = timezone.now()
        relato.save()
        
        messages.success(request, f'Relato "{relato.titulo}" aprovado com sucesso!')
    else:
        messages.warning(request, f'Relato "{relato.titulo}" já estava aprovado.')
    
    # Redireciona de volta para o admin
    return redirect('admin:relatos_relato_changelist')

@login_required
@user_passes_test(is_admin)
def reject_relato(request, relato_id):
    """✅ REJEITA UM RELATO (via admin)"""
    relato = get_object_or_404(Relato, id=relato_id)
    
    if relato.status == 'pending':
        relato.status = 'rejected'
        relato.aprovado_por = request.user
        relato.save()
        
        messages.success(request, f'Relato "{relato.titulo}" rejeitado.')
    else:
        messages.warning(request, f'Não foi possível rejeitar o relato "{relato.titulo}".')
    
    return redirect('admin:relatos_relato_changelist')