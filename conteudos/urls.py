from django.urls import path
from .views import ConteudoListView, ConteudoDetailView

urlpatterns = [
    path('', ConteudoListView.as_view(), name='lista_conteudos'),
    path('<int:pk>/', ConteudoDetailView.as_view(), name='detalhe_conteudo'),
]