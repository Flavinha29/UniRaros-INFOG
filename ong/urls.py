# ong/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('', views.OngListView.as_view(), name='ong-list'),
    path('<int:pk>/', views.OngDetailView.as_view(), name='ong-detail'),
]
