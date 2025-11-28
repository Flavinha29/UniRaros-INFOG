# relatos/urls.py
from django.urls import path
from . import views

app_name = 'relatos'  # ✅ ADICIONAR APP_NAME

urlpatterns = [
    path('', views.RelatoListView.as_view(), name='relatos-list'),
    path('<int:pk>/', views.RelatoDetailView.as_view(), name='relato-detail'),
    path('novo/', views.RelatoCreateView.as_view(), name='relato-create'),
    path('<int:pk>/comentario/', views.adicionar_comentario, name='adicionar_comentario'),
    path('<int:pk>/curtir/', views.toggle_curtida, name='toggle_curtida'),
    
    # ✅ URLs DE APROVAÇÃO (SÓ ADMINS)
    path('<int:relato_id>/approve/', views.approve_relato, name='approve_relato'),
    path('<int:relato_id>/reject/', views.reject_relato, name='reject_relato'),
]
