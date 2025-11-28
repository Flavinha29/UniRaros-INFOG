from django.urls import path
from . import views

app_name = 'ajuda'  # ✅ ADICIONAR APP_NAME

urlpatterns = [
    path('', views.ajuda_redirect, name='ajuda'),  # ✅ MUDE O NOME PARA 'ajuda'
    path('novo/', views.PedidoAjudaCreateView.as_view(), name='pedido_ajuda'),
    path('obrigado/', views.pedido_ajuda_obrigado, name='obrigatorio'),
    
    # URLs COMPATÍVEIS
    path('pedido-ajuda/', views.PedidoAjudaCreateView.as_view(), name='pedido-ajuda'),
    path('pedido-ajuda-obrigado/', views.pedido_ajuda_obrigado, name='pedido-ajuda-obrigado'),
]
