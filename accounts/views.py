from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UserCreationFormCustom

class SignupView(CreateView):
    form_class = UserCreationFormCustom
    template_name = 'accounts/signup.html'
    success_url = reverse_lazy('login')

@login_required
def dashboard(request):
    user = request.user
    if user.is_staff:
        template = 'dashboards/dashboard_admin.html'
    elif hasattr(user, 'paciente_profile'):
        template = 'dashboards/dashboard_paciente.html'
    else:
        template = 'dashboards/dashboard_user.html'
    return render(request, template)
