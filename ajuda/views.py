from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render
from .models import PedidoAjuda

class PedidoAjudaCreateView(CreateView):
    model = PedidoAjuda
    fields = ['nome', 'email', 'mensagem']
    template_name = 'ajuda/form.html'
    success_url = reverse_lazy('pedido-ajuda-obrigado')

def pedido_ajuda_obrigado(request):
    return render(request, 'ajuda/obrigado.html')
