# accounts/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
