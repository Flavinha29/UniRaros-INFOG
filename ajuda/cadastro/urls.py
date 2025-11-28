from django.urls import path
from . import views

app_name = 'cadastro'

urlpatterns = [
    # Cadastros
    path('novo/', views.cadastrar_usuario, name='cadastro_usuario'),
    path('signup/', views.SignupView.as_view(), name='signup'),
    path('novo/paciente/', views.cadastrar_paciente, name='cadastro_paciente'),

    # Login
    path('login/', views.login_view, name='login'),

    # Dashboards
    path('dashboard/admin/', views.dashboard_admin, name='dashboard_admin'),
    path('dashboard/paciente/', views.dashboard_paciente, name='dashboard_paciente'),
    path('dashboard/usuario/', views.dashboard_usuario, name='dashboard_usuario'),
]
