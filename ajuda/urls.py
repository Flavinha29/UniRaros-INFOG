# ajuda/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.PedidoAjudaCreateView.as_view(), name='pedido-ajuda'),
    path('obrigado/', views.pedido_ajuda_obrigado, name='pedido-ajuda-obrigado'),
]
