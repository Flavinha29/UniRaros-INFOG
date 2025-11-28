# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView

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
    path('cadastro/', include('cadastro.urls')),
   path('accounts/login/', RedirectView.as_view(url='/cadastro/login/', permanent=False)),
    
    path('accounts/', include('django.contrib.auth.urls')),
]
