from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Paciente

class UsuarioForm(UserCreationForm):
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        labels = {
            'username': 'Nome de usuário',
            'password1': 'Senha',
            'password2': 'Confirme a senha',
        }

class PacienteForm(forms.ModelForm):
    senha = forms.CharField(widget=forms.PasswordInput, label="Senha")

    class Meta:
        model = Paciente
        fields = ['nome_completo', 'cpf', 'telefone', 'email', 'laudo', 'senha']

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Usuário ou E-mail",
        max_length=150,
        widget=forms.TextInput(attrs={'placeholder': 'Digite seu usuário ou e-mail'})
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={'placeholder': 'Digite sua senha'})
    )

