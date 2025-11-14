from django.urls import path
from .views import EventoListView, EventoDetailView

urlpatterns = [
    path('', EventoListView.as_view(), name='lista_eventos'),
    path('<int:pk>/', EventoDetailView.as_view(), name='detalhe_evento'),
]
