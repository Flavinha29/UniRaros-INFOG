from django.shortcuts import render
from django.views.generic import CreateView
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from .forms import UserCreationFormCustom
from django.contrib.auth import logout
from django.shortcuts import redirect

class SignupView(CreateView):
    form_class = UserCreationFormCustom
    template_name = 'accounts/register.html'
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

def custom_logout(request):
    logout(request)
    return redirect('home')
