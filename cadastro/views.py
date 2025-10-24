from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from .forms import UsuarioForm, PacienteForm, LoginForm

# Signup usando classe (opcional)
class SignupView(CreateView):
    model = User
    form_class = UsuarioForm
    template_name = 'cadastro/form.html'  # seu template de cadastro
    success_url = reverse_lazy('login')

# Cadastro de usuário via função
def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro realizado com sucesso! Agora você pode fazer login.')
            return redirect('login')
    else:
        form = UsuarioForm()
    return render(request, 'cadastro/form.html', {'form': form})

# Cadastro de paciente
def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, 'Cadastro de paciente realizado com sucesso! Agora faça login.')
            return redirect('login')
    else:
        form = PacienteForm()
    return render(request, 'cadastro/form_paciente.html', {'form': form})

# Login por username ou email
def login_view(request):
    form = LoginForm(request.POST or None)
    error = None

    if request.method == 'POST' and form.is_valid():
        username_or_email = form.cleaned_data['username_or_email']
        senha = form.cleaned_data['senha']

        try:
            if '@' in username_or_email:
                user_obj = User.objects.get(email=username_or_email)
                username = user_obj.username
            else:
                username = username_or_email
        except User.DoesNotExist:
            username = None

        user = authenticate(request, username=username, password=senha)

        if user is not None:
            login(request, user)
            tipo = user.profile.tipo_usuario
            if tipo == 0:
                return redirect('dashboard_admin')
            elif tipo == 1:
                return redirect('dashboard_paciente')
            elif tipo == 2:
                return redirect('dashboard_usuario')
        else:
            error = "Usuário ou senha inválidos"

    return render(request, 'cadastro/login.html', {'form': form, 'error': error})

# Dashboards
@login_required
def admin_dashboard(request):
    return render(request, 'dashboards/admin.html')

@login_required
def paciente_dashboard(request):
    return render(request, 'dashboards/paciente.html')

@login_required
def usuario_dashboard(request):
    return render(request, 'dashboards/usuario.html')
