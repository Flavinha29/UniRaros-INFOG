from django.views.generic import ListView, DetailView, CreateView
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.utils import timezone
from .models import Relato

class RelatoListView(ListView):
    model = Relato
    template_name = 'relatos/list.html'
    context_object_name = 'relatos'

    def get_queryset(self):
        return Relato.objects.filter(aprovado=True, publicado=True).order_by('-data_postagem')

class RelatoDetailView(DetailView):
    model = Relato
    template_name = 'relatos/detail.html'

class RelatoCreateView(LoginRequiredMixin, UserPassesTestMixin, CreateView):
    model = Relato
    fields = ['titulo', 'texto']
    template_name = 'relatos/form.html'

    def form_valid(self, form):
        form.instance.paciente = self.request.user.paciente_profile
        form.instance.aprovado = False
        form.instance.publicado = False
        form.instance.data_postagem = timezone.now()
        return super().form_valid(form)

    def test_func(self):
        return hasattr(self.request.user, 'paciente_profile') and self.request.user.paciente_profile.aprovado
