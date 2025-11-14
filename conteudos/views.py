from django.views.generic import ListView, DetailView
from .models import Conteudo

class ConteudoListView(ListView):
    model = Conteudo
    template_name = 'conteudos/list.html'
    context_object_name = 'conteudos'

class ConteudoDetailView(DetailView):
    model = Conteudo
    template_name = 'conteudos/detail.html'
    context_object_name = "conteudo"