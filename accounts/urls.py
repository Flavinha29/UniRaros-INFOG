# accounts/urls.py
from django.urls import path
from . import views

app_name = 'accounts'  # ✅ ADICIONAR APP_NAME PARA ORGANIZAÇÃO

urlpatterns = [
    path('logout/', views.custom_logout, name='logout'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('dashboard/', views.dashboard, name='dashboard'),
    
    # ✅ URLs DE APROVAÇÃO (SÓ ADMINS)
    path('user/<int:user_id>/approve/', views.approve_user, name='approve_user'),
    path('user/<int:user_id>/reject/', views.reject_user, name='reject_user'),
]
