# eventos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.EventoListView.as_view(), name='evento-list'),
    path('<int:pk>/', views.EventoDetailView.as_view(), name='evento-detail'),
]
