# config/urls.py
from django.contrib import admin
from django.urls import path, include
from django.views.generic import RedirectView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),

    # Apps
    path('', include('core.urls')),             # home, sobre
    path('relatos/', include('relatos.urls')),
    path('ongs/', include('ong.urls')),
    path('conteudos/', include('conteudos.urls')),
    path('eventos/', include('eventos.urls')),
    path('ajuda/', include('ajuda.urls')),
    
    # ✅ CORRIGIDO: URLs de accounts organizadas
    path('accounts/', include('django.contrib.auth.urls')),  # Login/logout padrão do Django
    path('accounts/', include('accounts.urls')),             # Suas views customizadas
    
    # ✅ CORRIGIDO: Cadastro com redirecionamento
    path('cadastro/', include('cadastro.urls')),
    path('accounts/login/', RedirectView.as_view(url='/cadastro/login/', permanent=False)),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    