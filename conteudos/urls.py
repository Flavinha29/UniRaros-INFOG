# conteudos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.ConteudoListView.as_view(), name='conteudo-list'),
    path('<int:pk>/', views.ConteudoDetailView.as_view(), name='conteudo-detail'),
]
