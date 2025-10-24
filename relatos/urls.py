# relatos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.RelatoListView.as_view(), name='relatos-list'),
    path('<int:pk>/', views.RelatoDetailView.as_view(), name='relato-detail'),
    path('novo/', views.RelatoCreateView.as_view(), name='relato-create'),
    path('<int:pk>/comentario/', views.adicionar_comentario, name='adicionar_comentario'),
    path('<int:pk>/curtir/', views.toggle_curtida, name='toggle_curtida'),
]
