from django.views.generic import ListView, DetailView
from .models import Evento

class EventoListView(ListView):
    model = Evento
    template_name = 'eventos/list.html'
    context_object_name = 'eventos'

class EventoDetailView(DetailView):
    model = Evento
    template_name = 'eventos/detail.html'
