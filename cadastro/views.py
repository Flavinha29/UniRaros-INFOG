from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.views.generic.edit import CreateView
from django.contrib.auth import get_user_model
from .forms import UsuarioForm, PacienteForm, LoginForm
from .models import Profile, Paciente

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
            user.user_type = "staff"
            user.save()

            messages.success(request, 'Cadastro realizado com sucesso!')
            return redirect('cadastro:login')
    else:
        form = UsuarioForm()

    return render(request, 'cadastro/form.html', {'form': form})

def cadastrar_paciente(request):
    if request.method == 'POST':
        form = PacienteForm(request.POST, request.FILES)

        if form.is_valid():
            try:
                email = form.cleaned_data['email']
                first_name = form.cleaned_data['first_name']
                last_name = form.cleaned_data['last_name']
                phone = form.cleaned_data['phone']
                doenca = form.cleaned_data.get('doenca', '')
                laudo = request.FILES.get('laudo')

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
                    user_type="patient",
                    status="pending",
                    first_name=first_name,
                    last_name=last_name,
                    phone=phone
                )

                # ✅ ATUALIZA o Profile para tipo Paciente (já foi criado pelo signal)
                profile = Profile.objects.get(user=user)
                profile.tipo_usuario = 1  # 1 = Paciente
                profile.save()

                # ----- CRIA O PACIENTE -----
                paciente = Paciente(
                    user=user,
                    doenca=doenca,
                    laudo=laudo
                )
                paciente.save()

                messages.success(request, 'Paciente cadastrado com sucesso! Aguarde aprovação.')
                return redirect('cadastro:login')

            except Exception as e:
                messages.error(request, f'Erro no cadastro: {str(e)}')
                return render(request, 'cadastro/form_paciente.html', {'form': form})

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

            if user.user_type == "patient":
                return redirect('cadastro:dashboard_paciente')
            elif user.user_type == "staff":
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

# ========== PERFIL ==========
@login_required
def perfil_view(request):
    return render(request, 'cadastro/perfil.html', {
        'user': request.user
    })

@login_required
def editar_perfil(request):
    user = request.user

    if request.method == 'POST':
        user.first_name = request.POST.get('first_name')
        user.last_name = request.POST.get('last_name')
        user.email = request.POST.get('email')
        user.save()
        return redirect('cadastro:perfil')

    return render(request, 'cadastro/editar_perfil.html')

@login_required
def alterar_foto(request):
    profile, created = Profile.objects.get_or_create(user=request.user)

    if request.method == "POST" and request.FILES.get("image"):
        profile.image = request.FILES["image"]
        profile.save()
        return redirect("cadastro:perfil")

    return render(request, "cadastro/alterar_foto.html", {"profile": profile})
