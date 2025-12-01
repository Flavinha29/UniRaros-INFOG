from django.shortcuts import render
from eventos.models import Evento
from relatos.models import Relato
from conteudos.models import Conteudo
from ong.models import Ong  # <--- aqui não tem 's'

def home(request):
    eventos = Evento.objects.order_by('-data_inicio')[:3]
    relatos = Relato.objects.order_by('-id')[:3]
    conteudos = Conteudo.objects.order_by('-id')[:3]
    ongs = Ong.objects.order_by('-id')[:3]  # adiciona ONGs na home
    
    context = {
        'eventos': eventos,
        'relatos': relatos,
        'conteudos': conteudos,
        'ongs': ongs,
    }
    return render(request, 'public/home.html', context)

def sobre(request):
    return render(request, 'public/sobre.html')
