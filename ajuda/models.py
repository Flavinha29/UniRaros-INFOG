from django.db import models
from django.contrib.auth import get_user_model
from django.utils import timezone

User = get_user_model()

class PedidoAjuda(models.Model):
    """RF - Gerenciar pedidos de ajuda dos usuários"""
    
    STATUS_CHOICES = [
        ('Pendente', 'Pendente'),
        ('Em andamento', 'Em andamento'),
        ('Resolvido', 'Resolvido'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Usuário")
    titulo = models.CharField(max_length=200, verbose_name="Título do pedido")
    descricao = models.TextField(verbose_name="Descrição detalhada")
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='Pendente')
    criado_em = models.DateTimeField(auto_now_add=True)
    atualizado_em = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.titulo} ({self.status})"

    class Meta:
        verbose_name = "Pedido de Ajuda"
        verbose_name_plural = "Pedidos de Ajuda"
        ordering = ['-criado_em']
