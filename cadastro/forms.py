from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model
from .models import Paciente

User = get_user_model()

class UsuarioForm(UserCreationForm):
    # ✅ PRIMEIRO NOME OBRIGATÓRIO
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primeiro nome'
        }),
        label="Primeiro Nome"
    )
    
    # ✅ SOBRENOME OBRIGATÓRIO
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sobrenome'
        }),
        label="Sobrenome"
    )
    
    # ✅ TELEFONE OBRIGATÓRIO
    phone = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999'
        }),
        label="Telefone"
    )
    
    email = forms.EmailField(required=True, label='E-mail')

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'phone', 'password1', 'password2']

class PacienteForm(forms.ModelForm):
    # ✅ CAMPOS DO USER (OBRIGATÓRIOS)
    first_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Primeiro nome do paciente'
        }),
        label="Primeiro Nome"
    )
    
    last_name = forms.CharField(
        max_length=30,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Sobrenome do paciente'
        }),
        label="Sobrenome"
    )
    
    phone = forms.CharField(
        max_length=20, 
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': '(11) 99999-9999'
        }),
        label="Telefone"
    )
    
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'E-mail do paciente'
        }),
        label="E-mail"
    )
    
    senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Senha"
    )
    confirm_senha = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control'}),
        label="Confirmar senha"
    )
    
    # CAMPOS ESPECÍFICOS DO PACIENTE (OPCIONAIS)
    doenca = forms.CharField(
        label="Doença",
        required=False,
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    laudo = forms.FileField(
        label="Laudo médico", 
        required=False,
        widget=forms.FileInput(attrs={'class': 'form-control'})
    )

    class Meta:
        model = Paciente
        fields = ['doenca', 'laudo']

    def clean(self):
        cleaned_data = super().clean()
        senha = cleaned_data.get("senha")
        confirm_senha = cleaned_data.get("confirm_senha")

        if senha and confirm_senha and senha != confirm_senha:
            self.add_error("confirm_senha", "As senhas não coincidem.")

        return cleaned_data

class LoginForm(forms.Form):
    username_or_email = forms.CharField(
        label="Usuário ou E-mail",
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite seu usuário ou e-mail'
        })
    )
    senha = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha'
        })
    )
