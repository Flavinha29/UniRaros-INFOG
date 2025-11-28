from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden
from django.conf import settings

from .models import Relato, Comentario, Curtida
from .forms import RelatoForm, ComentarioForm

# ✅ FUNÇÃO AUXILIAR PARA VERIFICAR PERMISSÕES
def is_patient_approved(user):
    """✅ VERIFICA SE É UM PACIENTE APROVADO"""
    return user.is_authenticated and user.user_type == 'patient' and user.status == 'approved'

def is_admin(user):
    """✅ VERIFICA SE É ADMINISTRADOR"""
    return user.is_authenticated and (user.user_type == 'admin' or user.is_staff)

class RelatoListView(ListView):
    model = Relato
    template_name = 'relatos/list.html'
    context_object_name = 'relatos'

    def get_queryset(self):
        # ✅ MOSTRA APENAS RELATOS APROVADOS (status='approved')
        return Relato.objects.filter(status='approved').order_by('-data_postagem')

class RelatoDetailView(DetailView):
    model = Relato
    template_name = 'relatos/detail.html'

    def get_queryset(self):
        # ✅ SÓ PERMITE ACESSAR RELATOS APROVADOS
        return Relato.objects.filter(status='approved')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        relato = self.get_object()
        context['comentarios'] = relato.comentarios.all().order_by('-data')
        context['form'] = ComentarioForm()
        
        # Flag se o usuário atual curtiu este relato
        if self.request.user.is_authenticated:
            context['usuario_curtiu'] = relato.curtidas.filter(usuario=self.request.user).exists()
        else:
            context['usuario_curtiu'] = False

        return context

class RelatoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Relato
    form_class = RelatoForm
    template_name = 'relatos/form.html'

    def form_valid(self, form):
        form.instance.paciente = self.request.user.paciente_profile
        form.instance.status = 'pending'  # ✅ STATUS PENDENTE
        form.instance.data_postagem = timezone.now()

        # ✅ O SIGNAL VAI ENVIAR O EMAIL AUTOMATICAMENTE
        messages.success(self.request, "Seu relato foi enviado e está aguardando aprovação.")
        return super().form_valid(form)

    def test_func(self):
        # ✅ SÓ PACIENTES APROVADOS PODEM CRIAR RELATOS
        return is_patient_approved(self.request.user)

# ✅ NOVAS VIEWS PARA APROVAÇÃO DE RELATOS (SÓ ADMINS)
@login_required
@user_passes_test(is_admin)
def approve_relato(request, relato_id):
    """✅ APROVA UM RELATO"""
    relato = get_object_or_404(Relato, id=relato_id)
    
    if relato.status == 'pending':
        relato.status = 'approved'
        relato.aprovado_por = request.user
        relato.save()
        
        messages.success(request, f'Relato "{relato.titulo}" aprovado com sucesso!')
    else:
        messages.warning(request, f'Relato "{relato.titulo}" já estava aprovado.')
    
    return redirect('admin:relatos_relato_changelist')

@login_required
@user_passes_test(is_admin)
def reject_relato(request, relato_id):
    """✅ REJEITA UM RELATO"""
    relato = get_object_or_404(Relato, id=relato_id)
    
    if relato.status == 'pending':
        relato.status = 'rejected'
        relato.aprovado_por = request.user
        relato.save()
        
        messages.success(request, f'Relato "{relato.titulo}" rejeitado.')
    else:
        messages.warning(request, f'Não foi possível rejeitar o relato "{relato.titulo}".')
    
    return redirect('admin:relatos_relato_changelist')

# ✅ VIEWS EXISTENTES (MANTIDAS COM PEQUENOS AJUSTES)
@login_required
def adicionar_comentario(request, pk):
    relato = get_object_or_404(Relato, pk=pk, status='approved')  # ✅ CORRIGIDO: status
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Você precisa estar logado para comentar.")

    if request.method == "POST":
        form = ComentarioForm(request.POST)
        if form.is_valid():
            comentario = form.save(commit=False)
            comentario.relato = relato
            comentario.autor = request.user
            comentario.save()
            messages.success(request, "Comentário publicado com sucesso.")
    return redirect('relatos_detail', pk=relato.pk)

@login_required
def toggle_curtida(request, pk):
    relato = get_object_or_404(Relato, pk=pk, status='approved')  # ✅ CORRIGIDO: status
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Você precisa estar logado para curtir.")

    curtida, created = Curtida.objects.get_or_create(relato=relato, usuario=request.user)
    if not created:
        curtida.delete()
        messages.info(request, "Curtida removida.")
    else:
        messages.success(request, "Você curtiu este relato.")

    return redirect('relatos_detail', pk=relato.pk)