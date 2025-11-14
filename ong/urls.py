from django.urls import path
from .views import OngListView, OngDetailView

urlpatterns = [
    path('', OngListView.as_view(), name='ong_list'),
    path('<int:pk>/', OngDetailView.as_view(), name='ong_detail'),
]
