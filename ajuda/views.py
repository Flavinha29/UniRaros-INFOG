from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib import messages
from .models import PedidoAjuda
from .forms import PedidoAjudaForm  # ✅ USAR O FORM CUSTOMIZADO

@method_decorator(login_required, name='dispatch')
class PedidoAjudaCreateView(CreateView):
    model = PedidoAjuda
    form_class = PedidoAjudaForm  # ✅ USAR O FORM CUSTOMIZADO
    template_name = 'ajuda/form.html'
    success_url = reverse_lazy('ajuda:obrigatorio')  # ✅ CORRIGIDO: usar app_name

    def form_valid(self, form):
        form.instance.usuario = self.request.user
        
        # ✅ MENSAGEM DE SUCESSO
        messages.success(
            self.request, 
            'Seu pedido de ajuda foi enviado com sucesso! '
            'Nossa equipe entrará em contato em breve.'
        )
        
        # ✅ O SIGNAL VAI ENVIAR O EMAIL AUTOMATICAMENTE
        return super().form_valid(form)

@login_required
def pedido_ajuda_obrigado(request):
    """✅ PÁGINA DE AGRADECIMENTO/OBRIGADO"""
    return render(request, 'ajuda/obrigado.html')

@login_required
def ajuda_redirect(request):
    """✅ REDIRECIONAMENTO INTELIGENTE"""
    if request.user.is_authenticated:
        return redirect('ajuda:pedido_ajuda')  # ✅ CORRIGIDO: usar app_name
    return render(request, 'ajuda/precisa_login.html')

@login_required
def meus_pedidos_ajuda(request):
    """✅ LISTA OS PEDIDOS DE AJUDA DO USUÁRIO (NOVO)"""
    pedidos = PedidoAjuda.objects.filter(usuario=request.user).order_by('-criado_em')
    return render(request, 'ajuda/meus_pedidos.html', {'pedidos': pedidos})