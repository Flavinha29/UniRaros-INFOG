from django.shortcuts import render
from eventos.models import Evento
from relatos.models import Relato
from conteudos.models import Conteudo

def home(request):
    # Pega os últimos 3 itens de cada app, usando campos existentes
    eventos = Evento.objects.order_by('-data_inicio')[:3]  # data_inicio existe no model Evento
    relatos = Relato.objects.order_by('-id')[:3]           # id é seguro para ordenar
    conteudos = Conteudo.objects.order_by('-id')[:3]       # id é seguro para ordenar
    
    context = {
        'eventos': eventos,
        'relatos': relatos,
        'conteudos': conteudos,
    }
    return render(request, 'public/home.html', context)

def sobre(request):
    return render(request, 'public/sobre.html')
