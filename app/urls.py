from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),

    # inclui as rotas do APP eventos
    path('eventos/', include('eventos.urls')),
    path('conteudos/', include('conteudos.urls')),
]
