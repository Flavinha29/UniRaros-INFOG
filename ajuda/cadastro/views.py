from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from .forms import UsuarioForm, PacienteForm, LoginForm

User = get_user_model()


# ========== CADASTRO COMUM ==========
class SignupView(CreateView):
    model = User
    form_class = UsuarioForm
    template_name = 'cadastro/form.html'
    success_url = reverse_lazy('cadastro:login')


def cadastrar_usuario(request):
    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.tipo_usuario = "usuario"
            user.save()

            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('cadastro:login')
    else:
        form = UsuarioForm()

    return render(request, 'cadastro/form.html', {'form': form})


# ========== CADASTRO DE PACIENTE ==========
def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)

        if form.is_valid():

            email = form.cleaned_data['email']

            # ----- GERA USERNAME AUTOMÁTICO ÚNICO -----
            base_username = email.split('@')[0]
            username = base_username
            contador = 1

            while User.objects.filter(username=username).exists():
                username = f"{base_username}{contador}"
                contador += 1

            # ----- CRIA O USER -----
            user = User.objects.create_user(
                username=username,
                email=email,
                password=form.cleaned_data['senha'],
                tipo_usuario="paciente"
            )

            # ----- CRIA O PACIENTE -----
            paciente = form.save(commit=False)
            paciente.user = user
            paciente.save()

            messages.success(request, 'Paciente cadastrado com sucesso!')
            return redirect('cadastro:login')

    else:
        form = PacienteForm()

    return render(request, 'cadastro/form_paciente.html', {'form': form})


# ========== LOGIN ==========
def login_view(request):
    form = LoginForm(request.POST or None)
    error = None

    if request.method == 'POST' and form.is_valid():
        username_or_email = form.cleaned_data['username_or_email']
        senha = form.cleaned_data['senha']

        if '@' in username_or_email:
            try:
                username = User.objects.get(email=username_or_email).username
            except User.DoesNotExist:
                username = None
        else:
            username = username_or_email

        user = authenticate(request, username=username, password=senha)

        if user:
            login(request, user)

            if user.tipo_usuario == "paciente":
                return redirect('cadastro:dashboard_paciente')
            elif user.tipo_usuario == "usuario":
                return redirect('cadastro:dashboard_usuario')
            else:
                return redirect('cadastro:dashboard_admin')

        error = "Usuário ou senha inválidos."

    return render(request, 'cadastro/login.html', {
        'form': form,
        'error': error
    })


# ========== DASHBOARDS ==========
@login_required
def dashboard_admin(request):
    return render(request, 'dashboards/admin.html')


@login_required
def dashboard_paciente(request):
    return render(request, 'dashboards/paciente.html')


@login_required
def dashboard_usuario(request):
    return render(request, 'dashboards/usuario.html')
