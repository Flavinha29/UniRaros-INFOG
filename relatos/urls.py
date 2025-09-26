# relatos/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.RelatoListView.as_view(), name='relato-list'),
    path('<int:pk>/', views.RelatoDetailView.as_view(), name='relato-detail'),
    path('novo/', views.RelatoCreateView.as_view(), name='relato-create'),
]
