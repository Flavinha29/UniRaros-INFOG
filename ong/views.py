from django.views.generic import ListView, DetailView
from .models import Ong

class OngListView(ListView):
    model = Ong
    template_name = "ong/list.html"
    context_object_name = "ongs"


class OngDetailView(DetailView):
    model = Ong
    template_name = "ong/detail.html"
    context_object_name = "ong"

