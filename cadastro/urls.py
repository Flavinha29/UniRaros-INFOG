# cadastro/urls.py
from django.urls import path
from . import views

app_name = 'cadastro'

urlpatterns = [
    path('novo/', views.cadastrar_usuario, name='cadastro_usuario'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('novo/paciente/', views.cadastrar_paciente, name='cadastro_paciente'),
    path('login/', views.login_view, name='login'),
    path('dashboard/admin/', views.admin_dashboard, name='dashboard_admin'),
    path('dashboard/paciente/', views.paciente_dashboard, name='dashboard_paciente'),
    path('dashboard/usuario/', views.usuario_dashboard, name='dashboard_usuario'),
    
]
