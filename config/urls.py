# uniraros_project/urls.py
from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps
    path('', include('core.urls')),             # home, sobre
    path('accounts/', include('accounts.urls')),
    path('relatos/', include('relatos.urls')),
    path('ongs/', include('ong.urls')),
    path('conteudos/', include('conteudos.urls')),
    path('eventos/', include('eventos.urls')),
    path('ajuda/', include('ajuda.urls')),
    path('cadastro/', include('cadastro.urls')),  # ADICIONAR ESTA LINHA
]
