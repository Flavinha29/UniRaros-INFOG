from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from django.shortcuts import redirect, get_object_or_404
from django.core.mail import send_mail
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseForbidden

from .models import Relato, Comentario, Curtida
from .forms import RelatoForm, ComentarioForm


class RelatoListView(ListView):
    model = Relato
    template_name = 'relatos/list.html'
    context_object_name = 'relatos'

    def get_queryset(self):
        return Relato.objects.filter(aprovado=True, publicado=True).order_by('-data_postagem')


class RelatoDetailView(DetailView):
    model = Relato
    template_name = 'relatos/detail.html'

    def get_queryset(self):
        return Relato.objects.filter(aprovado=True, publicado=True)

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
        form.instance.aprovado = False
        form.instance.publicado = False
        form.instance.data_postagem = timezone.now()

        # e-mail para admin
        send_mail(
            subject="Novo relato aguardando aprovação",
            message=f"O paciente {self.request.user.username} enviou um relato: {form.instance.titulo}",
            from_email="noreply@uniraros.com",
            recipient_list=["admin@uniraros.com"],  # trocar para e-mail real
            fail_silently=True,
        )

        messages.success(self.request, "Seu relato foi enviado e está aguardando aprovação.")
        return super().form_valid(form)

    def test_func(self):
        return hasattr(self.request.user, 'paciente_profile') and self.request.user.paciente_profile.aprovado


# Comentários
def adicionar_comentario(request, pk):
    relato = get_object_or_404(Relato, pk=pk, aprovado=True, publicado=True)
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


# Curtidas
def toggle_curtida(request, pk):
    relato = get_object_or_404(Relato, pk=pk, aprovado=True, publicado=True)
    if not request.user.is_authenticated:
        return HttpResponseForbidden("Você precisa estar logado para curtir.")

    curtida, created = Curtida.objects.get_or_create(relato=relato, usuario=request.user)
    if not created:
        curtida.delete()
        messages.info(request, "Curtida removida.")
    else:
        messages.success(request, "Você curtiu este relato.")

    return redirect('relatos_detail', pk=relato.pk)
